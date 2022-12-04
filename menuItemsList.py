import os
from PyQt5.QtWidgets import  QMessageBox
import subprocess
import pyperclip as clipboard
from videoDatabase import VideoDatabase
import time
from exceptionList import  *
from generalFunctions import GeneralFunctions


class MenuItemsList():
    def __init__(self, myparent=None):
        self.my_parent = myparent  # child item window
        self.selected_data = None

    def get_menu(self):
        try:
            if self.my_parent is not None:
                if self.my_parent.database.get_status(self.my_parent.url) == 'completed':
                    key = "Restart"
                    value = "{'name': '','text': 'Restart', 'icon': ':/white icons/White icon/play.svg','function_name': 'restart()'}"
                    selected_data = (key, value)
                    return selected_data
                else:
                    key = "Start"
                    value = "{'name': '','text': 'Start', 'icon': ':/white icons/White icon/play.svg','function_name': 'restart()'}"
                    selected_data = (key, value)
                    return selected_data
            else:
                key = "Start"
                value = "{'name': '','text': 'Start', 'icon': ':/white icons/White icon/play.svg','function_name': 'restart()'}"
                selected_data = (key, value)
                return selected_data
        except Exception as e:
            print(f"an error occurred in MenuItemList > get_menu(): \n>>>>{e}")

    def auto_menu(self):

        self.selected_data =  self.get_menu()

        item_menu_list = {

            'Copy URL': {'name': '',
                         'text': 'Copy URL',
                         'icon': ':/white icons/White icon/copy.svg',
                         'function_name': 'copy_url()'},

            'Copy playlist URL': {'name': '',
                                  'text': 'Copy playlist URL',
                                  'icon': ':/white icons/White icon/copy.svg',
                                  'function_name': 'copy_playlist_url()'},

            'goto URL': {'name': '',
                                  'text': 'Go to URL',
                                  'icon': ':/white icons/White icon/globe.svg',
                                  'function_name': 'goto_url()'},

            'separator1': {'name': '',
                           'text': 'separator',
                           'icon': '',
                           'function_name': ''},

            f'{self.selected_data[0]}': f'{self.selected_data[1]}' ,

            'Stop': {'name': '',
                     'text': 'Stop',
                     'icon': ':/white icons/White icon/stop-circle.svg',
                     'function_name': 'stop_download()'},

            'separator2': {'name': '',
                           'text': 'separator',
                           'icon': '',
                           'function_name': ''},

            'Open in Explorer': {'name': '',
                                 'text': 'Open in Explorer',
                                 'icon': ':/white icons/White icon/folder.svg',
                                 'function_name': 'open_in_explorer()'},

            'separator3': {'name': '',
                           'text': 'separator',
                           'icon': '',
                           'function_name': ''},

            'Delete': {'name': '',
                       'text': f'Remove "{self.my_parent.title[:20]}..." \nfrom Download list',
                       'icon': ':/white icons/White icon/trash-2.svg',
                       'function_name': 'delete_selected()'}
        }

        return item_menu_list

    # item window menu function starts here
    def copy_url(self):
        clipboard.copy(self.my_parent.url)
        QMessageBox.information(self.my_parent, 'URL copied', 'ULR copied to the clipboard')

    def copy_playlist_url(self):
        clipboard.copy(self.my_parent.playlist_url)
        QMessageBox.information(self.my_parent, 'URL copied', 'Playlist URL copied to the clipboard')
        # print('copying playlist url...')

    def goto_url(self):
        self.my_parent.open_url_in_browser(self.my_parent.url)
        pass

    def restart(self):
        if self.my_parent.database.get_status(self.my_parent.url) != 'Completed' and self.my_parent.database.get_status(self.my_parent.url) != 'Downloading':
            self.my_parent.database.set_status(self.my_parent.url, 'Waiting')
            self.my_parent.labelStatus.setText('Waiting')
            self.my_parent.set_font_color(self.my_parent.labelStatus, 'rgb(240, 217, 219)')
            # self.labelStatus.setText(self.message)

    def stop_download(self):
        if self.my_parent.database.get_status(self.my_parent.url) != 'Completed':
            self.my_parent.database.set_status(self.my_parent.url, 'Stopped')
            # self.my_parent.stop_activities()
            # self.my_parent.labelStatus.setText('Stopped')

    def open_in_explorer(self):
        try:
            # path = os.path.normpath(f"{self.my_parent.myself.default_download_location}\\")

            location = VideoDatabase().get_download_location_by_url(self.my_parent.url)
            # print(f"Location: {location}")

            # self.my_parent.update_download_location()
            # path = os.path.normpath(f"{self.my_parent.download_location}\\")
            path = os.path.normpath(f"{location}\\")
            print(path)

            if self.my_parent.is_playlist is True:
                path = os.path.join(path, self.my_parent.playlist_title)

            filename = None
            nameToFind = self.my_parent.title
            for root, dirs, files in os.walk(path):
                for file in files:
                    if str(file).__contains__(nameToFind):
                        filename = file
                        break

            if filename is not None:
                fullFilePath = os.path.join(path, filename)
                print(fullFilePath)

                # os.popen(self.downloadLocation)
                # subprocess.Popen(f'explorer {self.downloadLocation}')
                if os.path.exists(fullFilePath):
                    subprocess.Popen(rf'explorer /select,"{fullFilePath}"')
                else:

                    QMessageBox.information(self.my_parent, 'File not found', 'File not found in the download directory!'
                                                                              ' \nPossibly the file has been moved or file '
                                                                              'download is yet to be completed.\n\n'
                                                                              'Please restart the download if not '
                                                                              'in progress.')
                    # subprocess.getoutput(f'start {path}')
            else:
                QMessageBox.information(self.my_parent, "File not Found", "File not found. File or Folder must have been moved or renamed.")

        except Exception as e:

            print(e)
            QMessageBox.information(self.my_parent, 'File location not known', 'File location not know.'
                                                                     ' Please restart the download and check again '
                                                                               'when download is completed.')

    def delete_selected(self):
        try:
            self.my_parent.delete_me()

        except Exception as e:
            print(f"An error occurred in menuItemslist > delete_selected: {e}")

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
            print(f"An error occurred in Common > ItemWindow > get_index(): \n>>{e}")

    def delete_index(self, index, container):
        try:
            def start(index):
                container.itemAt(index).widget().deleteLater()

            # GeneralFunctions.run_function(start, False, index)
            start(index)
        except Exception as e:
            print(f"An error occurred in Common > ItemWindow > delete_index(): \n>>{e}")


