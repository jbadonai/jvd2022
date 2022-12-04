from PyQt5 import QtCore
import time
addDownloadEmergencyStop = False
global_inner_error_message = None
import random
from exceptionList import *
from childItemWindow import ChildItemWindow
from videoDatabase import VideoDatabase


class LoadChildrenItems():
    def __init__(self, parent, grandparent, data):
        super(LoadChildrenItems, self).__init__()
        self.parent = parent
        self.grandparent = grandparent
        self.entries = data
        self.threadController = self.parent.threadController
        self.win_list = {}
        print("[Debug] \tLoad Children Item Initialized: LoadChildrenItem.__init__")
        # print(self.entries)

    def start_loading_children_items(self, refreshing = False):

        def children_items_loader_connector(data):
            try:

                entry = data['entry']
                temp = f"child window - {random.randint(1111,5555)}"
                self.win_list[temp] = ChildItemWindow(parent=self.parent, grandParent=self.grandparent, entry=entry)
                self.parent.frame_parent.layout().addWidget(self.win_list[temp])
                # add the window handle object for accessibility in other class

                if refreshing is False:
                    self.grandparent.children_window_handle_list.append(self.win_list[temp])
                    self.grandparent.total_loaded += 1
                    # update total data variable

                    totalData = VideoDatabase().get_total_number()
                    self.grandparent.total_data = totalData

                    if totalData == self.grandparent.total_loaded:
                        self.grandparent.main_message = "Loading Completed."
                        self.grandparent.data_loading_completed = True

                    # print(totalData, "<><>", self.grandparent.total_loaded)

                    percentage = round((self.grandparent.total_loaded / self.grandparent.total_data)*100)

                    if percentage < 99:
                        self.grandparent.main_message = f"[ {percentage}% ] Loading {self.grandparent.total_loaded} of {self.grandparent.total_data} videos in your download list"
                    else:
                        self.grandparent.main_message = "Loading Completed."
                        self.grandparent.data_loading_completed = True

                    if totalData == self.grandparent.total_loaded:
                        self.grandparent.main_message = "Loading Completed."
                        self.grandparent.data_loading_completed = True



            except Exception as e:
                print(f"An Error Occurred in LoadChildrenItems > children items loader connector: {e}")

        try:
            tempName = random.randint(11111,99999)
            self.threadController[f"children items loader-{tempName}"] = LoadChildrenItemsThread(self.entries)
            self.threadController[f"children items loader-{tempName}"].start()
            self.threadController[f"children items loader-{tempName}"].any_signal.connect(children_items_loader_connector)
        except Exception as e:
            print(f"An Error Occurred in LoadChildrenItems > start loading children items: {e}")


class LoadChildrenItemsThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, entries):
        super(LoadChildrenItemsThread, self).__init__()
        self.entries = entries
        self.data_to_emit = {}

    def stop(self):
        self.requestInterruption()

    def run(self):
        try:
            if self.isInterruptionRequested() is True:
                raise StoppedByUserException

            self.data_to_emit['completed'] = False
            for index, data in enumerate(self.entries):
                self.data_to_emit['entry'] = data
                self.any_signal.emit(self.data_to_emit)
                time.sleep(0.2)

        except StoppedByUserException:
            print("stopped by user")
        except Exception as e:
            print(f"An Error Occurred in threadLodChildrenItems > run: {e}")
        pass
