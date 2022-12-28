from PyQt5.QtWidgets import QMainWindow, QApplication, QSizeGrip,QLineEdit, \
    QMessageBox,QInputDialog, QVBoxLayout,  QSizePolicy, QGridLayout, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QBasicTimer
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

import time
import os
import random

from ui import newDownloaderInterface_
# import newDownloaderInterface
from generalFunctions import GeneralFunctions
from threadGetEntry import GetEntryThread
from threadGetInternetDownloadSpeed import GetInternetConnectionSpeed, DownloadSpeedThread, InternetConnection
from videoDatabase import VideoDatabase
from threadLoadDataFromDatabase import LoadDataFromDB
from threadStatistics import Statistics
from threadAddNewDownload import AddNewDownloadItems
from threadDownloadController import DownloadController
from threadMonitorRunningThreads import  MonitorRunningThread
from threadLoadParentItem import LoadParentItems
from threadAnimations import ObjectBlinker
from runtimeStyleSheet import  VideoDownloaderStyleSheet, ColorScheme,Proxy
# from threadLicenseChecker import LicenseChecker
from security import JBEncrypter, LicenseGenerator, JBHash
from authentication import Authentications
from exceptionList import *
import requests
from environment import Config
from dialogs import MessageBox
import apiCalls
import supported_sites
from threadLoadSupportedSites import SupportedSitesLoaderThread
from getSubtitleList import GetSubtitleList

#Pyinstaller -w -y videoDownloader.spec

# test subtitle::: https://www.youtube.com/watch?v=smjfGmCn7x0

import yt_dlp as youtube_dl     #yt-dlp-2022.1.21, yt-dlp 2022.3.8.2

'''
--proxy URL                      Use the specified HTTP/HTTPS/SOCKS proxy.
                                 To enable SOCKS proxy, specify a proper
                                 scheme. For example
                                 socks5://127.0.0.1:1080/. Pass in an empty
                                 string (--proxy "") for direct connection
--socket-timeout SECONDS         Time to wait before giving up, in seconds
--source-address IP              Client-side IP address to bind to
-4, --force-ipv4                 Make all connections via IPv4
-6, --force-ipv6                 Make all connections via IPv6
'''

# ffmpeg -i wildlife.wmv -c:v libx264 wildlife.mp4

# ---------------------------
# Global variable declaration
# ---------------------------
restart = False

playlist_contains_private_video = r'https://www.youtube.com/watch?v=5NdLgQQLPk4&list=PLxuUHF3OiqfVxvC178FariJNrFLh-e9n2'


