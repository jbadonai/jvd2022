from PyQt5 import QtCore
from videoDatabase import VideoDatabase
from exceptionList import *
from generalFunctions import GeneralFunctions
import time


class DownloadController():
    def __init__(self, parent):
        super(DownloadController, self).__init__()
        self.database = VideoDatabase()

        self.max_download = int(self.database.get_settings('max_download'))
        self.parent = parent
        self.threadController = self.parent.threadController

    def start_download_controller(self):
        def download_controller_connector(data):
            try:
                pass
            except Exception as e:
                print(f"An Error Occurred in DownloadController > download controller connector: {e}")

        try:
            self.threadController['download controller'] = DownloadControllerThread(self.parent)
            self.threadController['download controller'].start()
            self.threadController['download controller'].any_signal.connect(download_controller_connector)
        except Exception as e:
            print(f"An Error occurred in downloadController > start download controller: {e}")


class DownloadControllerThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent):
        super(DownloadControllerThread, self).__init__()
        self.myself = parent

    def stop(self):
        self.requestInterruption()

    def activate_timer(self, url):
        try:
            # print(f">>>: Detecting child item to activate...")
            for x in range(self.myself.parentScrollAreaWidgetContents.layout().count()):
                item = self.myself.parentScrollAreaWidgetContents.layout().itemAt(x).widget()
                no = item.frame_parent.layout().count()
                for y in range(item.frame_parent.layout().count()):
                    child_item = item.frame_parent.layout().itemAt(y).widget()
                    item_url = child_item.url
                    if item_url == url:
                        # print(f">>>: Activating child timer...")
                        # child_item.start_child_timer()
                        child_item.initialize()

        except Exception as e:
            print(f"An Error Occurred in DownloadControllerThread > activate timer: {e}")

    def activate_timer_bak(self, url):
        print(f'activating timer for {url}..............')
        try:
            for win in self.myself.children_window_handle_list:
                # print("winURL: ", win.url)
                if win.url == url:
                    print(f"found: {win.url}")
                    win.start_child_timer()

        except Exception as e:
            print(f"An Error Occurred in DownloadControllerThread > activate timer: {e}")

    def start_downloading_next(self):
        try:
            # print(f">>>: Deciding which url to start downloading...")
            all_entries = VideoDatabase().get_all_video_data()
            for entry in all_entries:
                entry = GeneralFunctions().database_list_to_dictionary(entry)
                status = entry['status']
                if status == "Waiting":
                    VideoDatabase().set_status(entry['url'], 'Downloading')
                    # print(f">>>: {entry['url']} has been picked to start next. Activating the timer for the url")
                    self.activate_timer(entry['url'])
                    break

            pass
        except Exception as e:
            print(f"An Error occurred in DownloadControllerThread > start downloading next: {e}")

    def stop_last_downloading(self):
        try:
            data = VideoDatabase().get_all_entries_by_status("Downloading")
            lastData = data[-1]
            lastData = GeneralFunctions().database_list_to_dictionary(lastData)

            VideoDatabase().set_status(lastData['url'], "Waiting")
            pass

        except Exception as e:
            print(f"An Error Occurred in DownloadControllerThread > stop last downloading: {e}")

    def run(self):
        try:
            if self.isInterruptionRequested():
                raise StoppedByUserException

            print(f">>>: Waiting for all data to be loaded...")
            while True:
                if self.myself.data_loading_completed is True:
                    break
                time.sleep(0.2)

            print(f">>>: All data loaded. Starting download controller...")
            while True:
                if self.isInterruptionRequested():
                    raise StoppedByUserException

                max_download = int(VideoDatabase().get_settings('max_download'))
                download_in_progress_total = int(VideoDatabase().get_total_by_status("Downloading"))
                total_video = int(VideoDatabase().get_total_number())

                if total_video > 0:
                    if download_in_progress_total < max_download:
                        # print(f">>>: staring next download activated.....")
                        self.start_downloading_next()

                    if download_in_progress_total > max_download:
                        print(f">>>: stopping last download activated....")
                        self.stop_last_downloading()

                time.sleep(1)

        except StoppedByUserException:
            pass
        except Exception as e:
            print(f"An Error occurred in Download controller thread > run: {e}")
