from PyQt5 import QtCore
import time
addDownloadEmergencyStop = False
global_inner_error_message = None
import  random

from generalFunctions import GeneralFunctions
from videoDatabase import VideoDatabase
from exceptionList import *


class LoadDataFromDB():
    def __init__(self, myself):
        self.my_self = myself

        self.database = myself.database
        self.threadController = myself.threadController
        self.functions = GeneralFunctions()
        self.total = 0
        self.counter = 1

    def load_entries(self):
        """Loads all Entries from the database """
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

    def start_loading(self):
        self.my_self.message = "loading commenced...."
        self.total = self.database.get_total_number()
        self.counter = 1

        def loading_connector(data):
            if data['completed'] is False:
                download_entries = data['entries']
                print(f"[Debug] \tAdding content({len(download_entries)}) to Parent Item")
                self.my_self.add_parent_item("", download_entries)
            else:
                # self.my_self.parentScrollAreaWidgetContents.setVisible(True)
                # self.my_self.data_loading_completed = True
                pass

        try:
            testName = random.randint(1111111, 9999999)
            self.threadController[f"loadData-{testName}"] = LoadDataFromDatabaseThread(self.my_self)
            self.threadController[f"loadData-{testName}"].start()
            self.threadController[f"loadData-{testName}"].any_signal.connect(loading_connector)

        except Exception as e:
            print(f"An Error occurred in boot > LoadDataFromDB :>>>\n{e}")


class LoadDataFromDatabaseThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self,  parent=None):
        super(LoadDataFromDatabaseThread, self).__init__(parent)
        try:
            # self.is_running = False
            self.general_function = GeneralFunctions()
            self.database = VideoDatabase()
            self.parent = parent
            self.data_to_emit = {}

        except Exception as e:
            print(f"An Error occurred in  LoadDataFromDatabaseThread > Init(): \n >>>{e}")

    def stop(self):
        try:
            ''' stops the thread '''
            # self.is_running = False
            # self.terminate()
            self.requestInterruption()

        except Exception as e:
            print(f"An Error occurred in Common > AddDownloadItemsThread > stop(): \n >>>{e}")

    def scan_database(self):
        '''
        CHECK EVERY ITEM IN THE DATABASE:
        extract the title and playlist status
        returns list of tuple(title, isPlaylist)  of every element in the database
        '''

        all_data = self.database.get_all_video_data()
        selected = []
        for data in all_data:
            item = self.general_function.database_list_to_dictionary(data)
            content = None
            if bool(item['is_playlist']) is True:
                title = item['playlist_title']
                isPlaylist = True
                content = (title,isPlaylist)
            else:
                title = item['title']
                isPlaylist = False
                content = (title, isPlaylist)

            if content not in selected:
                selected.append(content)

        return selected

    def convert_list_to_dictionary(self, list):
        final =[]
        for data in list:
            ans = self.general_function.database_list_to_dictionary(data)
            final.append(ans)

        return final
        pass

    def run(self):
        try:
            if self.isInterruptionRequested() is True:
                raise StoppedByUserException

            self.data_to_emit['completed'] = False
            self.data_to_emit['interrupted'] = False

            # return every element in database in a list of tuple(title, isPlaylist) and store it in data
            print("[Debug] Scanning the Database")
            data = self.scan_database()

            print("[Debug] Extracting Content of each items in the download list")
            for index, d in enumerate(data):
                if self.isInterruptionRequested() is True:
                    raise StoppedByUserException

                if d[1] is True:    # if playlist
                    # get all data in the database with the same playlist title
                    item = self.database.get_all_entries_by_playlist_title(d[0])
                    item = self.convert_list_to_dictionary(item)
                else:   # non playlist
                    # get all data in the database with title
                    item = self.database.get_all_entries_by_title(d[0])
                    item = self.convert_list_to_dictionary(item)

                self.data_to_emit['entries'] = item
                self.any_signal.emit(self.data_to_emit)
                print(f"[Debug] \t{index + 1} -- Total content: {len(item)}")
                time.sleep(0.3)

            self.data_to_emit['completed'] = True
            self.any_signal.emit(self.data_to_emit)
            time.sleep(0.3)

        except StoppedByUserException:
            self.data_to_emit['interrupted'] = True
            pass

        except Exception as e:
            print(f"An Error Occurred in LoadDataFromDatabaseThread > run : {e}")
        pass
