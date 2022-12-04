from PyQt5 import QtCore
from exceptionList import *
import time


class MonitorRunningThread():
    def __init__(self, parent):
        self.parent = parent
        self.thread_controller = {}

    def start_monitoring_running_threads(self):

        def monitor_thread_connector(data):
            # self.parent.labelTitle.setText(f"Number of Running Threads: {str(data['running_threads'])}")
            pass

        self.thread_controller['monitor thread'] = ThreadMonitorRunningThread(self.parent)
        self.thread_controller['monitor thread'].start()
        self.thread_controller['monitor thread'].any_signal.connect(monitor_thread_connector)


class ThreadMonitorRunningThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent):
        super(ThreadMonitorRunningThread, self).__init__()
        self.myself = parent
        self.running_threads_counter = 0
        self.data_to_emit = {}

    def stop(self):
        self.requestInterruption()

    def run(self):
        try:
            if self.isInterruptionRequested():
                raise StoppedByUserException

            while True:
                self.running_threads_counter = 0

                for thread in self.myself.threadController:
                    if self.myself.threadController[thread].isRunning() is True:
                        self.running_threads_counter += 1

                self.data_to_emit['running_threads'] = self.running_threads_counter
                self.any_signal.emit(self.data_to_emit)
                time.sleep(1)

        except StoppedByUserException:
            pass
        except Exception as e:
            print(f"An Error Occurred in ThreadMonitorRunningThread > run: {e}")
