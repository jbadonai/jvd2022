from PyQt5 import QtCore
import time
addDownloadEmergencyStop = False
global_inner_error_message = None
from exceptionList import *


class AddNewDownloadItems():
    def __init__(self, parent):
        super(AddNewDownloadItems, self).__init__()
        self.parent = parent
        self.threadController = self.parent.threadController
        self.win_list = {}

    def start_adding_new_items(self, entries):

        def add_new_items_loader_connector(data):
            try:
                entry = data['entry']
                self.parent.add_parent_item("", entry)
            except Exception as e:
                print(f"An Error Occurred in Add new download items > children items loader connector: {e}")

        try:
            self.threadController[f"add new entry"] = AddNewItemsThread(entries)
            self.threadController[f"add new entry"].start()
            self.threadController[f"add new entry"].any_signal.connect(add_new_items_loader_connector)
        except Exception as e:
            print(f"An Error Occurred in Add new download items > start loading children items: {e}")


class AddNewItemsThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, entries):
        super(AddNewItemsThread, self).__init__()
        self.entries = entries
        self.data_to_emit = {}

    def stop(self):
        self.requestInterruption()

    def run(self):
        try:
            self.data_to_emit['entry'] = self.entries
            self.any_signal.emit(self.data_to_emit)
            time.sleep(0.1)

        except StoppedByUserException:
            print("stopped by user")
        except Exception as e:
            print(f"An Error Occurred in add new item thread > run: {e}")
        pass
