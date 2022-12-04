from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import time
addDownloadEmergencyStop = False
global_inner_error_message = None
import  random
import os
import requests
from exceptionList import *
from videoDatabase import VideoDatabase

class LoadImage():
    def __init__(self, parent):
        super(LoadImage, self).__init__()
        self.myself = parent

        self.labelImage = self.myself.labelImage
        self.threadController = self.myself.threadController
        self.thumbnail = self.myself.thumbnail
        self.counter = 0


    def start_loading_image(self):
        self.labelImage.setText("Loading\nImage\nPlease Wait...")

        def image_loader_connector(data):
            imageError = data['image_error']
            if imageError is True:
                if data['retrying'] is True:
                    self.counter += 1
                    self.labelImage.setText(f"Image Loading Error.Retrying [{self.counter}]")
                else:
                    self.labelImage.setText(f"Image Loading Error.")
                    self.myself.image_loading_error = True
            else:
                self.myself.image_loading_error = False

            if 'image_filename' in data:
                image_filename = data['image_filename']
                self.labelImage.setPixmap(QPixmap(f"temp\\{image_filename}"))
                self.labelImage.setScaledContents(True)
        pass

        tempName = random.randint(22222,99999)
        self.threadController[f"ImageLoader-{tempName}"] = LoadImageThread(self.myself, self.thumbnail)
        self.threadController[f"ImageLoader-{tempName}"].start()
        self.threadController[f"ImageLoader-{tempName}"].any_signal.connect(image_loader_connector)


class LoadImageThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self,parent, thumbnail):
        super(LoadImageThread, self).__init__()
        self.thumbnail = thumbnail
        # self.is_running = False
        self.imageData = None
        self.myself = parent
        self.data_to_emit = {}
        self.data_to_emit['image_error'] = False
        self.data_to_emit['retrying'] = True


        self.max_retries = int(VideoDatabase().get_settings('max_retries'))
        self.retries = 0

    def stop(self):
        # self.is_running = False
        self.requestInterruption()
        pass

    def run(self):
        try:
            self.retries += 1
            if self.isInterruptionRequested() is True:
                raise StoppedByUserException

            # check if directory 'temp' where image will be store does not exist then create the directory
            if os.path.exists("temp") is False:
                os.makedirs("temp")

            # this process of loading image was separated into a different function to make error catching easy
            self.load_image()

            if self.isInterruptionRequested() is True:
                raise StoppedByUserException

            # if there is no image error then load the image
            if self.imageData != "Error":
                tempFilename = f"img_{random.randrange(1111, 9999)}"

                # write the image byte obtained from internet to file using the tempfilename generated above
                with open(f"temp\\{tempFilename}", 'wb') as f:
                    f.write(self.imageData)

                self.data_to_emit['image_filename'] = tempFilename
                self.any_signal.emit(self.data_to_emit)
                time.sleep(0.1)
            else:
                self.data_to_emit['image_error'] = True
                self.any_signal.emit(self.data_to_emit)
                self.max_retries = int(VideoDatabase().get_settings('max_retries'))
                if self.retries <= self.max_retries:
                    time.sleep(5)
                    self.run()
                else:
                    self.data_to_emit['retrying'] = False
                    self.any_signal.emit(self.data_to_emit)


        except StoppedByUserException:
            print("stopped by user")
        except Exception as e:
            self.is_running = False
            print(f"An Error Occurred in LoadImageThread > run: {e}")
        pass

    def load_image(self):
        try:
            self.imageData = requests.get(self.thumbnail).content
        except Exception as e:
            self.imageData = 'Error'
            pass
