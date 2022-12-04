import yt_dlp as youtube_dl     #yt-dlp-2022.1.21, yt-dlp 2022.3.8.2 ---- yt-dlp==2022.8.19
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import time

from generalFunctions import GeneralFunctions
from videoDatabase import VideoDatabase
from threadAnimations import ObjectBlinker, ObjectHighlighter

class RefreshPlaylistEntries:
    def __init__(self, parent, playlistUrl):
        self.url = playlistUrl
        self.myself = parent
        self.threadController = self.myself.threadController

    def refresh(self):

        def refresh_connector(data):
            if data['finished'] is True:
                print("Download Entries: ", data['download_entries'])
                self.myself.load_refreshed_data(data=data['download_entries'])
            pass

        self.threadController['refresh playlist'] = RefreshPlaylistEntryThread(self.url, self.myself)
        self.threadController['refresh playlist'].start()
        self.threadController['refresh playlist'].any_signal.connect(refresh_connector)



class RefreshPlaylistEntryThread(QtCore.QThread):
    """

    """
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, url, my_parent):
        super(RefreshPlaylistEntryThread, self).__init__()
        try:
            # print(f"data:  {data}")
            self.is_running = False
            self.myself = my_parent
            self.url = url
            self.info_logger = self.InfoLogger()
            self.entry_messages = ""
            self.emit_data = {}

            self.download_entries = []
            self.private_video_count = 0

            self.emit_data['download_entries'] = self.download_entries
            self.emit_data['finished'] = False

        except Exception as e:
            print(f"An Error Occurred in getEntryThread > __init__(): \n >>{e}")

    def message_broadcaster(self):
        try:
            while True:
                if self.is_running is False:
                    if self.entry_messages.__contains__("Error!") is False:
                        self.entry_messages = "Completed!"
                        self.emit_data['info'] = self.entry_messages
                        self.any_signal.emit(self.emit_data)
                        time.sleep(1)
                    else:
                        self.entry_messages = f"Error!:{self.info_logger.innerErrorMessage}"
                        self.emit_data['info'] = self.entry_messages
                        self.any_signal.emit(self.emit_data)
                        time.sleep(1)
                    break

                if self.info_logger.innerMessage != "":
                    self.entry_messages = self.info_logger.innerMessage

                self.emit_data['info'] = self.entry_messages
                self.any_signal.emit(self.emit_data)
                time.sleep(0.5)
                pass
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > 'message broadcaster' : {e}")

    def stop(self):
        try:
            self.is_running = False
            # self.terminate()
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass

    def run(self):
        try:
            self.is_running = True
            GeneralFunctions().run_function(self.message_broadcaster)
            # self.message_broadcaster()
            self.info_logger.innerMessage = ""

            self.get_download_entries(self.url)

        except Exception as e:
            self.myself.busy = False
            print(f"An Error occurred in getEntryThread > 'run' : {e}")

    def get_download_entries(self, url):
        # get download items/data from url
        try:
            self.entry_messages = "Extracting Video Info..."

            # set info extraction/ download options
            # ------------------------------------
            path = os.path.join(os.getcwd(),'youtube-cookie.txt')
            ydl_opts = {
                'postprocesor-args': 'loglevel quiet, -8',
                'nopart': True,
                'quiet': True,
                # 'username': 'jbadonaiventures@gmail.com',
                # 'password': "Afolayemi1",
                'ignoreerrors': True,
                'logger': self.info_logger,
            }

            # Extract video info
            # -----------------------
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            # print(info)
            # detect if url contains playlist or not
            # -------------------------------------
            isPlaylist = None
            if info is not None:
                self.info_logger.innerMessage = "" # to stop broadcasting inner message
                try:
                    print(info['requested_entries'])
                    # ans = info['requested_entries']
                    isPlaylist = True
                except Exception as e:
                    isPlaylist = False

                self.entry_messages = "Extracting Required Video data..."
                self.private_video_count = 0
                available_format = []
                if isPlaylist:
                    for d in info['entries']:
                        if d is not None:
                            # print(d)
                            entry = {}

                            entry['is_playlist'] = isPlaylist
                            entry['title'] = GeneralFunctions().screen_the_title(d['title'])
                            entry['url'] = d['webpage_url']
                            entry['playlist_index'] = d['playlist_index']
                            entry['playlist_title'] = GeneralFunctions().screen_the_title(d['playlist_title'])
                            entry['thumbnail'] = d['thumbnail']
                            entry['playlist_url'] = url


                            available_format.append(d['formats'])
                            # entry['formats'] = d['formats']
                            common_title = d['playlist_title']
                            if VideoDatabase().is_url_exists_in_database(entry['url']) is False:
                                self.download_entries.append(entry)
                        else:
                            self.private_video_count += 1  # [ update self.private_video_count here ]


                self.emit_data['finished'] = True
                self.emit_data['download_entries'] = self.download_entries
                print('finished!')

                # self.any_signal.emit(self.emit_data)
            else:
                self.entry_messages = f"Error!:{self.info_logger.innerErrorMessage}"
                # print(f"entry message: {self.entry_messages}")
                self.is_running = False

            self.myself.busy = False
            self.is_running = False
        except Exception as e:
            self.myself.busy = False
            print(f"An Error Occurred in getEntryThread >  'get download entries' : {e}")

    # [1c]
    class InfoLogger(object):
        innerMessage = "waiting..."
        mainmsg = ""
        submsg = ""
        privateError = False
        innerErrorMessage = ""

        def debug(self, msg):
            print(msg)
            if '[download]' in str(msg):
                self.mainmsg = str(msg).replace('[download]',"").replace("Downloading", "Extracting Data for")
            else:
                self.submsg = str(msg).split(":")[1].replace("tab]","Analyzing ")
                # self.submsg = "Analysing the url..."

                # print(msg)
            if self.mainmsg != "":
                self.innerMessage = f"[ PLAYLIST DETECTED ]\n[ {self.mainmsg} ] {self.submsg}"
            else:
                self.innerMessage = f" {self.submsg}"
            pass

        def warning(self, msg):
            print(f"WARNING::: {msg}")
            pass

        def error(self, msg):
            # print("Error message:", msg)
            if str(msg).__contains__("Private"):
                self.privateError = True
                self.innerErrorMessage = str(msg).split(":")[-1]
                # print(f'inner:: {self.innerErrorMessage}')
            else:
                self.privateError = False
                self.innerErrorMessage = ""
            pass
