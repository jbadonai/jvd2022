from PyQt5 import QtCore
from exceptionList import *
import time


class ChildStatusUpdater():
    def __init__(self, parent):
        self.parent = parent
        self.threadController = self.parent.threadController

    def stop(self):
        self.threadController[f'{self.parent.title}'].stop()
        pass

    def start_updating_child_status(self):

        def status_updater_connector(data):
            try:
                status = data['status']
                self.parent.labelStandardStatus.setText(status)

                pass
            except Exception as e:
                print(f"An Error Occurred in ChildStatusUpdater > status updater connector: {e}")
            pass

        try:
            self.threadController[f'{self.parent.title}'] = ChildStatusUpdaterThread(self.parent)
            self.threadController[f'{self.parent.title}'].start()
            self.threadController[f'{self.parent.title}'].any_signal.connect(status_updater_connector)
        except Exception as e:
            print(f"An Error Occurred in ChildStatusUpdater > start updating child status: {e}")


class ChildStatusUpdaterThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent):
        super(ChildStatusUpdaterThread, self).__init__()
        self.myself = parent
        self.parent = parent
        self.data_to_emit = {}

    def stop(self):
        self.requestInterruption()

    def action(self):
        try:
            self.parent.labelStatus.setText(self.parent.message)

            self.parent.download_location = self.parent.database.get_settings('default_download_location')

            status = self.parent.get_status()
            if status == 'Downloading':
                if self.parent.download_in_progress is False:
                    self.parent.download_in_progress = True

                    # start downloader engine
                    self.parent.downloader_engine.start_downloader_engine()

            if status == "Completed":  # or status == 'Waiting' or status == "Stopped":
                self.parent.labelStatus.setText(status)

        except Exception as e:
            print(f"An Error Occurred in ChildstatusUpdaterThread > action. :{e}")

    def run(self):
        try:
            status = self.myself.database.get_status(self.myself.url)
            if self.isInterruptionRequested():
                raise StoppedByUserException

            while True:
                status = self.myself.database.get_status(self.myself.url)
                if self.isInterruptionRequested() or status == "Completed":
                    self.data_to_emit['status'] = status
                    self.any_signal.emit(self.data_to_emit)
                    time.sleep(1)
                    raise StoppedByUserException

                # update status display on the item window
                self.data_to_emit['status'] = status
                self.any_signal.emit(self.data_to_emit)
                time.sleep(0.2)
                
        except StoppedByUserException:
            pass

        except Exception as e:
            print(f"An Error Occurred in ChildStatusUpdaterThread > run : {e}")
