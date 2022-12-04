import yt_dlp as youtube_dl     #yt-dlp-2022.1.21, yt-dlp 2022.3.8.2 ---- yt-dlp==2022.8.19
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import time

from generalFunctions import GeneralFunctions


class GetEntryThread(QtCore.QThread):
    """
    1. take url and the parent (window that call this class)
    2. detect if url contains playlist
    3. if url is non playlist: extract video all info and return only wanted info (entry)
    4. if url is playlist: extract video info for all video in the list and return list of video info (entry list)
    """
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, url, my_parent):
        super(GetEntryThread, self).__init__()
        try:
            # print(f"data:  {data}")
            self.is_running = False
            self.myself = my_parent
            self.url = url
            self.info_logger = self.InfoLogger()
            self.entry_messages = ""
            self.emit_data = {}

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
            self.myself.reset_variables()

            # self.myself.busy = True
            common_title = ""

            # set info extraction/ download options
            # ------------------------------------
            path = os.path.join(os.getcwd(),'youtube-cookie.txt')
            print(f"path::::: {path}")
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

                # extract required video info from the entries
                # ---------------------------------------------
                # entries = []
                #
                # for d in info['entries']:
                #     if d is not None:
                #         for final in d:
                #             print(">.>.>.>> ", final)
                #         print("----------------------------------------------------")
                #         print()

                # print(f"is playlist? : {isPlaylist}")
                self.entry_messages = "Extracting Required Video data..."
                self.myself.private_video_count = 0
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

                            self.myself.download_entries.append(entry)
                        else:
                            self.myself.private_video_count += 1  # [ update self.private_video_count here ]
                else:
                    # print(info)
                    try:
                        entry = {}

                        entry['is_playlist'] = isPlaylist
                        entry['title'] = GeneralFunctions().screen_the_title(info['title'])
                        entry['url'] = info['webpage_url']
                        entry['playlist_index'] = None
                        entry['playlist_title'] = None
                        entry['thumbnail'] = info['thumbnail']
                        entry['playlist_url'] = url

                        common_title = entry['title']
                        try:
                            available_format.append(info['formats'])
                        except:
                            available_format.append(info['format'])
                            # print(available_format)
                        # entry['formats'] = info['formats']

                        self.myself.download_entries.append(entry)
                    except Exception as e:
                        self.myself.busy = False
                        print(f"An Error occurred in 'get download entries: {e}")


                # Extract available formats [ update self.available_format here ]
                # ----------------------------------------------------------------
                self.entry_messages = "Extracting available formats..."
                self.myself.available_formats.clear()

                try:
                    check = None
                    if type(available_format[0]) is str:
                        check = available_format
                        for w in check:
                            try:
                                filesize = w['filesize']
                                filesize = GeneralFunctions().convert_size(filesize)
                            except Exception as e:
                                filesize = "Unknown file size"

                            self.myself.available_formats.append(w)
                            self.myself.comboBoxSelectFormat.addItem(f"{str(w)} : {filesize}")
                    else:
                        check = available_format[0]
                        for w in check:
                            try:
                                filesize = w['filesize']
                                filesize = GeneralFunctions().convert_size(filesize)
                            except Exception as e:
                                filesize = "Unknown file size"

                            self.myself.available_formats.append(w)
                            self.myself.comboBoxSelectFormat.addItem(f"{str(w['format'])} : {filesize}")

                except:
                    self.myself.comboBoxSelectFormat.clear()
                    self.myself.comboBoxSelectFormat.addItem("No Format Detected!")
                    self.myself.available_formats.clear()
                    pass

                # get the common title [update self.common_title here]
                # (playlist title in playlist and video title in non playlist)
                # ------------------------------------------------------------------------------------
                self.myself.common_title = common_title

                print('finished!')
                # self.entry_messages = "Completed!"
                # time.sleep(0.5)
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