class ParentMenuItemsList():
    def __init__(self, myparent=None):
        self.my_parent = myparent  # child item window
        self.selected_data = None

    def auto_menu(self):
        item_menu_list = {

            'Stop All': {'name': '',
                         'text': 'Stop All',
                         'icon': ':/white icons/White icon/stop-circle.svg',
                         'function_name': 'stop_all()'},

            'Start All': {'name': '',
                                  'text': 'Start All',
                                  'icon': ':/white icons/White icon/play-circle.svg',
                                  'function_name': 'start_all()'},

            'separator1': {'name': '',
                           'text': 'separator',
                           'icon': '',
                           'function_name': ''},

            'Resolve All Errors': {'name': '',
                                  'text': 'Resolve All Errors',
                                  'icon': ':/white icons/White icon/alert-triangle.svg',
                                  'function_name': 'resolve_all_errors()'},

            'separator2': {'name': '',
                           'text': 'separator',
                           'icon': '',
                           'function_name': ''},


            'Remove completed from download list': {'name': '',
                     'text': 'Remove completed from download list',
                     'icon': ':/white icons/White icon/trash-2.svg',
                     'function_name': 'remove_completed()'},

        }

        return item_menu_list

    # item window menu function starts here
    def stop_all(self):
        try:
            for y in range(self.my_parent.frame_parent.layout().count()):
                child_item = self.my_parent.frame_parent.layout().itemAt(y).widget()
                item_url = child_item.url

                if VideoDatabase().get_status(item_url) != 'Completed':
                    VideoDatabase().set_status(item_url, 'Stopped')

                time.sleep(0.1)

        except Exception as e:
            print(f"An Error Occurred in [menuItemsList.py] > ParentMenuitemsList > stop_all(): {e}")

    def start_all(self):
        try:
            for y in range(self.my_parent.frame_parent.layout().count()):
                child_item = self.my_parent.frame_parent.layout().itemAt(y).widget()
                item_url = child_item.url

                if VideoDatabase().get_status(item_url) != 'Completed':
                    VideoDatabase().set_status(item_url, 'Waiting')

                time.sleep(0.1)

        except Exception as e:
            print(f"An Error Occurred in [menuItemsList.py] > ParentMenuitemsList > start_all(): {e}")
        pass

    def resolve_all_errors(self):
        try:
            for y in range(self.my_parent.frame_parent.layout().count()):
                child_item = self.my_parent.frame_parent.layout().itemAt(y).widget()
                item_url = child_item.url

                if child_item.error_detected is True:
                    print('detected..............')
                    VideoDatabase().set_status(item_url, 'Waiting')
                    child_item.error_detected = False

                time.sleep(0.1)
        except StoppedByUserException:
            pass
        except Exception as e:
            print(f"An Error Occurred in [menuItemsList.py] > ParentMenuitemsList > remove_completed(): {e}")


        pass

    def remove_completed(self):
        try:
            ans = QMessageBox.question(self.my_parent, "Remove Completed!", "Remove all completed downloads from the download list?", QMessageBox.Yes | QMessageBox.No)
            if ans == QMessageBox.No:
                raise StoppedByUserException

            for y in range(self.my_parent.frame_parent.layout().count()):
                child_item = self.my_parent.frame_parent.layout().itemAt(y).widget()
                item_url = child_item.url

                if VideoDatabase().get_status(item_url) == 'Completed':
                    # child_item.delete_me(prompt=False)
                    # child_item.hide()
                    GeneralFunctions().run_function(child_item.delete_me,False, False)

                time.sleep(0.1)
        except StoppedByUserException:
            pass
        except Exception as e:
            print(f"An Error Occurred in [menuItemsList.py] > ParentMenuitemsList > remove_completed(): {e}")

