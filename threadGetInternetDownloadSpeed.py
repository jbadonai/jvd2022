# pip install speedtest-cli

import time
import speedtest
from PyQt5 import QtCore
from generalFunctions import GeneralFunctions
import urllib.request


class GetInternetConnectionSpeed():
    def __init__(self):
        self.download_speed = 0
        self.upload_speed = 0
        self.ip_address = None
        self.is_internet = False
        self.threadController = {}

    def start(self):
        def loading_connector(data):
            try:
                # print("[DATA] ", data)
                if 'download speed' in data:
                    self.download_speed = data['download speed']
                else:
                    self.download_speed = 0

                if 'upload speed' in data:
                    self.upload_speed = data['upload speed']
                else:
                    self.upload_speed = 0

                if 'internet connection' in data:
                    self.is_internet = data['internet connection']


                pass
            except Exception as e:
                print(f"An Error Occurred in 'geInternetConnection'>'start'> 'loading connector' : {e}")
        try:
            self.threadController['internet speed'] = DownloadSpeed()
            self.threadController['internet speed'].start()
            self.threadController['internet speed'].any_signal.connect(loading_connector)
        except Exception as e:
            print(f"An Error Occurred in 'getInternetDownloadSpeed'>start: {e}")
        pass

    def stop(self):
        try:
            self.threadController['internet speed'].stop()
            pass
        except Exception as e:
            print(f"An Error Occurred in 'getInternetDownloadSpeed'>'stop' : {e}")
        pass


class DownloadSpeed(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(DownloadSpeed, self).__init__()
        try:
            # print(f"data:  {data}")
            self.is_running = False
            self.download_speed = 0
            self.upload_speed = 0
            self.speed_test = None
            self.data = {}
            self.down_check = True
            self.up_check = True
            self.internet_check = True

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

    def _get_download_speed(self):
        try:
            self.down_check = False
            download_speed = self.speed_test.download()
            self.download_speed = f"{download_speed/1024/1024:.2f} Mbit/s"
            self.data['download speed'] = self.download_speed
            self.any_signal.emit(self.data)
            time.sleep(30)
            self.down_check = True
        except Exception as e:
            print(f"An Error Occurred in _get download speed: {e}")
            self.download_speed = 0

    def _get_upload_speed(self):
        try:
            self.up_check = False
            upload_speed = self.speed_test.upload()
            self.upload_speed = GeneralFunctions().convert_size(upload_speed)
            self.data['upload speed'] = self.upload_speed
            self.any_signal.emit(self.data)
            self.up_check = True

        except Exception as e:
            print(f"An Error Occurred in _get download speed: {e}")
            self.upload_speed = 0

    def run(self):
        try:
            self.is_running = True

            while True:
                if self.isInterruptionRequested() is True:
                    break

                try:
                    self.speed_test = speedtest.Speedtest()
                    break
                except Exception as e:
                    # print(f"An error occurred initializing speed test {e}. \nRetrying...")
                    pass
                time.sleep(5)

            # self.speed_test.get_servers()
            # self.speed_test.get_closest_servers()
            # best = self.speed_test.get_best_server()
            # print(f"Best server: {best}")
            while True:
                if self.isInterruptionRequested() is True:
                    break

                if self.down_check is True:
                    GeneralFunctions().run_function(self._get_download_speed)


                if self.is_running is False:
                    break
                time.sleep(1)

            pass

        except Exception as e:
            print(f"An Error occurred in getInternetDownloadSpeed > 'run' : {e}")


class InternetConnection(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(InternetConnection, self).__init__()
        try:
            self.is_running = False
            self.data = {}
            self.internet_check = True

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

    def _get_internet_connection_status(self):
        try:
            try:
                self.internet_check = False
                urllib.request.urlopen('https://www.google.com')  # Python 3.x
                self.data['internet connection'] = True
                self.any_signal.emit(self.data)
                self.internet_check = True
                return True
            except Exception as e:
                self.data['internet connection'] = False
                self.any_signal.emit(self.data)
                self.internet_check = True
                return False

        except Exception as e:
            print(e)

    def run(self):
        try:
            self.is_running = True

            while True:
                if self.isInterruptionRequested() is True:
                    break

                if self.internet_check is True:
                    GeneralFunctions().run_function(self._get_internet_connection_status)
                    # self._get_internet_connection_status()

                if self.is_running is False:
                    break
                time.sleep(3)

            pass

        except Exception as e:
            print(f"An Error occurred in getInternetDownloadSpeed > 'run' : {e}")


