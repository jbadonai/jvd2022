from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QSizeGrip,QWidget, QMenu, \
    QMessageBox, QFileDialog, QVBoxLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QProcess, QEvent, QBasicTimer
from PyQt5.QtGui import QColor, QIcon
import random
import yt_dlp as youtube_dl     #yt-dlp-2022.1.21, yt-dlp 2022.3.8.2
import time

from ui import parentItemWindow_
# import parentItemWindow_
from childItemWindow import ChildItemWindow
# from stylesheet import Stylesheet
from threadLoadChildrenItems import LoadChildrenItems
from videoDatabase import VideoDatabase
from generalFunctions import GeneralFunctions
from threadRefreshPlaylistEntries import RefreshPlaylistEntries
from threadAnimations import ObjectBlinker, ObjectHighlighter
from runtimeStyleSheet import ParentItemStyleSheet, ColorScheme
from runtimeStyleSheet import  MenuItemStyleSheet
from menuItemsList import ParentMenuItemsList
from dialogs import MessageBox
from exceptionList import *

class ParentItemWindow(QMainWindow, parentItemWindow_.Ui_MainWindow):

    def __init__(self, parent, entries, common_title):
        super(ParentItemWindow, self).__init__()
        print("[Debug] \tSetting up Parent Item window: ParentItemWindow__init__")
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.parent = parent

        # custom messagebox
        self.msgBox = MessageBox()


        # stylesheet
        self.my_color_scheme = ColorScheme()
        self.my_stylesheet = ParentItemStyleSheet(self, self.my_color_scheme.dark_theme())
        self.my_stylesheet.apply_stylesheet()  # apply stylesheet to self

        self.data = entries
        self.database = VideoDatabase()
        self.threadController = self.parent.threadController
        print(f"[Debug] \tInitializing children loader with data({len(self.data)}) ")
        # print(self.data)
        self.children_loader = LoadChildrenItems(parent= self, grandparent=self.parent, data=self.data)

        # configure a layout
        self.childLayout = QVBoxLayout()
        self.buttonShowHideDetails.clicked.connect(self.showHide)
        self.frame_parent.setLayout(self.childLayout)

        self.buttonCloseParentItem.clicked.connect(self.remove_parent)
        self.buttonRefreshPlaylist.clicked.connect(self.refresh_playlist)

        self.tit = ""
        self.isParentPlaylist = None
        self.top_title = None
        self.playlistURL = self.data[0]['playlist_url']
        self.downloadVideo = self.data[0]['download_video']
        self.downloadLocation = self.data[0]['download_location']
        self.downloadFormat = self.data[0]['format']
        self.playlistTitle = self.data[0]['playlist_title']

        self.generalFunction = GeneralFunctions()

        self.parent.blinkerList[self.playlistTitle] = ObjectBlinker(self, self.buttonRefreshPlaylist, 0.2)
        self.refreshBusy = False

        self.download_entries = []  # used for refresh pupose only

        if self.data[0]['is_playlist'] is True:
            self.top_title = self.data[0]['playlist_title']
            self.labelTitle.setText(f"{self.data[0]['playlist_title']}".upper())
            self.labelTitleTotalVideo.setText(str(len(self.data)))

            self.tit = self.data[0]['playlist_title']
            self.isParentPlaylist = True
            self.frame_refresh_playlist.setVisible(True)
            self.frame_status.setVisible(False)

        else:
            self.top_title = self.shorten(self.data[0]['title'], 30)
            self.labelTitle.setText(self.shorten(str(self.data[0]['title']), 30))
            self.tit =  self.data[0]['title']
            self.isParentPlaylist = False
            self.frame_refresh_playlist.setVisible(False)
            self.frame_playlist.setVisible(False)
            self.frame_title_playlist__count.setVisible(False)
            self.frame_statusdetails.setVisible(False)


        # self.add_child_items()
        self.parentTimer = QBasicTimer()

        self.initialScreenSize = self.generalFunction.get_screen_size()

        self.initialize()

    def initialize(self):
        print("[Debug] \tParent window: Initialize")
        self.parentTimer.start(1000, self)

        self.frame_parent.setVisible(False)
        self.buttonShowHideDetails.setIcon(QIcon(":/white icons/White icon/chevron-down.svg"))

        self.add_child_items()
        self.frame_title_playlist__count.setVisible(False)

        self.menu_item_list = ParentMenuItemsList(self)

    def refresh_playlist(self):
        '''
        Refresh playlist to detect newly added video to the playlist
        '''
        # sender = self.sender().objectName()
        # self.msgBox.show_information("Sender", f"{sender}")

        if self.refreshBusy is False:
            self.refreshBusy = True
            self.download_entries.clear()

            self.buttonRefreshPlaylist.setIcon(QIcon(':/blue icons/blue icon/refresh-ccw.svg'))
            self.parent.blinkerList[self.playlistTitle].start_blinking()

            refresher = RefreshPlaylistEntries(self, self.playlistURL)
            refresher.refresh()
            pass
        else:
            print("Busy!")
            # self.msgBox.show_information("busy", "Busy!")

    def load_refreshed_data(self, data):
        # should be called from the thread when data extraction is completed

        self.download_entries.extend(data)
        self.update_download_entries()

        self.generalFunction.run_function(self.parent.save_entry, False, self.download_entries)

        children_refresher_loader = LoadChildrenItems(parent=self, grandparent=self.parent, data=self.download_entries)
        children_refresher_loader.start_loading_children_items()

        self.buttonRefreshPlaylist.setIcon(QIcon(':/white icons/White icon/refresh-ccw.svg'))
        total = len(self.download_entries)

        self.refreshBusy = False
        self.parent.blinkerList[self.playlistTitle].stop_blinking()



        if total > 0:
            old = int(self.labelTitleTotalVideo.text())
            self.labelTitleTotalVideo.setText(str(old + total))
            # QMessageBox.information(self, 'Refresh Completed!', f"Refresh Completed for {self.playlistTitle}. {total} new link detected and has been added to the playlist download list.")
            self.msgBox.show_information('Refresh Completed!', f"Refresh Completed for {self.playlistTitle}. {total} new link detected and has been added to the playlist download list.")
        else:
            # QMessageBox.information(self, "Refresh Completed!", f"Playlist is up to date! No new link found for {self.playlistTitle}")
            self.msgBox.show_information("Refresh Completed!", f"Playlist is up to date! No new link found for {self.playlistTitle}")

    def update_download_entries(self):
        for index, entry in enumerate(self.download_entries):
            self.download_entries[index]['download_video'] = self.downloadVideo
            self.download_entries[index]['format'] = self.downloadFormat
            self.download_entries[index]['status'] = "Waiting"
            self.download_entries[index]['download_all'] = True
            self.download_entries[index]['download_location'] = self.downloadLocation

    def add_child_items(self):
        try:
            print("[Debug] \tLoading of Children items commenced in thread")
            self.children_loader.start_loading_children_items()

        except Exception as e:
            print(e)

    def showHide(self):
        # print(self.frame_top.height())
        if self.frame_parent.isVisible():
            self.frame_parent.setVisible(False)

            self.buttonShowHideDetails.setIcon(QIcon(":/white icons/White icon/chevron-down.svg"))
        else:
            self.frame_parent.setVisible(True)
            self.buttonShowHideDetails.setIcon(QIcon(":/white icons/White icon/chevron-up.svg"))

    def get_actual_count(self):
        counter = 0
        for y in range(self.frame_parent.layout().count()):
            child_item = self.frame_parent.layout().itemAt(y).widget()
            try:
                title = child_item.title
                print(f"title: {title}")
                counter += 1
            except:
                continue

        return counter

    def shorten(self, text, no_of_char):
        if len(text) > no_of_char:
            return f"{str(text)[:no_of_char].upper().strip()}..."
        else:
            return text

    def remove_parent(self):

        total_children = self.frame_parent.layout().count()
        # total_children = self.get_actual_count()

        if self.isParentPlaylist:
            # ans = QMessageBox.question(self.parent, "Remove Playlist!", f"Remove  the playlist ' {self.shorten(self.labelTitle.text().split('-')[-1], 20)}'  from the download list? \n\n"
            # f"All the {total_children} download items will be removed from the download list!", QMessageBox.Yes | QMessageBox.No)
            #
            self.msgBox.show_question("Remove Playlist!", f"Remove  the playlist ' {self.shorten(self.labelTitle.text().split('-')[-1], 20)}'  from the download list? \n\n"
            f"All the {total_children} download items will be removed from the download list!")
        else:
            # ans = QMessageBox.question(self.parent, "Remove Download", f"Remove [ '{self.shorten(self.labelTitle.text(), 20) }' ] from the download list", QMessageBox.Yes | QMessageBox.No)
            self.msgBox.show_question("Remove Download", f"Remove [ '{self.shorten(self.labelTitle.text(), 20) }' ] from the download list")

        # if ans == QMessageBox.Yes:
        if self.msgBox.Yes is True:
            if self.frame_parent.isVisible() is False:
                self.frame_parent.setVisible(True)

            GeneralFunctions().run_function(self.delete_children)
        pass

    def remove_parent_express(self):
        if self.frame_parent.isVisible() is False:
            self.frame_parent.setVisible(True)

        GeneralFunctions().run_function(self.delete_children)


        pass

    def delete_children(self):
        for y in range(self.frame_parent.layout().count()):
            child_item = self.frame_parent.layout().itemAt(y).widget()
            item_url = child_item.url

            if child_item.download_in_progress is True:
                # try to stop the download before attempting to delete
                child_item.stop_activities()
                child_item.interrupt()
                time.sleep(0.2)

            self.database.delete_by_url(item_url)
            child_item.close()
            time.sleep(0.1)

        time.sleep(0.1)
        self.close()

    def stop_all(self):
        for y in range(self.frame_parent.layout().count()):
            child_item = self.frame_parent.layout().itemAt(y).widget()
            item_url = child_item.url

            if child_item.download_in_progress is True:
                # try to stop the download before attempting to delete
                child_item.stop_activities()
                child_item.interrupt()
                time.sleep(0.2)

            self.database.set_status(item_url, 'Stopped')
            child_item.labelStatus.setText("Stopped")
            time.sleep(0.1)

        time.sleep(0.1)

    def check_status(self):
        try:
            errorCount = 0
            completed = 0
            downloading = 0
            waiting = 0
            stopped = 0
            total = 0
            data = {}

            for y in range(self.frame_parent.layout().count()):
                child_item = self.frame_parent.layout().itemAt(y).widget()
                status = child_item.labelStatus.text()
                if str(status).lower() == 'completed':
                    completed += 1
                if str(status).lower().__contains__('downloading') :
                    downloading += 1
                if str(status).lower() == 'waiting':
                    waiting += 1
                if str(status).lower() == 'stopped':
                    stopped += 1
                if child_item.error_message != "":
                    errorCount += 1
                total += 1

            data['completed'] = completed
            data['downloading'] = downloading
            data['waiting'] = waiting
            data['stopped'] = stopped
            data['errorCount'] = errorCount
            data['total'] = total

            return data
        except Exception as e:
            print(f"An Error Occurred in check status: {e}")
            pass

    def timerEvent(self, a0):
        try:
            # sh = self.generalFunction.get_screen_size()
            # if sh.height != self.initialScreenSize.height or sh.width != self.initialScreenSize.width:
            #     if sh.height >= 800:
            #         self.frame_top.setMinimumHeight(int(sh.height/14))
            #     else:
            #         self.frame_top.setMinimumHeight(int(sh.height/10))

            data = self.check_status()
            status = "..."

            if data['completed'] == data['total']:
                self.labelParentStatus.setText("Completed!")
                # self.parentTimer.stop()

            if self.isParentPlaylist is True:
                # status = f"TOTAL: [{data['total']}]  |  " \
                #     f"COMPLETED: [{data['completed']}]  |  " \
                #     f"DOWNLOADING: [{data['downloading']}]  |  " \
                #     f"STOPPED: [{data['stopped']}]  |  " \
                #     f"WAITING: [{data['waiting']}]  |  " \
                #     f"ERROR: [{data['errorCount']}]"

                self.textTotal.setText(str(data['total']))
                self.textCompleted.setText(str(data['completed']))
                self.textDownloading.setText(str(data['downloading']))
                self.textStopped.setText(str(data['stopped']))
                self.textWaiting.setText(str(data['waiting']))
                self.textError.setText(str(data['stopped']))
            else:
                child_item = self.frame_parent.layout().itemAt(0).widget()

                if int(data['downloading']) > 0:
                    status = f"Downloading [ {child_item.progressBar.value()}% ]"

                if int(data['stopped']) > 0:
                    status = "Download Stopped"

                if int(data['waiting']) > 0:
                    status = "Waiting..."

                if int(data['errorCount']) > 0:
                    status = "An Error Occurred. Click on warning button to see details"

                if int(data['completed']) > 0:
                            status = "Completed"



            self.labelParentStatus.setText(status)
            pass
        except Exception as e:
            print(f"An Error Occurred in parent timer event: {e}")

    def contextMenuEvent(self, event):
        try:
            if self.isParentPlaylist is False:
                raise SoftLandingException

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
        except SoftLandingException:
            pass
        except Exception as e:
            print(f"An Error Occurred in [childItemWindow.py] >   contextMenuEvent(): \n>>{e}")





