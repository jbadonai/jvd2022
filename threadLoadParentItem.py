from PyQt5 import QtCore
import time
addDownloadEmergencyStop = False
global_inner_error_message = None
import random
from exceptionList import *
from childItemWindow import ChildItemWindow
from parentItemWindow import ParentItemWindow
from videoDatabase import VideoDatabase


class LoadParentItems():
    def __init__(self, myself):
        super(LoadParentItems, self).__init__()
        self.myself = myself
        self.threadController = self.myself.threadController
        self.win_list = {}

    def start_loading_parent_items(self, entries, common_title):

        def parent_items_loader_connector(data):
            try:
                entry = data['entry']

                temp = f"parent window -  {random.randint(5555, 9999)}"
                print(f"[Debug] \tSending Data to Parent Window to Handle. Total data sent: {len(entry)}")
                self.win_list[temp] = ParentItemWindow(parent=self.myself, entries=entry, common_title=common_title)
                self.myself.parentScrollAreaWidgetContents.layout().addWidget(self.win_list[temp])
                print("[Debug] \tContent List added to Parent's window Widget")

            except Exception as e:
                print(f"An Error Occurred in LoadChildrenItems > children items loader connector: {e}")

        try:
            tempName = random.randint(11111,99999)
            self.threadController[f"parent items loader-{tempName}"] = LoadParentItemsThread(entries)
            self.threadController[f"parent items loader-{tempName}"].start()
            self.threadController[f"parent items loader-{tempName}"].any_signal.connect(parent_items_loader_connector)
        except Exception as e:
            print(f"An Error Occurred in LoadParentItems > start loading parent items: {e}")


class LoadParentItemsThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, entries):
        super(LoadParentItemsThread, self).__init__()
        self.entries = entries
        self.data_to_emit = {}

    def stop(self):
        self.requestInterruption()

    def run(self):
        try:
            if self.isInterruptionRequested() is True:
                raise StoppedByUserException

            self.data_to_emit['completed'] = False

            self.data_to_emit['entry'] = self.entries
            self.any_signal.emit(self.data_to_emit)
            time.sleep(0.2)

        except StoppedByUserException:
            print("stopped by user")
        except Exception as e:
            print(f"An Error Occurred in threadLodParentItems > run: {e}")
        pass
