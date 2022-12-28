from PyQt5.QtWidgets import QMainWindow,  QMenu, QMessageBox, QPushButton
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import  QIcon
import  time
import webbrowser
from ui import childItemWindow_
# import childItemWindow_
from threadLoadImage import LoadImage
from generalFunctions import GeneralFunctions
# from stylesheet import Stylesheet
from menuItemsList import MenuItemsList
from videoDatabase import VideoDatabase
from threadChildStatusUpdater import ChildStatusUpdater
from threadDownloaderEngine import DownloaderEngine
from stylesheet import TextColor
from runtimeStyleSheet import ChildItemStyleSheet, ColorScheme, MenuItemStyleSheet
from dialogs import MessageBox



class ChildItemWindow(QMainWindow, childItemWindow_.Ui_MainWindow):
    def __init__(self, parent, grandParent, entry):
        super(ChildItemWindow, self).__init__()
        try:
            self.setupUi(self)
            self.setWindowFlag(Qt.FramelessWindowHint)

            # custom message box
            self.msgBox = MessageBox()

            # stylesheet
            self.my_color_scheme = ColorScheme()
            self.my_stylesheet = ChildItemStyleSheet(self, self.my_color_scheme.dark_theme())
            self.my_stylesheet.apply_stylesheet()  # apply stylesheet to self

            self.child_timer = QBasicTimer()

            # inherited variable declaration
            self.myParent = parent
            self.myGrandParent = grandParent
            self.myEntry = entry
            self.threadController = self.myGrandParent.threadController
            self.download_video = entry['download_video']
            self.download_all = entry['download_all']
            self.format = entry['format']
            self.url = entry['url']
            self.title = entry['title']
            self.is_playlist = entry['is_playlist']
            self.playlist_index = entry['playlist_index']
            self.playlist_title = entry['playlist_title']
            self.playlist_url = entry['playlist_url']
            self.thumbnail = entry['thumbnail']
            self.status = entry['status']
            self.download_location = entry['download_location']

            # other variable declaration
            self._eta = "0:00"
            self._speed = "0 kbs"
            self._downloaded = "0 kb"
            self._size = "0 kb"
            self._percent = "0 %"

            self.generalFunction =  GeneralFunctions()
            self.my_downloader_thread_name = None  # intended to hold the thread name handling download for this item
            self.menu_item_list = MenuItemsList(self)
            self.database = VideoDatabase()
            self.status_updater = ChildStatusUpdater(self)
            self.downloader_engine = DownloaderEngine(self)
            self.download_in_progress = False

            self.error_message = ""
            self.message = ""
            self.warning_message = ""
            self.error_detected = False

            self.image_loading_error = False
            self.image_loader = None

            self.cooldown = 0
            self.buttonWarning.clicked.connect(self.display_error)

            self.updater_list = {}
            self.kickstart = False
            self.first_timer = True

            self.textColor = TextColor()

            self.busy_deleting = False

            self.initialize()
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  __init__ : {e}")
            pass

    def style_menu(self):
        try:
            style = JbadonaiStyleSheet()
            color_radial_gradient = "qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0))"
            color_primary_green = "rgb(0,255,127)"
            color_pale_white = "rgb(200,200,200)"
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] > style_menu(): {e}")

    def initialize(self):
        try:
            self.child_timer.start(200, self)
            try:
                if self.get_status() == "Downloading":
                    self.set_font_color(self.labelStatus, self.textColor.downloading_color)
                    self.start_child_timer()

                if self.get_status() == "Waiting":
                    self.set_font_color(self.labelStatus, self.textColor.waiting_color)

                if self.get_status() == "Stopped":
                    self.set_font_color(self.labelStatus, self.textColor.stopped_color)

                if self.get_status() == "Completed":
                    self.set_font_color(self.labelStatus, self.textColor.completed_color)
            except Exception as e:
                pass

            # reset progress bar
            self.progressBar.setValue(0)

            # set the video title
            #--------------------------
            if self.is_playlist is True:
                self.labelTitle.setText(f"{self.playlist_index}. {self.title}")
            else:
                self.labelTitle.setText(self.title)

            self.labelStatus.setText(self.status)
            self.message = self.status

            # highlight video or audio download indicator
            # -------------------------------------------
            if self.download_video is True:
                self.select_object(self.buttonVideo)
            else:
                self.select_object(self.buttonAudio)

            # load url image
            # -----------------
            if self.first_timer is True:
                self.image_loader = LoadImage(self)
                self.image_loader.start_loading_image()

            self.first_timer = False

            self.labelStandardStatus.setVisible(False)
            self.checkBoxChildItem.setVisible(False)

            # self.resize_screen_objects()
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] > initialize(): {e}")
            pass

    def resize_screen_objects(self):
        try:
            sh = self.generalFunction.get_screen_height()
            self.initialScreenHeight = sh


            if sh > 800:
                self.setMaximumHeight(sh / 9)
                new_height = new_width = int(self.height()/1.4)
                self.frame_image.setMaximumSize(new_width, new_height)
                self.frame_image.setMinimumSize(new_width, new_height)
                self.labelImage.setMaximumSize(new_width, new_height)
                self.labelImage.setMinimumSize(new_width, new_height)
            elif sh <= 800 and sh > 700:
                self.setMaximumHeight(sh / 9)
                new_height = new_width = int(self.height()/1.5)
                self.frame_image.setMaximumSize(new_width, new_height)
                self.frame_image.setMinimumSize(new_width, new_height)
                self.labelImage.setMaximumSize(new_width, new_height)
                self.labelImage.setMinimumSize(new_width, new_height)
            else:
                self.setMaximumHeight(sh / 7)
                new_height = new_width = int(self.height()/1.2)
                self.frame_image.setMaximumSize(new_width, new_height)
                self.frame_image.setMinimumSize(new_width, new_height)
                self.labelImage.setMaximumSize(new_width, new_height)
                self.labelImage.setMinimumSize(new_width, new_height)
            pass
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  resize_screen_object(): {e}")

    def stop_activities(self):
        try:
            self.kickstart = False
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  stop_activities() : {e}")
            pass

    def start_child_timer(self):  # needed to control starting of timer in threadDownloadController
        try:
            self.kickstart = True
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  start_child_timer()")
            pass

    def get_status(self): # needed to control starting of timer in threadDownloadController
        try:
            status = self.database.get_status(self.url)
            return status
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  get_status() : {e}")
            pass

    def interrupt(self):
        try:
            self.downloader_engine.stop()
            time.sleep(0.2)
            self.child_timer.stop()
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  interrupt() : {e}")
            pass

    def delete_me(self, prompt=True):
        try:
            self.busy_deleting = True
            remaining = self.myParent.frame_parent.layout().count()
            if prompt is True:
                # ans = QMessageBox.question(self.myGrandParent, "Delete?", f"Delete '{self.title}'",
                #                            QMessageBox.Yes | QMessageBox.No)

                self.msgBox.show_question("Delete?", f"Delete '{self.title}'")

            else:
                # ans = QMessageBox.Yes
                self.msgBox.Yes = True

            # if ans == QMessageBox.Yes:
            if self.msgBox.Yes is True:
                if self.download_in_progress is True:
                    # try to stop the download before attempting to delete
                    self.stop_activities()
                    self.interrupt()
                    time.sleep(0.2)

                if remaining > 1:
                    index = self.get_index(self.title, self.myParent.frame_parent.layout())

                    # self.myParent.frame_parent.layout().itemAt(index).widget().close()
                    self.myParent.frame_parent.layout().itemAt(index).widget().deleteLater()

                    self.database.delete_by_title(self.title)

                    self.child_timer.stop()
                    # print(self.myParent.labelTitle.text())

                    self.myParent.labelTitle.setText(f"{self.myParent.top_title}")
                    self.myParent.labelTitleTotalVideo.setText(str(remaining-1))
                else:
                    self.myParent.remove_parent_express()

                pass

            remaining = self.myParent.frame_parent.layout().count()
            if remaining <= 0:
                self.myParent.close()

            self.busy_deleting = False
        except Exception as e:
            self.busy_deleting = False
            print(f"An Error Occurred in [childItemWindow.py] >  deleteme(): {e}")
            pass

    def get_index(self, title, container):
        try:
            # self.frame_parent.layout().count()
            if container.count() > 0:
                for x in range(container.count()):
                    this_title = container.itemAt(x).widget().title
                    if str(this_title).strip().lower() == str(title).strip().lower():
                        # print(container.itemAt(x).widget().title)
                        return x
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  get_index(): \n>>{e}")

    def delete_index(self, index, container):
        try:
            def start(index):
                container.itemAt(index).widget().deleteLater()
            start(index)
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  delete_index(): \n>>{e}")

    def select_object(self, myobject: object):
        if myobject.objectName() == self.buttonWarning.objectName():
            myobject.setStyleSheet("border: 1px solid yellow; padding:5px; border-radius:15px; background-color: red;")
        else:
            myobject.setStyleSheet("border: 1px solid yellow; padding:5px; border-radius:15px; background-color: gray;")

    def deselect_object(self, myobject:object):
        myobject.setStyleSheet("border: 1px solid gray;padding:5px;background: transparent;margin: 5px 15px; ")

    def open_url_in_browser(self, url):
        try:
            webbrowser.register('chrome',
                                None,
                                webbrowser.BackgroundBrowser(
                                    "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
            webbrowser.get('chrome').open(url)
        except Exception as e:
            self.msgBox.show_information("Aborted!", "Operation Aborted! Chrome browser is required for this operation.")
            print(f"An Error Occurred in [childItemWindow.py] >  open_url_in_ browser(): {e}")

    def display_error(self):
        try:
            if self.error_message != "":
                if self.error_message.lower().__contains__('urlopen error') or \
                        self.error_message.lower().__contains__('timed out'):

                    displayMesage = "Download Stopped due to Internet connection issue. \n\nPlease Check your Internet connection and try again by righ clicking this download and select 'Start'!"
                    # QMessageBox.information(self, "Error Message", displayMesage)
                    self.msgBox.show_information("Error Message", displayMesage)
                else:
                    self.msgBox.show_information("Error Message", f"Download Stopped due to an unhandled Error  below: \n\n"
                    f" '{self.error_message}' \n\n"
                    f"Please make sure your internet connection is ok, Right click on this video and click 'Start' to try again.")

        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  display_error(): {e}")

    def set_font_color(self, myobject, color):
        myobject.setStyleSheet(f'color: {color};')

    def update_download_location(self):
        self.download_location = self.database.get_settings('default_download_location')


    def timerEvent(self, a0):
        try:
            if self.kickstart is True:
                # print(f"timer actually rurnning for : {self.title}")
                self.labelStatus.setText(self.message)

                self.download_location = self.database.get_settings('default_download_location')

                status = self.get_status()
                if status == 'Downloading':
                    if self.download_in_progress is False:
                        self.download_in_progress = True

                        # start downloader engine
                        self.downloader_engine.start_downloader_engine()
                        self.set_font_color(self.labelStatus, self.textColor.downloading_color)


                if status == "Completed":   # or status == 'Waiting' or status == "Stopped":
                    self.cooldown += 1
                    if self.cooldown >= 10:
                        self.labelStatus.setText(status)
                        self.child_timer.stop()
                        self.kickstart = False
                        self.set_font_color(self.labelStatus, self.textColor.completed_color)

                if status == 'Waiting':
                    # if self.download_in_progress is True:
                    #     self.download_in_progress = False
                    self.labelStatus.setText(status)
                    self.kickstart = False
                    # self.status_updater.stop()
                    print('Kick stater and updater stopped')
                    # if status == 'Waiting':
                    self.set_font_color(self.labelStatus, self.textColor.waiting_color)

                if status == "Stopped":
                    # if self.download_in_progress is True:
                    #     self.download_in_progress = False
                    self.labelStatus.setText(status)
                    # self.kickstart = False
                    # self.status_updater.stop()
                    # print('Kick stater and updater stopped')
                    # if status == 'Waiting':
                    #     self.set_font_color(self.labelStatus, self.textColor.waiting_color)
                    # else:
                    self.set_font_color(self.labelStatus, self.textColor.stopped_color)
            else:


                pass
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >  timer_event(): {e}\n"
                  f">>:{self.title}" )

        pass

    def contextMenuEvent(self, event):
        try:
            style = MenuItemStyleSheet()
            menu = QMenu(self)  # create an instance of the menu

            # menu.setStyleSheet(Stylesheet().menuDarkTheme)  # apply custom sytle to the menu
            menu.setStyleSheet(style.context_menu_stylesheet())  # apply custom sytle to the menu

            menu_list = self.menu_item_list.auto_menu()  # get the content of the menu
            # loop through the menu item list to apply icon and display them.
            for m in menu_list:
                menu_list[m] = eval(str(menu_list[m]))

                if str(m).__contains__('separator'):
                    menu_list[m]['name'] = menu.addSeparator()
                else:
                    menu_list[m]['name'] = menu.addAction(menu_list[m]['text'])
                    menu_list[m]['name'].setIcon(QIcon(menu_list[m]['icon']))

            action = menu.exec_(self.mapToGlobal(event.pos()))

            for m in menu_list:
                if action == menu_list[m]['name']:
                    #   get the function name to be executed and run / evaluate it.
                    eval(f"self.menu_item_list.{menu_list[m]['function_name']}")
                    break

        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >   contextMenuEvent(): \n>>{e}")




