from PyQt5 import QtCore
from videoDatabase import VideoDatabase
import time
from exceptionList import *

class Statistics():
    def __init__(self, parent):
        self.myself = parent
        self.threadController = self.myself.threadController

    def start_getting_statistics(self):

        def statistics_connector(data):
            try:
                # print(data)
                self.myself.textAll.setText(str(data['all']))
                self.myself.textInProgress.setText(str(data['downloading']))
                self.myself.textStopped.setText(str(data['stopped']))
                self.myself.textCompleted.setText(str(data['completed']))
                self.myself.textWaiting.setText(str(data['waiting']))
                pass
            except Exception as e:
                print(f"An Error Occurred in Statistics > statistics connector: {e}")

        try:
            self.threadController['statistics'] = StatisticsThread()
            self.threadController['statistics'].start()
            self.threadController['statistics'].any_signal.connect(statistics_connector)
        except Exception as e:
            print(f"An Error Occurred in Statistics > start getting statistics : {e}")


class StatisticsThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(StatisticsThread, self).__init__()
        self.database = VideoDatabase()
        self.data_to_emit = {}

    def stop(self):
        self.requestInterruption()
        pass

    def run(self):
        try:
            while True:
                if self.isInterruptionRequested() is True:
                    raise StoppedByUserException

                self.data_to_emit['all'] = self.database.get_total_number()
                self.data_to_emit['downloading'] = self.database.get_total_by_status('Downloading')
                self.data_to_emit['stopped'] = self.database.get_total_by_status('Stopped')
                self.data_to_emit['completed'] = self.database.get_total_by_status('Completed')
                self.data_to_emit['waiting'] = self.database.get_total_by_status('Waiting')

                self.any_signal.emit(self.data_to_emit)

                time.sleep(1)
        except StoppedByUserException:
            pass

        except Exception as e:
            print(f"An Error Occurred in 'StatisticsThread' > run : {e}")

