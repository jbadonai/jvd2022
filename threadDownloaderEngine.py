from PyQt5 import QtCore
from videoDatabase import VideoDatabase
from exceptionList import *
from generalFunctions import GeneralFunctions
import time
import random
import signal
import  os
import yt_dlp as youtube_dl
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QSizeGrip,QWidget, QMenu, \
    QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout, QBoxLayout, QFormLayout, QSizePolicy


class DownloaderEngine():
    def __init__(self, parent):
        self.parent = parent
        self.threadController = self.parent.threadController

    def start_downloader_engine(self):

        def downloader_engine_connector(data):
            # print(data)
            try:
                self.parent.message = data['download_message']

                if data['download_error'] is True:
                    if data['download_error_message'] != "":
                        self.parent.select_object(self.parent.buttonWarning)
                        self.parent.error_detected = True
                        self.parent.error_message = data['download_error_message']
                        self.parent.message = "Stopped!.\nAn Error Occurred"
                        VideoDatabase().set_status(self.parent.url, "Stopped")

                if data['download_completed'] is True:
                    VideoDatabase().set_status(self.parent.url, "Completed")

                if self.threadController[f'{self.parent.title}'].logger.alreadyDownloaded is True:
                    VideoDatabase().set_status(self.parent.url, "Completed")

                self.parent.textETA.setText(str(data['eta']))
                self.parent.textSpeed.setText(str(data['speed']))
                self.parent.textDownloaded.setText(str(data['downloaded']))
                self.parent.textSize.setText(str(data['size']))

                percent = str(data['percent']).replace("%","")
                percent = round(float(percent))
                self.parent.progressBar.setValue(percent)

                pass
            except Exception as e:
                print(f"An Error Occurred in DownloaderEngine > downloader engine connector: {e}")
            pass

        try:
            self.threadController[f'{self.parent.title}'] = DownloaderEngineThread(self.parent)
            self.threadController[f'{self.parent.title}'].start()
            self.threadController[f'{self.parent.title}'].any_signal.connect(downloader_engine_connector)
        except Exception as e:
            print(f"An Error Occurred in ChildStatusUpdater > start updating child status: {e}")

    def stop(self):
        self.threadController[f'{self.parent.title}'].stop()
        pass


class DownloaderEngineThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent):
        super(DownloaderEngineThread, self).__init__()
        self.myself = parent
        self.data_to_emit = {}
        self.functions = GeneralFunctions()
        self.db = VideoDatabase()
        self.logger = self.MyLogger()

        self.download_error = False
        self.download_error_message = ""
        self.download_completed = False

        self.download_message = ""
        self.download_started_in_thread = False

        self.finish_counter =0
        self.data_to_emit['download_completed'] = False
        self.data_to_emit['download_message'] = ""
        self.data_to_emit['download_error'] = False
        self.data_to_emit['eta'] = ""
        self.data_to_emit['speed'] = ""
        self.data_to_emit['size'] = ""
        self.data_to_emit['percent'] = 0
        self.data_to_emit['downloaded'] = ""

        self.audio_conversion_started = False

    def stop(self):
        self.requestInterruption()
        self.logger.interrupted = self.isInterruptionRequested()

    def send_message(self, message):
        self.data_to_emit['download_message'] = message
        self.any_signal.emit(self.data_to_emit)
        time.sleep(1)

    def start_downloading(self):
        self.send_message("Starting Download...")
        # download_location = self.db.get_settings('default_download_location')
        download_location = VideoDatabase().get_download_location_by_url(self.myself.url)
        print(f"Download location at starting download: {download_location}")


        videoFormat = None
        if self.myself.format == "Best Quality":
            videoFormat = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        else:
            videoFormat = str(self.myself.format).split(" ")[0].strip()

        self.download(url=self.myself.url,
                      directory=download_location,
                      video_format=videoFormat)

        pass

    # def stop_downloading(self, status):
    #     self.send_message(f"Stopping download...")
    #     time.sleep(1)
    #     # self.requestInterruption()
    #     self.logger.interrupted = True
    #     self.send_message(status)
    #     pass

    class MyLogger(object):
        # loggerEmergencyStop = False
        alreadyDownloaded = False
        # logger_functions = None
        # url = None
        loggerMessage = ""
        loggerWarning = "..."
        loggerCompleted = False
        fragment = False

        interrupted = False
        error_message = ""

        merging_required = False
        audio_download_completed = False

        def debug(self, msg):
            # print(f"[msg] - {msg}")

            if self.interrupted is True:
                print(f"Interrupted!")
                signal.signal(signal.SIGTERM, self.debug)

            try:
                # print(">>> ", msg)
                if str(msg).__contains__('[download]') is False:
                    self.loggerMessage = f"\nPreparing to Download! Please Wait..."
                else:
                    # self.loggerMessage = msg
                    self.loggerMessage = "Downloading..."

                #   Already downloaded check
                if str(msg).lower().__contains__('already'):
                    self.loggerMessage = "url already downloaded"
                    self.alreadyDownloaded = True

                #   checking format merging
                if str(msg).lower().__contains__('format'):
                    if str(msg).lower().__contains__('+'):
                        self.merging_required = True

                if str(msg).lower().__contains__('destination'):
                    print(f"initial destination file: {str(msg).split(':')[1]}")
                    print(msg)
                    if str(msg).lower().__contains__('ffmpeg'):
                        print(f"final destination file: {str(msg).split(':')[1]}")
                        print(msg)
                if str(msg).lower().__contains__('deleting original file'):
                    print(msg)
                    print(f"Audio download completed. Thanks")
                    self.audio_download_completed = True

                if self.fragment is False:
                    if str(msg).lower().__contains__('frag'):
                        self.fragment = True

                if str(msg).lower().__contains__('Fixing'):
                    self.loggerCompleted = True
                    print("Completed by fixing")

                pass
            except EmergencyError:
                signal.signal(signal.SIGTERM, youtube_dl.YoutubeDL.download)

                pass
            except Exception as e:
                signal.signal(signal.SIGTERM, youtube_dl.YoutubeDL.download)
                pass

        def warning(self, msg):
            self.loggerWarning = msg
            pass

        def error(self, msg):
            # print(f"Error in MYLOgger::: {msg}")
            self.error_message = msg
            signal.signal(signal.SIGTERM, self.debug)

            pass

    def my_hook(self, d):

        if self.isInterruptionRequested() is True:
            print("interrupted in my hook")
            raise StoppedByUserException

        try:
            # print("[status] - ", d['status'])

            # handle Finished download
            # ------------------------------------------------------------
            if d['status'] == 'finished':
                self.finish_counter += 1
                if self.finish_counter == 1:
                    if self.myself.download_video is True:
                        print('Done downloading, now converting ...')
                        if self.logger.fragment is True:
                            print('completed by fragment')
                            self.finish_counter = 2

                        if self.logger.merging_required is False:
                            print('completed by No Audio. No merging')
                            self.finish_counter = 2

                    else:
                        print("Download completed for Audio")
                        # self.db.set_status(self.videoURL, 'completed')
                        if self.logger.audio_download_completed is True:
                            self.data_to_emit['download_completed'] = True
                            self.any_signal.emit(self.data_to_emit)
                            time.sleep(0.1)
                            print('Conversion completed')
                        else:
                            print("Converting audio.....")
                            self.audio_conversion_started = True

                if self.finish_counter == 2:
                    self.finish_counter = 0
                    print("Completed!!!!!!!!!!!!!!!!!!!!!!!")
                    # self.downloadCompleted = True
                    # self.db.set_status(self.videoURL, 'completed')
                    self.data_to_emit['download_completed'] = True
                    self.any_signal.emit(self.data_to_emit)
                    time.sleep(0.1)

                if self.logger.loggerCompleted is True:
                    self.finish_counter = 2

            # ETA
            # --------------------------------------------
            try:
                _eta = str(d['_eta_str'])
            except:
                _eta = "00:00"

            self.data_to_emit['eta'] = _eta

            # Speed
            # ----------------------------------------------------
            try:
                _speed = d['_speed_str']
            except:
                _speed = "-:-"

            self.data_to_emit['speed'] = _speed

            # downloaded
            # -----------------------------------------------------------
            try:
                _downloaded = str(self.functions.convert_size(d['downloaded_bytes']))
            except:
                _downloaded = "-:-"

            self.data_to_emit['downloaded'] = _downloaded

            # Size
            # --------------------------------------------------------------------
            try:
                _size = str(self.functions.convert_size(d['total_bytes']))
            except:
                _size = "-"

            self.data_to_emit['size'] = _size

            # Percent
            # ----------------------------------------------------------
            try:
                _percent = d['_percent_str']
            except:
                _percent = "100%"
            self.data_to_emit['percent'] = _percent

            self.data_to_emit['download_error'] = self.download_error
            self.data_to_emit['download_error_message'] = self.download_error_message
            self.data_to_emit['download_message'] = self.logger.loggerMessage

            self.any_signal.emit(self.data_to_emit)
            time.sleep(0.2)

        except StoppedByUserException:
            print(f"An Error Occurred in DownladerEngineThread > my_hook:[stopped by user] {e}")
            signal.signal(signal.SIGTERM, self.my_hook)

        except Exception as e:
            print(f"An Error Occurred in DownladerEngineThread > my_hook: {e}")
            signal.signal(signal.SIGTERM, self.my_hook)

    def download(self, url,
                 directory='downloads',
                 video_format='bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'):

        # check if the root directory exists, if not create one.
        if directory == 'downloads':
            full_download_path = os.path.join(os.getcwd(), directory)
            if os.path.exists(full_download_path) is False:
                os.makedirs(full_download_path)

        if video_format != 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best':
            if 'audio' not in str(video_format):
                video_format = str(video_format).split(" ")[0].strip()
                video_format = f"{video_format}+bestaudio[ext=m4a]/best[ext=mp4]/best"
            else:
                video_format = str(video_format).split(" ")[0].strip()

        # print(f"selected format  is ::::::::::::{video_format}")

        # set the output template depending on wether the url is playlist or not
        print(f"Directory @ download: {directory}")
        if self.myself.is_playlist:
            outtmpl = f'{directory}/{self.myself.playlist_title}/{self.myself.playlist_index}-{self.myself.title}.%(ext)s'
        else:
            outtmpl = f'{directory}/{self.myself.title}.%(ext)s'

        # set the looger object
        logger = self.logger

        # check if Audio or vidoe is being downloaded and set youtube dl option accordingly
        if self.myself.download_video is True:
            # option for downloading video
            ydl_opts = {
                'outtmpl': outtmpl,
                'format': video_format,
                'postprocesor-args': 'loglevel quiet, -8',
                'nopart': True,
                'quiet': True,
                'logger': logger,
                'progress_hooks': [self.my_hook],
            }
        else:
            # option for downloading audio
            ydl_opts = {
                'outtmpl': outtmpl,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',

                }],
                'postprocesor-args': 'loglevel quiet, -8',
                'nopart': True,
                'quiet': True,
                'logger': logger,
                'progress_hooks': [self.my_hook],
            }

        # downloading with youtube-dl with the opiton set above.
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            if self.logger.error_message != "":
                self.download_error = True
                self.download_error_message = self.logger.error_message

            else:
                # print(f"An Error occurred in DownloaderEngineThread > download : {e}")
                self.download_error = True
                self.download_error_message = self.logger.error_message

            self.data_to_emit['download_error'] = self.download_error
            self.data_to_emit['download_error_message'] = self.download_error_message

            self.any_signal.emit(self.data_to_emit)

            # if self.Logger.loggerEmergencyStop is False:
            #     if self.functions.IsInternet() is False:
            #         self.retries_counter += 1
            #         if self.retries_counter <= self.max_retries:
            #             print("retrying download in 5s")
            #             time.sleep(5)
            #             print(f"retrying [{self.retries_counter}/{self.max_retries}]...")
            #             self.message = f"retrying [{self.retries_counter}/{self.max_retries}]..."
            #             self.download(url, directory, video_format)
            #         else:
            #             print(
            #                 f"Internet Connection issue. Download stopped after {self.max_retries} retries. Please restart downloading of '{self.title}' when connection is restored.")
            #             self.message = f"Internet Connection issue. Download stopped after {self.max_retries} retries. Please restart downloading of '{self.title}' when connection is restored."
            #             self.db.set_status(self.videoURL, 'stopped')
            #             self.retries_counter = 0
            #             print("[][][][][][][][][][][][][][][][][][][]")
            #

    def run(self):
        try:

            self.myself.deselect_object(self.myself.buttonWarning)
            self.myself.error_message = ""

            self.data_to_emit['download_completed'] = False
            self.data_to_emit['download_message'] = ""

            if self.isInterruptionRequested():
                raise StoppedByUserException

            # wait for all data to be loaded before starting download engine properly
            while True:
                if self.myself.myGrandParent.data_loading_completed is True:
                    break
                time.sleep(1)

            # continuously check status to decide wether to start or stop download
            audio_conversion_counter = 0
            while True:
                if self.isInterruptionRequested():
                    raise StoppedByUserException

                # get status
                status = self.myself.database.get_status(self.myself.url)
                # if status changed to downloading and downloding has not started
                if status == 'Downloading':
                    if self.logger.loggerMessage != "" and str(self.logger.loggerMessage).__contains__("Downloading") is False:
                        if self.audio_conversion_started is False:
                            # self.send_message(f"Downloading...\n{self.logger.loggerMessage}")
                            self.send_message(f"{self.logger.loggerMessage}")

                    if self.download_started_in_thread is False:
                        self.download_started_in_thread = True
                        GeneralFunctions().run_function(self.start_downloading)

                # if download is in progress and user clicked stop which set the status to stopped
                # or restart which might set the status to waiting
                status = self.myself.database.get_status(self.myself.url)
                if status == 'Stopped' or status == 'Waiting':

                    if self.myself.download_in_progress is True:
                        # self.send_message(status)

                        self.logger.interrupted = True
                        self.logger.loggerMessage = "Stopping Download..."
                        self.myself.download_in_progress = False
                        self.myself.labelStatus.setText("Stopping Download...")
                        time.sleep(2)
                        self.myself.labelStatus.setText(status)
                        break

                status = self.myself.database.get_status(self.myself.url)
                if status == "Completed":
                    print("Status: completed <<<<<<<<<<<<<<<<<<<")
                    self.send_message("Completed")
                    break

                # check for audio download only conversion is completed
                # conversion happen outside the hook, so it could not be tracked there
                if self.myself.download_video is False:
                    status = self.myself.database.get_status(self.myself.url)
                    if self.audio_conversion_started is True and status != "Completed":
                        audio_conversion_counter += 1
                        tt = GeneralFunctions().format_seconds(audio_conversion_counter)
                        self.send_message(f"Converting Audio to mp3.\nPlease wait...\n [ {tt} ]")

                    if self.logger.audio_download_completed is True:
                        self.logger.audio_download_completed = False
                        self.audio_conversion_started = False
                        self.data_to_emit['download_completed'] = True
                        self.any_signal.emit(self.data_to_emit)
                        time.sleep(0.1)
                        self.send_message("Completed!")

                time.sleep(1)

        except StoppedByUserException:
            pass

        except Exception as e:
            print(f"An Error Occurred in DownloaderEngineThread > run : {e}")