class JBVideoDownloader(QMainWindow, newDownloaderInterface_.Ui_MainWindow):

    def __init__(self):
        super(JBVideoDownloader, self).__init__()
        # setting up the ui
        # ---------------------
        try:
            print("[Debug] Setting up Main window UI: JBVidewoDownloader.__init__")
            self.setupUi(self)
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.buttonTheme.setIcon(QIcon(":/white icons/White icon/sun.svg"))
            self.setWindowIcon(QIcon(":/icons/jba logo.png"))
            self.activation_in_progress = False
            self.threadController = {}

            self.database = VideoDatabase()
            # --> start initializing the database
            print("[Debug] \tSetting up database")
            self.database.initialize_database()

            self.spinBoxNumberOfRetries.setStyle(Proxy())
            self.spinBoxConcurrentDownload.setStyle(Proxy())
            p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))
            print(p)

            # title = GetSubtitleList(url='https://www.youtube.com/watch?v=4e9ouxqKfuE')
            # print(title.get_subtitle_list())
            #
            # input("Wait")

            # stylesheet
            self.my_color_scheme = ColorScheme()
            self.my_stylesheet = VideoDownloaderStyleSheet(self, self.my_color_scheme.dark_theme())
            self.my_stylesheet.apply_stylesheet()  # apply stylesheet to self
            GeneralFunctions().centralize_main_window(self)
            # print("here")
            # [AUTHENTICATION]
            self.authentications = Authentications(self)
            self.allow_downloading = False
            # print("here")
            # print(JBEncrypter().encrypt("http://44.208.20.214/", Config().config('ENCRYPT_PASSWORD')))

            # custom message box
            self.msgBox = MessageBox()

            # variables declarations
            self.generalFunction = GeneralFunctions()
            # self.info_logger = self.InfoLogger()
            self.busy = False
            self.download_entries = []
            self.available_formats = []
            self.common_title = ""
            self.private_video_count = 0

            self.timer = QBasicTimer()
            self.main_message = ""
            self.download_speed = 0
            self.is_internet = False
            self.ip_address = None
            self.default_download_location = os.path.join(os.getcwd(), 'Downloads')



            # these are initialized in the initialize after database initialization as been completed
            self.internet_speed = None
            self.data_loader = None
            self.statistics_loader = None
            self.add_new_loader = None
            self.download_controller = None
            self.monitor_running_thread = None
            self.parent_item_loader = None
            self.blinkerList = {}
            # self.license_checker = None

            self.data_loading_completed = False # indicator to know when data is fully loaded from database at startup
            self.load_next = True  # intended to be used to control loading of items into the parent window

            self.win_list ={}

            # connect buttons to functions(actions)
            # -----------------------------------------
            self.buttonTheme.clicked.connect(self.change_theme)
            self.buttonHideShowAddNew.clicked.connect(self.slideAddNewPanel)
            self.buttonShowHideStatistics.clicked.connect(self.slideFrameStatistics)
            self.buttonRestoreMaximize.clicked.connect(self.restore_or_maximize_window)
            self.buttonClose.clicked.connect(self.close)
            self.buttonMinimize.clicked.connect(self.showMinimized)

            # configure a layout
            # --------------------
            self.pl = QVBoxLayout()
            self.pl.setAlignment(Qt.AlignTop)
            self.pl.setSpacing(0)

            sizePolicy = QSizePolicy()
            sizePolicy.setVerticalStretch(1)
            sizePolicy.setHorizontalStretch(1)
            sizePolicy.setHorizontalPolicy(QSizePolicy.Expanding)

            # apply layout configuration on parent scroll area widget
            self.parentScrollAreaWidgetContents.setLayout(self.pl)
            self.parentScrollAreaWidgetContents.setSizePolicy(sizePolicy)

            # setup layout for supported sites
            self.ssl = QGridLayout()
            self.supportedSitesScrollAreaWidgetContents.setLayout(self.ssl)


            # Resize Grip configuration
            # -----------------------------
            QSizeGrip(self.frame_resize_grip)

            # movement of window by dragging title bar
            # ----------------------------------------
            def moveWindow(e):
                try:
                    if not self.isMaximized():
                        if e.buttons() == Qt.LeftButton:
                            # move window
                            self.move(self.pos() + e.globalPos() - self.clickPosition)
                            self.clickPosition = e.globalPos()
                            e.accept()
                except Exception as e:
                    print(e)

            self.frame_TitleBar.mouseMoveEvent = moveWindow

            self.initialScreenSize = self.generalFunction.get_screen_size()

            self.initialize()

            # tesing testing testing
            self.textAddNewURL.textChanged.connect(self.start_extraction)
            self.buttonAddNewDownload.clicked.connect(self.add_to_download_list)
            self.buttonDelete.clicked.connect(lambda: self.restart_app(prompt=True))
            self.fsp = None
            self.total_loaded = 0
            self.total_data = self.database.get_total_number()
            self.spinBoxNumberOfRetries.valueChanged.connect(self.change_settings)
            self.spinBoxConcurrentDownload.valueChanged.connect(self.change_settings)
            self.buttonBrowseDownloadLocation.clicked.connect(self.change_settings)
            self.buttonSettings.clicked.connect(self.slideSettingsPanel)
            self.checkBoxAutoAdd.clicked.connect(self.change_settings)
            self.checkBoxCheckInternetSpeed.clicked.connect(self.change_settings)
            self.checkBoxTooltipAssistance.clicked.connect(self.change_settings)
            self.buttonExpandAll.clicked.connect(self.expand_all)
            self.buttonCollapseAll.clicked.connect(self.collapse_all)
            # self.textLicense.textChanged.connect(self.proof_read_license_code)
            self.buttonTitleIcon.clicked.connect(self.about_me)
            self.buttonUser.clicked.connect(self.about_user)
            self.buttonUser.setToolTip("License Owner! Click for more...")
            self.buttonDoneWithLocalhostTest.clicked.connect(self.done)
            self.checkBoxTestWithLocalhost.clicked.connect(self.localhost_test_switch)
            self.buttonViewSupportedSites.clicked.connect(self.view_supported_site)

            # application ACTIVATION
            # ----------------------------------------------------------------------------
            self.buttonActivate.clicked.connect(self.activate)
            self.buttonActivateLicense.clicked.connect(self.activate_license)
            # ----------------------------------------------------------------------------

            self.children_window_handle_list = []
            self.timerConstant = 0

            self.internetBlinker = ObjectBlinker(self, self.buttonInternetAvailable, 0.3)

            self.labelTitle.installEventFilter(self)
            self.frame_2.installEventFilter(self)
            self.frame_connection_stats.installEventFilter(self)
            self.labelEmailAddress.installEventFilter(self)
            self.labelEmailAddress.setToolTip("Not a valid Email Address? or License was not received after 5mins. \nDouble Click here to request for a change.")
            self.buttonAddNewDownload.installEventFilter(self)
            self.labelAbout.installEventFilter(self)

            self.textOwner.installEventFilter(self)
            self.textOwner.setToolTip("License Owner! Double click for more...")

            self.labelSettings.installEventFilter(self)

            #Extra-------------------------------------
            self.license_point_of_failure = None
            self.activated = False # keep track of app activation status
            self.checking_available_server_in_progress = False
            self.milestone_ready = True

            self.ss_loader_busy = False
            self.load_supported_sites()

            # want to use this to create a channel folder if multiple playlist is detected
            self.channelDownload = False
            self.channelName = None
            self.duplicateVideoEntry = 0

        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > __init__(): {e}")

    def view_supported_site(self):
        if self.buttonViewSupportedSites.isChecked():
            self.mainStackedWidget.setCurrentWidget(self.PageSupportedSites)
            self.buttonViewSupportedSites.setText("Show Download Page")
            # self.load_supported_sites()
        else:
            self.mainStackedWidget.setCurrentWidget(self.PageDownloader)
            self.buttonViewSupportedSites.setText("View Supported Sites")

    def load_supported_sites_bak(self):
        try:
            ss = supported_sites.get_supported_site()
            total = len(ss)
            col = 4
            row = round(total/col) + 1

            counter = 0
            for i in range(1, row):
                for j in range(1, col + 1):
                    try:
                        site = QLabel()
                        site.setText(ss[counter].split(":")[0])
                        site.setWordWrap(True)
                        # site.setMaximumWidth(200)
                        counter += 1
                        site.setStyleSheet("color: rgb(0,255,127); background-color: rgb(35,35,35); border: 1px solid gray; border-radius: 15px; margin: 10px, 0px; padding:10px; font-size:11pt")
                        self.supportedSitesScrollAreaWidgetContents.layout().addWidget(site, i, j)
                    except:
                        continue
        except Exception as e:
            pass

    def load_supported_sites(self):
        self.counter = 0
        try:
            def supported_site_connector(data):
                # print(data)

                if 'text' in data:
                    self.counter += 1
                    site = QLabel()
                    site.setText(data['text'])
                    site.setWordWrap(True)
                    if data['tooltip'] is not None:
                        site.setToolTip(data['tooltip'])
                    site.setStyleSheet("color: rgb(0,255,127); "
                                       "background-color: rgb(35,35,35); "
                                       "border: 1px solid gray; "
                                       "border-radius: 15px; "
                                       "margin: 10px, 0px; "
                                       "padding:10px; "
                                       "font-size:11pt")

                    self.supportedSitesScrollAreaWidgetContents.layout().addWidget(site, data['row'], data['col'])
                    self.ss_loader_busy = False
                    self.labelSupportedSiteTitle.setText(f"Supported Sites List -- Loading [{self.counter}]...")

                if 'completed' in data:
                    self.labelSupportedSiteTitle.setText("Supported Sites List")
                    pass

            self.threadController['supported sites'] = SupportedSitesLoaderThread(self)
            self.threadController['supported sites'].start()
            self.threadController['supported sites'].any_signal.connect(supported_site_connector)

        except Exception as e:
            pass

    def reset_me(self):
        user = self.database.get_settings('owner')
        print(user)
        if str(user).__contains__("-"):
            username = str(user).split("-")[0].strip()
            email = str(user).split("-")[1].strip()
        else:
            username = email = user

        reset = self.msgBox.show_question("RESET?", "Reset Application to factory defaul? \n\nAll settings and license will be lost.")
        if self.msgBox.Yes:
            password, ok = QInputDialog.getText(self, "Password", "", QLineEdit.EchoMode.Password)
            if ok is True:
                if password == f"Reset@{username}":
                    db = self.database.dbname
                    try:
                        os.remove(db)
                    except:
                        pass

                    self.restart_app(False)
                elif password == "Show Local Host Test":
                    self.frame_test_with_localhost.setVisible(True)

    def done(self):
        self.checkBoxTestWithLocalhost.setChecked(False)
        self.frame_test_with_localhost.setVisible(False)

    def localhost_test_switch(self):
        if self.checkBoxTestWithLocalhost.isChecked() is True:
            self.database.update_setting('localhost_test', True)
            self.labelTitle.setText("JBA Video Downloader -- [Server: Localhost]")
        else:
            self.database.update_setting('localhost_test', False)
            self.labelTitle.setText("JBA Video Downloader")

    def about_me(self):
        self.msgBox.show_information("About","JBADONAI VIDEO DOWNLOADER (JVD)\n\n"
                                             "Developed by: Jbadonaiventures International.\n"
                                             "Email: jbadonaiventures@gmail.com\n"
                                             "Phone: +234 802 222 4284\n\n"
                                             "Copyright: \xa9 2022")

    def about_user(self):
        try:
            user = self.database.get_settings('owner')

            if str(user).__contains__("-"):
                username = str(user).split("-")[0].strip()
                email = str(user).split("-")[1].strip()
            else:
                username = email = user

            key = self.database.get_settings('trial_key')
            key_dec = JBEncrypter().decrypt(key, Config().config("ENCRYPT_PASSWORD"))
            license_type = str(key_dec).split("'")[0]

            key = f"{key[:40]} ... {key[-40:]}"
            self.msgBox.show_information("About",f"This application is licensed to:\n"
            f"\t{username}\n"
            f"\t{email}\n\n"
            f"License Type: {license_type}\n\n"
            f"License key: "
            f"{key}\n\n\n"                                             
            f"jbadonaiventures Copyright: \xa9 2022")
        except SoftLandingException:
            pass
        except:
            pass

    def activate(self):
        if self.activation_in_progress is False:
            self.start_up_check()
        else:
            self.msgBox.show_information("Wait!", "Activation process is in progress! Please Wait...")

    def activate_license(self):
        try:
            if self.textLicense.toPlainText() == "" or self.activation_in_progress is True:
                raise SoftLandingException

            self.activation_in_progress = True
            user_license = self.textLicense.toPlainText().strip()

            user_license_dec = JBEncrypter().decrypt(user_license, Config().config('ENCRYPT_PASSWORD'))

            if user_license_dec is None:
                raise InvalidLicenseException

            print('valid license. checking....')
            self.authentications.check_me_on_server_with_license(user_license)

        except SoftLandingException:
            if self.activation_in_progress is True:
                self.msgBox.show_information("Wait!", "License Activation process is in progress! Please Wait...")
            pass
        except InvalidLicenseException:
            self.activation_in_progress = False
            self.msgBox.show_information("Invalid license!", "License provided is invalid. \n\nPlease get a paid license if your trial license has expired, otherwise click 'Activate' button on the toolbar to get your free tiral license.")
        except Exception as e:
            self.activation_in_progress = False
            self.msgBox.show_information("Unhandled Exception!", f"Unhandled exception below occurred in activate license: {e}")
            pass

    def request_for_new_email(self):
        self.msgBox.show_information("No Longer Allowed!", "Changing of Email Address is no longer supported!\n\n"
                                                            "Don't Worry! Application will be automatically activated "
                                                            "with your Trial key!\n\nJust take note of the email "
                                                            "address used as this will be required for full activation.")

    def initialize(self):
        global restart
        restart = False
        try:
            self.mainStackedWidget.setCurrentWidget(self.PageDownloader)

            print("[Debug] Main Window Initialize Start: initialize()")
            self.labelAbout.setText("jbadonaiventures Copyright: \xa9 2022")

            # some of these required database to be ready, so they are initialize here after database initialization
            # --> INITIALIZING ENGINES
            print("[Debug] \tInitializing Engines")
            self.internet_speed = GetInternetConnectionSpeed()  # INTERNET CONNECTION SPEED
            self.data_loader = LoadDataFromDB(self)     # LOAD DATA FROM DATABASE AT START UP
            self.statistics_loader = Statistics(self)   # STATISTICS OF DATA
            self.add_new_loader = AddNewDownloadItems(self)     #
            self.download_controller = DownloadController(self)   # CONTROLS SETTING DOWNLOAD STATUS BASE ON...
            self.monitor_running_thread = MonitorRunningThread(self)
            self.parent_item_loader = LoadParentItems(self)

            # LICENSE
            # --------------------------------------------------------
            # self.license_checker = LicenseChecker(self)
            # --------------------------------------------------------

            #  --> initialize timer
            print("[Debug] \tStarting Timer")
            self.timer.start(200, self)

            # --> LOAD DATA FROM DATABASE (in a thread)
            print("[Debug] Loading Data from Database")
            totalData = self.database.get_total_number()    # check if there is data in the database to load
            self.total_data = totalData
            if totalData > 0:
                self.data_loader.start_loading() # load data from database
            else:
                self.data_loading_completed = True

            # --> START ENGINES (running continuously in a thread)
            start_speed = bool(int(self.database.get_settings('check_internet_speed')))
            if start_speed is True:
                self.frame_internet_speed.setVisible(True)
                self.start_internet_speed_check()   # [1]start internet speed checker thread
            else:
                self.frame_internet_speed.setVisible(False)

            self.start_internet_connection_check()  # start checking for internet availability
            self.statistics_loader.start_getting_statistics()   # start satistics checker
            self.download_controller.start_download_controller()    # controlls download
            self.monitor_running_thread.start_monitoring_running_threads() # monitors all running threads

            # [AUTHENTICATION]
            # ----------------------------------------
            # self.license_checker.start()
            # ----------------------------------------

            # -->load settings
            self.load_settings()
            self.frame_main_settings.setVisible(False)

            # :::::> initial security/license check
            self.start_up_check()
            self.authentications.monitor_license_key()

            # --> FINE TUNE
            self.buttonAddNewDownload.setText("\tAdd to download List") # change text on the add download button
            self.textAddNewURL.setFocus() # set focus on the url text box
            self.buttonTheme.setVisible(False)
            self.frame_retries.setVisible(False)
            self.radioButtonVideoDownload.setChecked(True)
            self.radioButtonMp4.setChecked(True)

            lht = bool(int(VideoDatabase().get_settings('localhost_test')))    # local host test value

            if lht is False:
                self.frame_test_with_localhost.setVisible(False)
                self.labelTitle.setText("JBA Video Downloader")
            else:
                self.frame_test_with_localhost.setVisible(True)
                self.checkBoxTestWithLocalhost.setChecked(lht)
                self.labelTitle.setText("JBA Video Downloader -- [Server: Localhost]")

            # SERVERS CHECK
            sl = self.generalFunction.get_server_list_from_db()
            print(f"Server list before update: {sl}")
            self.find_available_server()

            #   tooltip assistance
            tt = bool(int(self.database.get_settings('tooltip_assistance')))
            if tt is False:
                self.disable_tooltip()

            # self.buttonActivate.setVisible(False)
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > initialize(): {e}")

    def find_available_server(self):
        self.checking_available_server_in_progress = True
        def find_server_connector(data):
            try:
                # print(data)
                # print(f"DATA: {data}")
                if 'server' in data:
                    print(f"AVAILABLE SERVERS DETECTED: {data['server']}")
                    # GET LIST OF AVAILABLE SERVERS
                    available_servers = data['server']
                    if len(available_servers) <= 0:
                        raise SoftLandingException

                    # ENCRYPT IT
                    encrypted_available_server = JBEncrypter().encrypt(str(available_servers),
                                                                       Config().config('ENCRYPT_PASSWORD'))

                    # SAVE IT TO DATABASE
                    self.database.update_setting('server_list', encrypted_available_server)
                    print(f"Server list updated")

                    self.checking_available_server_in_progress = False

                if 'message' in data:
                    print(data['message'])
            except SoftLandingException:
                print(f"Server list update completed! No server list detected")
                pass
            except:
                pass

        try:
            self.threadController['find_server'] = apiCalls.FindServerListThread()
            self.threadController['find_server'].start()
            self.threadController['find_server'].find_server_signal.connect(find_server_connector)
        except Exception as e:
            print(f"eeeeeeeeeeeeee: {e}")
            pass

    def start_up_check(self):
        try:
            print(f"[DEBUB][STARTUP] - startup check started")
            #   1. check and skip this check if app is fully activated
            full_activation = self.generalFunction.is_fully_activated()
            if full_activation is True:
                raise FullyActivatedException

            print(f"[DEBUB][STARTUP] - No full license detected")

            #   2. check local db if there is a key
            is_lic_key = self.generalFunction.is_there_trial_key()

            if is_lic_key is False:     # i.e. no license key on local db:
                # check if pc has been registered before and download settings for the pc
                # if not register new user
                print(f"[DEBUB][STARTUP] - No license detected in local db. checking me on server")
                self.activation_in_progress = True
                self.authentications.check_me_on_server()

            else:   # i.e. a license key is on the local db:
                # Extract info from the key
                #   a. get the license from db
                lic = self.generalFunction.get_trial_key()

                #   b. decrypt the license
                licDecrypted = JBEncrypter().decrypt(lic, Config().config("ENCRYPT_PASSWORD"))

                # check if license is not valid
                if licDecrypted is None:
                    self.disable_downloading()
                    raise InvalidLicenseException

                #   c. separate the content/data stored in the user license
                lic_type, email, system_id, system_key, actual_license = licDecrypted.split("'")

                #   d. check if license has expired or not
                result = LicenseGenerator().is_license_expired(actual_license)
                print(result)
                licExpired = result[0]  # license expired status
                # licStatus = result[1]  # remaining days in license
                if licExpired is True:
                    self.disable_downloading()
                else:
                    self.enable_downloading()

        except FullyActivatedException:
            pass
        except InvalidLicenseException:
            self.msgBox.show_information("Invalid License", "Invalid license Code detected")

            pass
        except:
            pass

    def disable_tooltip(self):
        self.buttonViewSupportedSites.setToolTip("")
        self.buttonActivate.setToolTip("")
        self.buttonCollapseAll.setToolTip("")
        self.buttonDelete.setToolTip("")
        self.buttonExpandAll.setToolTip("")
        self.buttonSettings.setToolTip("")
        self.buttonUser.setToolTip("")
        self.textOwner.setToolTip("")
        self.buttonTheme.setToolTip("")
        self.buttonAddNewDownload.setToolTip("")
        self.comboBoxSelectFormat.setToolTip("")
        self.radioButtonMp4.setToolTip("")
        self.radioButtonMkv.setToolTip("")
        self.radioButtonVideoDownload.setToolTip("")
        self.radioButtonAudioDownload.setToolTip("")
        self.textAddNewURL.setToolTip("")
        self.buttonHideShowAddNew.setToolTip("")
        self.labelAddNewStatus.setToolTip("")
        self.buttonDownloadSubtitleSettings.setToolTip("")
        self.checkBoxDownloadSubtitle.setToolTip("")
        self.checkBoxAutoAdd.setToolTip("")
        self.checkBoxCheckInternetSpeed.setToolTip("")
        self.labelConcurrentDownload.setToolTip("")
        self.spinBoxConcurrentDownload.setToolTip("")
        self.buttonBrowseDownloadLocation.setToolTip("")
        self.textDownloadLocation.setToolTip("")
        self.labelRetries.setToolTip("")
        self.spinBoxNumberOfRetries.setToolTip("")
        self.checkBoxTooltipAssistance.setToolTip("")

    def disable_downloading(self):
        self.allow_downloading = False
        pass

    def enable_downloading(self):
        self.allow_downloading = True
        pass

    def start_extraction(self):

        def loading_connector(data):

            try:
                # print("[DATA] ", data)
                if data['info'] != "Completed!":
                    self.main_message = f"Parsing Video. Please Wait... \n\n{data['info']}"

                    myInfo = str(data['info'])
                    errorMessage = myInfo.split(":")[-1]

                    # print(f"Milesone: {data['milestone']}")
                    if data['milestone'] is True:
                        # Auto add download to the download list
                        # self.radioButtonVideoDownload.setChecked(True)
                        # self.radioButtonMp4.setChecked(True)
                        self.comboBoxSelectFormat.setCurrentIndex(0)
                        self.buttonAddNewDownload.click()
                        self.milestone_ready = True



                    if myInfo.__contains__("Error!"):
                        if errorMessage != "":
                            self.main_message = f"Data Extraction for the selected url Failed! Please try another url.\n\n {errorMessage}"
                            # QMessageBox.information(self, "Error!", f"Could not extract data for the selected url. \n\n{errorMessage}"
                            # f" Please try another url")

                            self.msgBox.show_information("Error!", f"Could not extract data for the selected url. \n\n{errorMessage}"
                            f" Please try another url")


                        else:
                            self.main_message = f"Data Extraction for the selected url Failed! Please try another url."
                            # QMessageBox.information(self, "Error!", f"Could not extract data for the selected url."
                            # f" Please try another url")

                            self.msgBox.show_information("Error!", f"Could not extract data for the selected url."
                            f" \n\nPlease check your internet connection or try another url.")
                else:
                    if self.duplicateVideoEntry > 0:
                        if self.duplicateVideoEntry == 1:
                            self.msgBox.show_information("Duplicate Video", f"Completed! But {self.duplicateVideoEntry} duplicate url(s) were found to be existing in your download list and were skipped!")
                        else:
                            self.msgBox.show_information("Duplicate Video", f"Completed! But {self.duplicateVideoEntry} duplicate url(s) were found to be existing in your download list and were skipped!")
                    else:
                        self.labelAddNewStatus.setText("Completed!")
                        # self.msgBox.show_information("completed", "completed")

                # else:
                #     self.main_message = data['info']
                #     if self.checkBoxAutoAdd.isChecked() is False:
                #         if self.private_video_count > 0:
                #             if self.private_video_count == 1:
                #                 # QMessageBox.information(self, "Completed!", f"Video Data Extraction Completed! \n"
                #                 #                                             f"[ {self.private_video_count} Private video detected and skipped! ]\n\n"
                #                 #                                             f"1. Select your desired Download/Format Option. \n\n"
                #                 #                                             f"2. Click 'Add Add To Download List' button")
                #                 self.msgBox.show_information("Completed!", f"Video Data Extraction Completed! \n"
                #                                                             f"[ {self.private_video_count} Private video detected and skipped! ]\n\n"
                #                                                             f"1. Select your desired Download/Format Option. \n\n"
                #                                                             f"2. Click 'Add To Download List' Button")
                #
                #             else:
                #                 # QMessageBox.information(self, "Completed!", f"Video Data Extraction Completed! \n"
                #                 #                                             f"[ {self.private_video_count} Private videos detected and skipped! ]\n\n"
                #                 #                                             f"1. Select your desired Download/Format Option. \n\n"
                #                 #                                             f"2. Click 'Add'")
                #
                #                 self.msgBox.show_information("Completed!", f"Video Data Extraction Completed! \n"
                #                                                             f"[ {self.private_video_count} Private videos detected and skipped! ]\n\n"
                #                                                             f"1. Select your desired Download/Format Option. \n\n"
                #                                                             f"2. Click 'Add To Download List' Button")
                #
                #         else:
                #             # QMessageBox.information(self, "Completed!", "Video Data Extraction Completed! \n\n"
                #             #                                             "1. Select your desired Download/Format Option. \n\n"
                #             #                                             "2. Click 'Add' ")
                #
                #             self.msgBox.show_information("Completed!", "Video Data Extraction Completed! \n\n"
                #                                                         "1. Select your desired Download/Format Option. \n\n"
                #                                                         "2. Click 'Add To Download List' Button ")
                #
                #
                #         self.radioButtonVideoDownload.setChecked(True)
                #         self.radioButtonMp4.setChecked(True)
                #         self.comboBoxSelectFormat.setCurrentIndex(0)
                #     else:
                #         # Auto add download to the download list
                #         self.radioButtonVideoDownload.setChecked(True)
                #         self.radioButtonMp4.setChecked(True)
                #         self.comboBoxSelectFormat.setCurrentIndex(0)
                #         self.buttonAddNewDownload.click()
                #         # QMessageBox.information(self, "Added successfully", "Your Video has been successfully added to the download list.")
                #         self.msgBox.show_information("Added successfully", "Your Video has been successfully added to the download list.")
                #
                # pass
            except Exception as e:
                print(f"An error occurred in [videoDownloader.py] > start_extraction() > loading_connector() : {e}")

        try:
            if self.textAddNewURL.text() != "":
                if self.allow_downloading is False:
                    # LOCK
                    # raise NotActivatedException
                    pass
                try:
                    # 1. check if the app is not busy with a request
                    if self.busy is False:
                        self.busy = True
                        self.duplicateVideoEntry = 0

                        # 2. Get the url user want to download
                        url = self.textAddNewURL.text()

                        # 3. Check if the url is valid
                        if self.generalFunction.is_url_valid(url):
                            try:
                                # 4. Check if the url exists in the database as playlist url or video url
                                playlistUrlExists = self.database.is_playlist_url_exists_in_database(url)
                                videoUrlExists = self.database.is_url_exists_in_database(url)

                                # 5. Start data extraction if url does not exist in the download list [CORE]
                                if playlistUrlExists is False and videoUrlExists is False:
                                    self.threadController['get entries'] = GetEntryThread(url=url, my_parent=self)
                                    self.threadController['get entries'].start()
                                    self.threadController['get entries'].any_signal.connect(loading_connector)
                                else:
                                    # 5 [a] Stop data extraction process if url exists in download list

                                    # 5 [b] Respond to user if video url exists
                                    if videoUrlExists is True:
                                        entry = self.database.get_entry_by_url(url)
                                        entry = self.generalFunction.database_list_to_dictionary(entry)
                                        # QMessageBox.information(self, "Download Exists", f"This url exists in your download list. \n\n"
                                        #                                                  f"url: {url}\n\n"
                                        #                                                  f"Title: {entry['title']}")

                                        self.msgBox.show_information("Download Exists", f"This url exists in your download list. \n\n"
                                                                                         f"url: {url}\n\n"
                                                                                         f"Title: {entry['title']}")


                                    # 5 [c] Respond to user if playlist url exists
                                    else: # playlistUrlExists is True:
                                        entry = self.database.get_entry_by_playlist_url(url)
                                        entry = self.generalFunction.database_list_to_dictionary(entry)
                                        # QMessageBox.information(self, "Download Exists", f"This playlist url exits in your "
                                        #                                                  f"download list.\n\n"
                                        #                                                  f"url: {entry['playlist_url']}\n\n"
                                        # f"Playlist Title: {entry['playlist_title']}")

                                        self.msgBox.show_information("Download Exists", f"This playlist url exits in your "
                                                                                         f"download list.\n\n"
                                                                                         f"url: {entry['playlist_url']}\n\n"
                                        f"Playlist Title: {entry['playlist_title']}")



                                    # 5 [d] reset data in preparation to receive a new url from user
                                    self.textAddNewURL.clear()
                                    self.busy = False
                            except Exception as e:
                                print(f"An Error occurred in start :>>>\n{e}")
                            pass
                        else:
                            # 3 [b] Respond to user if the url is not valid
                            self.labelAddNewStatus.setText("Invalid URL")
                            # QMessageBox.information(self, "Invalid URL", "Invalid URL supplied!")
                            self.msgBox.show_information("Invalid URL", "Invalid URL Supplied!")

                            # 3 [c] prepare to get a new url from user.
                            self.textAddNewURL.setFocus()
                            self.textAddNewURL.selectAll()
                            self.busy = False
                    else:
                        # 1 [b] Notify user if the app is busy
                        # QMessageBox.information(self, "Busy", "Busy!")
                        self.msgBox.show_information("Busy", "Busy!")

                except Exception as e:
                    self.busy = False
                    print(e)
        except NotActivatedException as e:
            # QMessageBox.information(self, 'Activation Required!', "Sorry! Activation is Required before you can start downloading.\n\n Just follow the simple steps to get your Free Trial License or Paid License.")
            self.msgBox.show_information('Activation Required!', "Sorry! Activation is Required before you can start downloading.\n\nClick 'Activate' button on the toolbar to start.")
            self.textAddNewURL.clear()
            pass
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > start_extraction(): {e}")

    def add_to_download_list(self):
        try:
            if len(self.download_entries) > 0:
                # add users choice (format, download type...) to the download entries
                self.update_download_entries()
                # print(self.download_entries)

                # save the entry to database
                # self.database.insert_into_video_database(self.download_entries)
                self.generalFunction.run_function(self.save_entry, False, self.download_entries)
                # self.save_entry(self.download_entries)

                # self.add_parent_item(self.common_title, self.download_entries)
                self.add_new_loader.start_adding_new_items(self.download_entries)

                self.textAddNewURL.clear()
                self.reset_variables()
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > add_to_download_list() : {e}")

    def update_download_entries(self):
        try:
            for index, entry in enumerate(self.download_entries):
                self.download_entries[index]['download_video'] = self.radioButtonVideoDownload.isChecked()
                self.download_entries[index]['format'] = self.comboBoxSelectFormat.currentText()
                self.download_entries[index]['status'] = "Waiting"
                self.download_entries[index]['download_all'] = True

                if self.channelDownload is True:
                    if self.channelName is None:
                        self.channelName = f"Channel__{random.randint(11111, 99999)}"

                    channel, subChannel = str(self.channelName).split("__")
                    # path = os.path.join(self.textDownloadLocation.text(), self.channelName)
                    path = os.path.join(self.textDownloadLocation.text(), channel, subChannel)
                    self.download_entries[index]['download_location'] = path
                else:
                    self.download_entries[index]['download_location'] = self.textDownloadLocation.text()
                self.download_entries[index]['download_subtitle'] = self.checkBoxDownloadSubtitle.isChecked()

                video_extension = 'mp4'
                if self.radioButtonMkv.isChecked() is True:
                    video_extension = "webm"
                else:
                    video_extension = "mp4"
                self.download_entries[index]['video_extension'] = video_extension



            pass
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > update_download_entries(): {e}")

    def add_parent_item(self, common_title, entries):
        try:
            # temp = f"parent window -  {random.randint(5555, 9999)}"
            # self.win_list[temp] = ParentItemWindow(parent=self, entries=entries, common_title=common_title)
            # self.parentScrollAreaWidgetContents.layout().addWidget(self.win_list[temp])
            print("[Debug] \tLoading of the content starts")
            self.parent_item_loader.start_loading_parent_items(entries, common_title)
            try:
                print("[Debug] \tTrying to scroll to page bottom")
                self.generalFunction.run_function(self.generalFunction.scroll_to_bottom, False,self.parentScrolArea)
            except Exception as e:
                print(e)

        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > add_parent_item(): {e}")
            pass

    def save_entry(self, entry_data):
        """Save a single entry to the database
            entry_data is a list """

        try:
            for data in entry_data:
                # print(data)

                # save the data to database
                self.database.insert_into_video_database(data=data)

        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > save_entry(): {e}")
            pass
        pass

    def load_entries(self):
        """Loads all Entries from the database """
        try:
            all_data = []
            lastPlaylistTitle = ""
            newPlaylistBegins = False
            tempData = []
            done = False

            last_status_is_playlist = False
            totalPlaylistVideo = 0
            playlistCounter = 0

            entries = self.database.get_all_video_data()
            for index, entry in enumerate(entries):
                entry = self.generalFunction.database_list_to_dictionary(entry)

                if entry['is_playlist'] is False:
                    if last_status_is_playlist is True:
                        last_status_is_playlist = False

                    done = True
                    td = [entry]
                    all_data.append(td)
                else:
                    last_status_is_playlist = True
                    playlistCounter += 1

                    if totalPlaylistVideo == 0:
                        totalPlaylistVideo = self.database.get_no_of_video_in_playlist(entry['playlist_url'])

                    # for Playlist. attempt to group same video in a playlist together
                    playlistTitle = entry['playlist_title']

                    # detect if a new playlist has been encountered
                    if lastPlaylistTitle != playlistTitle and newPlaylistBegins is False:
                        done = False
                        newPlaylistBegins = True
                        lastPlaylistTitle = playlistTitle
                        tempData.append(entry)

                    elif lastPlaylistTitle == playlistTitle and newPlaylistBegins is True:
                        tempData.append(entry)

                    if totalPlaylistVideo == playlistCounter:
                        totalPlaylistVideo = 0
                        playlistCounter = 0
                        done = True
                        newPlaylistBegins = False
                        lastPlaylistTitle = ""
                        all_data.append(tempData)

                if done is True:
                    for data in all_data:
                        self.download_entries = data
                        self.add_parent_item(self.common_title, self.download_entries)

                    all_data.clear()
                    tempData.clear()
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > load_entries(): {e}")

    def reset_variables(self):
        try:
            # self.busy = False
            self.download_entries = []
            self.available_formats = []
            self.common_title = ""
            self.private_video_count = 0
            self.comboBoxSelectFormat.clear()
            self.comboBoxSelectFormat.addItem("Best Quality")
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > reset_variables()")

    def change_theme(self):
        try:
            # from apiCalls import ApiCalls
            #
            # ApiCalls().send_user_settings()
            # if str(self.styleSheet())[2] == 'l':
            #     # self.setStyleSheet(Stylesheet().darkTheme)
            #     self.buttonTheme.setIcon(QIcon(":/white icons/White icon/sun.svg"))
            # else:
            #     # self.setStyleSheet(Stylesheet().lightTheme)
            #     self.buttonTheme.setIcon(QIcon(":/white icons/White icon/moon.svg"))
            pass
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > change_theme(): {e}")

    def slideAddNewPanel(self):
        try:
            height = self.frame_addNew.height()

            if height <= 50:
                newHeight = 300
                self.buttonHideShowAddNew.setIcon(QIcon(":/white icons/White icon/chevron-up.svg"))
                self.frame_AddNewOptions.setVisible(True)
                self.frame_AddNewURL.setVisible(True)
                self.labelAddNewStatus.setVisible(True)

            else:
                self.fsp = self.frame_AddNewOptions.sizePolicy()
                newHeight = 50
                self.buttonHideShowAddNew.setIcon(QIcon(":/white icons/White icon/chevron-down.svg"))
                self.frame_AddNewOptions.setVisible(False)
                self.frame_AddNewURL.setVisible(False)
                self.labelAddNewStatus.setVisible(False)

            try:
                self.animation = QPropertyAnimation(self.frame_addNew, b"maximumHeight")
                self.animation.setDuration(100)
                self.animation.setStartValue(height)
                self.animation.setEndValue(newHeight)
                self.animation.setEasingCurve(QEasingCurve.InOutQuart)
                self.animation.start()
            except Exception as e:
                print(f"An Error occurred slideAddNewPanel \n >>>{e}")
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > slideAddNewPanel() \n >>>{e}")

    def slideFrameStatistics(self):
        try:
            height = self.frame_statistics.height()
            # print(height)
            if height <= 40:

                newHeight = 101
                self.buttonShowHideStatistics.setIcon(QIcon(":/white icons/White icon/chevron-down.svg"))
                self.frame_statistics_details.setVisible(True)
                self.frame_about.setVisible(True)
            else:
                newHeight = 40
                self.buttonShowHideStatistics.setIcon(QIcon(":/white icons/White icon/chevron-up.svg"))
                self.frame_statistics_details.setVisible(False)
                self.frame_about.setVisible(False)

            try:
                self.animation = QPropertyAnimation(self.frame_statistics, b"maximumHeight")
                self.animation.setDuration(100)
                self.animation.setStartValue(height)
                self.animation.setEndValue(newHeight)
                self.animation.setEasingCurve(QEasingCurve.InOutQuart)
                self.animation.start()
            except Exception as e:
                print(f"An Error occurred slideAddNewPanel \n >>>{e}")
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > slideAddNewPanel() \n >>>{e}")

    def slideSettingsPanel(self):
        try:
            if self.frame_main_settings.isVisible() is True:
                self.frame_main_settings.setVisible(False)

            else:
                width = self.width()
                if self.isMaximized() is True:
                    self.frame_main_settings.setVisible(True)
                    self.frame_main_settings.setMaximumWidth(int(width/5))
                    self.frame_main_settings.setMinimumWidth(int(width/5))
                else:
                    self.frame_main_settings.setVisible(True)
                    self.frame_main_settings.setMaximumWidth(int(width/3.5))
                    self.frame_main_settings.setMinimumWidth(int(width/3.5))

                if self.buttonViewSupportedSites.isChecked():
                    # self.mainStackedWidget.setCurrentWidget(self.PageDownloader)
                    self.buttonViewSupportedSites.click()
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > slideSettingsPanel() \n >>>{e}")

    def restore_or_maximize_window(self):
        try:
            if self.isMaximized():
                self.showNormal()
                self.buttonRestoreMaximize.setIcon(QIcon(":/white icons/White icon/maximize-2.svg"))

                if self.frame_main_settings.isVisible():
                    width = self.width()
                    self.frame_main_settings.setVisible(True)
                    self.frame_main_settings.setMaximumWidth(width / 5)
                    self.frame_main_settings.setMinimumWidth(width / 5)
            else:
                self.showMaximized()
                self.buttonRestoreMaximize.setIcon(QIcon(":/white icons/White icon/minimize-2.svg"))

                if self.frame_main_settings.isVisible():
                    width = self.width()
                    if self.isMaximized() is True:
                        self.frame_main_settings.setVisible(True)
                        self.frame_main_settings.setMaximumWidth(width / 3.5)
                        self.frame_main_settings.setMinimumWidth(width / 3.5)
        except Exception as e:
            print(f"AAn error occurred in [videoDownloader.py] > restore_or_maximize_window(): \n >>>{e}")

    def start_internet_speed_check(self):

        def loading(data):
            try:
                # print("[DATA] ", data)
                if 'download speed' in data:
                    self.download_speed = data['download speed']
                else:
                    self.download_speed = "Calculating..."

                if 'upload speed' in data:
                    self.upload_speed = data['upload speed']
                else:
                    self.upload_speed = 0

                pass
            except Exception as e:
                print(f"An error occurred in [videoDownloader.py] > start_internet_speed_check() > loading() : {e}")

        try:
            self.threadController['internet speed'] = DownloadSpeedThread()
            self.threadController['internet speed'].start()
            self.threadController['internet speed'].any_signal.connect(loading)
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > start_internet_speed_check(): {e}")
        pass

    def start_internet_connection_check(self):

        def internet_connection_connector(data):
            try:
                # print("[DATA] ", data)
                if 'internet connection' in data:
                    self.is_internet = data['internet connection']

                    if self.is_internet is True:
                        # ':/white icons/White icon/globe.svg'
                        # self.pushButtonInternetAvailable.setVisible(True)

                        self.buttonInternetAvailable.setIcon(QIcon(':/blue icons/blue icon/globe.svg'))

                        if self.internetBlinker.isActive is True:
                            # print('blinking stops')
                            self.internetBlinker.stop_blinking()
                            self.buttonInternetAvailable.setVisible(True)
                    else:
                        # self.buttonInternetAvailable.setVisible(True)
                        self.buttonInternetAvailable.setIcon(QIcon(':/red icons/red icon/globe.svg'))
                        if self.internetBlinker.isActive is False:
                            # print('blinking starts..........')
                            self.internetBlinker.start_blinking()

                pass
            except Exception as e:
                print(f"An error occurred in [videoDownloader.py] > start_internet_connection_check() > internet_connection_connector() : {e}")

        try:
            self.threadController['internet connection'] = InternetConnection()
            self.threadController['internet connection'].start()
            self.threadController['internet connection'].any_signal.connect(internet_connection_connector)
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > start_internet_connection_check(): {e}")
        pass

    def stop_internet_speed_check(self):
        try:
            self.threadController['internet speed'].stop()
            self.download_speed = 0
            pass
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > stop_internet_speed_check(): {e}")

    def stop_internet_connection_check(self):
        try:
            self.threadController['internet speed'].stop()
            pass
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > stop_internet_connection_check(): {e}")

    def restart_app(self, prompt=True):
        global restart
        try:
            if prompt is True:
                # ans = QMessageBox.question(self, "Restart?", "Are you sure you want to restart the application?",
                #                            QMessageBox.Yes | QMessageBox.No)

                self.msgBox.show_question("Restart?", "Are you sure you want to restart the application?")

                # if ans == QMessageBox.Yes:
                if self.msgBox.Yes:
                    restart = True
                    self.close()
            else:
                restart = True
                self.close()
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > restart-app(): {e}")

    def load_settings(self):
        try:
            downloadLocation = self.database.get_settings('default_download_location')
            max_downloads = self.database.get_settings('max_download')
            max_retries = self.database.get_settings('max_retries')
            auto_add = self.database.get_settings('auto_add_new_download')
            check_internet_speed = self.database.get_settings('check_internet_speed')
            tooltip_assistance = self.database.get_settings('tooltip_assistance')

            self.textDownloadLocation.setText(downloadLocation)
            self.spinBoxConcurrentDownload.setValue(int(max_downloads))
            self.spinBoxNumberOfRetries.setValue(int(max_retries))
            self.checkBoxAutoAdd.setChecked(int(auto_add))
            self.checkBoxCheckInternetSpeed.setChecked(int(check_internet_speed))
            self.checkBoxTooltipAssistance.setChecked(bool(int(tooltip_assistance)))
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > load_settings(): {e}")

    def change_settings(self):
        try:
            sender = self.sender()
            if sender.objectName() == self.spinBoxConcurrentDownload.objectName():
                self.database.update_setting('max_download', self.spinBoxConcurrentDownload.value())

            if sender.objectName() == self.spinBoxNumberOfRetries.objectName():
                self.database.update_setting('max_retries', self.spinBoxNumberOfRetries.value())

            if sender.objectName() == self.buttonBrowseDownloadLocation.objectName():
                result = self.generalFunction.browse_folder_location(self)
                if result is not None:
                    self.textDownloadLocation.setText(result)
                    self.database.update_setting('default_download_location', result)

            if sender.objectName() == self.checkBoxAutoAdd.objectName():
                if self.checkBoxAutoAdd.isChecked() is True:
                    print("True")
                    self.database.update_setting('auto_add_new_download', True)
                else:
                    print("False")
                    self.database.update_setting('auto_add_new_download', False)

            if sender.objectName() == self.checkBoxCheckInternetSpeed.objectName():
                if self.checkBoxCheckInternetSpeed.isChecked() is True:
                    # self.frame_internet_speed.setVisible(True)
                    self.start_internet_speed_check()
                    self.database.update_setting("check_internet_speed", True)
                else:
                    # self.frame_internet_speed.setVisible(False)
                    self.stop_internet_speed_check()
                    self.database.update_setting("check_internet_speed", False)

            if sender.objectName() == self.checkBoxTooltipAssistance.objectName():
                self.msgBox.show_question("Change Settings?", "Changing this settings requires application restart, Continue?")
                if self.msgBox.Yes is True:
                    if self.checkBoxTooltipAssistance.isChecked() is True:
                        self.database.update_setting('tooltip_assistance', True)
                    else:
                        self.database.update_setting('tooltip_assistance', False)

                    self.restart_app(False)

                else:
                    self.checkBoxTooltipAssistance.setChecked(not self.checkBoxTooltipAssistance.isChecked())




        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > change-settings(): {e}")

    def collapse_all(self):
        try:
            total = self.parentScrollAreaWidgetContents.layout().count()

            for index in range(total):
                item = self.parentScrollAreaWidgetContents.layout().itemAt(index).widget()
                if item.frame_parent.isVisible():
                    item.buttonShowHideDetails.click()
            pass
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > collapse_all(): {e}")

    def expand_all(self):
        try:
            total = self.parentScrollAreaWidgetContents.layout().count()

            for index in range(total):
                item = self.parentScrollAreaWidgetContents.layout().itemAt(index).widget()
                if item.frame_parent.isVisible() is False:
                    item.buttonShowHideDetails.click()
            pass
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > expand_all(): {e}")

    def eventFilter(self, source, event):
        try:
            if event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.labelTitle:
                self.restore_or_maximize_window()

            if event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.frame_2:
                self.restore_or_maximize_window()

            if event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.frame_connection_stats:
                self.restore_or_maximize_window()

            if event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.labelEmailAddress:
                self.request_for_new_email()

            if event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.labelAbout:
                self.about_me()

            if event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.textOwner:
                self.about_user()

            if event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.labelSettings:
                self.reset_me()

            if event.type() == QtCore.QEvent.Enter and source is self.buttonAddNewDownload:
                # print('hover')
                # self.highlight.start_highlight(self.buttonAddNewDownload)
                pass

            if event.type() == QtCore.QEvent.Leave and source is self.buttonAddNewDownload:
                # print('Left')
                # self.highlight.stop_highlight(self.buttonAddNewDownload)
                pass



            return super(JBVideoDownloader, self).eventFilter(source, event)
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > eventFilter(): {e}")

    def mousePressEvent(self, event):
        try:
            self.clickPosition = event.globalPos()
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > mousePressEvent(): \n >>>{e}")

    def check_activation_status(self):
        try:
            trialActivated = self.generalFunction.is_trial_activated()
            trialExpired = self.generalFunction.is_trial_expired()
            fullyActivated = self.generalFunction.is_fully_activated()

            if trialActivated is False and trialExpired is False and fullyActivated is False:
                self.labelActivationStatus.setText("Activation Required! Click on Activate Button to Activate your Free Trial License!")
                self.labelActivationStatus.setToolTip("Click on 'Activate' button in the toolbar to Activate your Free Trial License")
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > check_activation_status(): {e}")

    def timerEvent(self, a0):
        try:
            self.adjust_application_size_in_timer()

            # display what is going on in add new section
            self.labelAddNewStatus.setText(f"{self.main_message}")

            if self.checkBoxCheckInternetSpeed.isChecked() is True:
                self.frame_internet_speed.setVisible(True)
                self.display_download_speed_in_timer()
            else:
                self.frame_internet_speed.setVisible(False)

            self.control_format_selection_in_timer()

        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > timer_event(): {e}")

    #  REFACTORING CONTENT OF THE TIMER FROM HERE

    def adjust_application_size_in_timer(self):
        try:
            # Adjust application size if screen resolution changed while app is running
            sz = self.generalFunction.get_screen_size()
            if sz.height != self.initialScreenSize.height or sz.width != self.initialScreenSize.width:
                if self.isMaximized():
                    self.restore_or_maximize_window()
                    time.sleep(1)
                self.initialScreenSize = sz
                self.generalFunction.centralize_main_window()

            pass
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > adjust_applicationsize_in_timer(): {e}")

    def display_download_speed_in_timer(self):
        try:
            # display download speed
            if self.download_speed == 0:
                self.textInternetSpeed.setText("Calculating...")
            else:
                self.textInternetSpeed.setText(self.download_speed)
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > display_download_speed_in_timer(): {e}")
            pass

    def control_format_selection_in_timer(self):
        try:
            # control format selection combobox availability based on download type.
            if self.radioButtonAudioDownload.isChecked() is True:
                self.comboBoxSelectFormat.setEnabled(False)
            else:
                self.comboBoxSelectFormat.setEnabled(True)
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > control_format_selection_in_timer(): {e}")
            pass

    # END TIMER REFACTOR

    def closeEvent(self, e):
        try:
            # just to improve user experience: it takes a while to kill all running process before finally closing
            # hide the window first (smooth close user experience) then close in the background after clean up
            self.hide()

            # try to stop ffmpeg if running. i.e video conversion in progress
            try:
                os.system("taskkill /f /im ffmpeg.exe")
                print('ffmpeg closed.')
            except:
                pass

            # remove all temporary files
            for root, dirs, files in os.walk('temp'):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                        # print(f"removing {file}...")
                    except:
                        continue

            # stop all running threads.
            for thread in self.threadController:
                try:
                    if self.threadController[thread].isRunning:
                        self.threadController[thread].stop()
                        # print(f"stopping thread - {thread}")
                except:
                    continue

            # print('finally clossing....................')
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > closeEvent(): \n >>>{e}")


def start():
    global restart

    if __name__ == '__main__':
        try:
            app = QApplication([])
            app.setStyle('fusion')

            win = JBVideoDownloader()
            win.installEventFilter(win)
            win.show()

            app.exec_()
            if restart is True:
                time.sleep(1)
                start()
        except Exception as e:
            print(f"An error occurred in [videoDownloader.py] > start(): {e}")


start()