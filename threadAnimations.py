
import time
import speedtest
from PyQt5 import QtCore
from generalFunctions import GeneralFunctions
import urllib.request
import random


class ObjectBlinker():
    def __init__(self,myParent, object_to_blink, interval):
        self.myObject = object_to_blink
        self.interval = interval
        self.myParent = myParent
        self.threadController = myParent.threadController
        self.isActive = False
        self.thisBlinkerId = f"blinker{random.randint(11111, 99999)}"

    def stop_blinking(self):
        try:
            self.threadController[self.thisBlinkerId].stop()
            self.isActive = False
            pass
        except Exception as e:
            print(f"An Error Occurred in Stop blinking(): {e}")

    def start_blinking(self):
        try:
            self.isActive = True

            def blinker_connector(data):
                pass

            self.threadController[self.thisBlinkerId] = BlinkerThread(self.myObject, self.interval)
            self.threadController[self.thisBlinkerId].start()
            self.threadController[self.thisBlinkerId].any_signal.connect(blinker_connector)
        except Exception as e:
            print(f"An Error Occurred in start blinking(): {e}")
        pass


class BlinkerThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, object_to_blink, interval):
        super(BlinkerThread, self).__init__()
        try:
            self.is_running = False
            self.data = {}
            self.internet_check = True
            self.myObject = object_to_blink
            self.interval = interval

        except Exception as e:
            print(f"An Error Occurred in getEntryThread > __init__(): \n >>{e}")

    def stop(self):
        try:
            self.requestInterruption()
            self.is_running = False
            # self.terminate()
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass

    def run(self):
        try:
            self.is_running = True

            while True:
                if self.isInterruptionRequested() is True:
                    break

                if self.myObject.isVisible() is True:
                    self.myObject.setVisible(False)
                else:
                    self.myObject.setVisible(True)

                time.sleep(self.interval)

            self.myObject.setVisible(True)
            pass

        except Exception as e:
            print(f"An Error occurred in getInternetDownloadSpeed > 'run' : {e}")



class ObjectHighlighter():
    def __init__(self,myParent):
        self.myParent = myParent
        self.threadController = myParent.threadController
        self.activeObjects = []

    def stop_highlight(self, highlight_object):
        ans = highlight_object.text() in self.activeObjects
        print(self.activeObjects)
        print("stopping: ", ans)
        if ans is True:
            print('True oooooooooooooo')
            self.activeObjects.pop(self.activeObjects.index(highlight_object.text()))
            self.threadController['h'].stop()
        pass

    def start_highlight(self, highlight_object):

        ans = highlight_object.text() in self.activeObjects
        if ans is False:
            self.activeObjects.append(highlight_object.text())

            def blinker_connector(data):
                pass

            self.threadController['h'] = HighlightThread(self.myParent, highlight_object)
            self.threadController['h'].start()
            self.threadController['h'].any_signal.connect(blinker_connector)
            pass


class HighlightThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, myParent, object_to_highlight):
        super(HighlightThread, self).__init__()
        try:
            self.is_running = False
            self.data = {}
            self.myObject = object_to_highlight
            self.myParent = myParent
            self.switch = True

        except Exception as e:
            print(f"An Error Occurred in getEntryThread > __init__(): \n >>{e}")

    def stop(self):
        try:
            self.requestInterruption()
            self.is_running = False
            # self.terminate()
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass

    def run(self):
        try:
            self.is_running = True
            print("stylesheet original: ", self.myObject.styleSheet())

            style1 = "border-top: 1px solid blue;" \
                     "border-right: 1px solid gray;" \
                     "border-bottom: 1px solid gray;" \
                     "border-left: 1px solid gray;"

            style2 = "border-top: 1px solid gray;" \
                     "border-right: 1px solid blue;" \
                     "border-bottom: 1px solid gray;" \
                     "border-left: 1px solid gray;"


            style3 = "border-top: 1px solid gray;" \
                     "border-right: 1px solid gray;" \
                     "border-bottom: 1px solid blue;" \
                     "border-left: 1px solid gray;"


            style4 = "border-top: 1px solid gray;" \
                     "border-right: 1px solid gray;" \
                     "border-bottom: 1px solid gray;" \
                     "border-left: 1px solid blue;"

            interval = 0.1

            while True:
                if self.isInterruptionRequested() is True:
                    break

                self.myObject.setStyleSheet(style1)
                time.sleep(interval)
                self.myObject.setStyleSheet(style2)
                time.sleep(interval)
                self.myObject.setStyleSheet(style3)
                time.sleep(interval)
                self.myObject.setStyleSheet(style4)
                time.sleep(interval)

            pass

        except Exception as e:
            print(f"An Error occurred in getInternetDownloadSpeed > 'run' : {e}")

