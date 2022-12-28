import yt_dlp as youtube_dl  # yt-dlp-2022.1.21, yt-dlp 2022.3.8.2 ---- yt-dlp==2022.8.19
import os
import subprocess
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import time
import signal
from dialogs import MessageBox

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
            self.msgbox = MessageBox()
            self.availableFormat = []

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
            self.requestInterruption()
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

    def get_video_type(self, info):
        try:
            entries = info['entries'][0]
        except:
            return "nonPlaylist"

        try:
            entries = info['entries'][0]['entries']
            return "channel"
        except:
            return "playlist"

    def get_download_entries(self, url):
        # get download items/data from url
        try:
            self.entry_messages = "Extracting Video Info..."
            self.myself.reset_variables()
            common_title = ""

            # set info extraction/ download options
            # ------------------------------------

            ydl_opts = {
                'postprocesor-args': 'loglevel quiet, -8',
                'nopart': True,
                'quiet': True,
                'ignoreerrors': True,
                'logger': self.info_logger,
            }

            if self.myself.checkBoxNoPlaylist.isChecked() is True:
                ydl_opts['noplaylist'] = True

            # Extract video info
            # -----------------------
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            if info is not None:
                videoType = self.get_video_type(info)
                if videoType == 'channel':
                    self.process_channel_entries(info)
                else:
                    self.process_non_channel_entries(info, url)
                # self.info_logger.innerMessage = "" # to stop broadcasting inner message
                # try:
                #     print(info['requested_entries'])
                #     # ans = info['requested_entries']
                #     isPlaylist = True
                # except Exception as e:
                #     isPlaylist = False
                #
                # self.entry_messages = "Extracting Required Video data..."
                # self.myself.private_video_count = 0
                # available_format = []
                # if isPlaylist:
                #     for d in info['entries']:
                #         if d is not None:
                #             # print(d)
                #             entry = {}
                #             entry['is_playlist'] = isPlaylist
                #             entry['title'] = GeneralFunctions().screen_the_title(d['title'])
                #             entry['url'] = d['webpage_url']
                #             entry['playlist_index'] = d['playlist_index']
                #             entry['playlist_title'] = GeneralFunctions().screen_the_title(d['playlist_title'])
                #             entry['thumbnail'] = d['thumbnail']
                #             entry['playlist_url'] = url
                #
                #             available_format.append(d['formats'])
                #             # entry['formats'] = d['formats']
                #             common_title = d['playlist_title']
                #
                #             self.myself.download_entries.append(entry)
                #         else:
                #             self.myself.private_video_count += 1  # [ update self.private_video_count here ]
                # else:
                #     # print(info)
                #     try:
                #         entry = {}
                #         entry['is_playlist'] = isPlaylist
                #         entry['title'] = GeneralFunctions().screen_the_title(info['title'])
                #         entry['url'] = info['webpage_url']
                #         entry['playlist_index'] = None
                #         entry['playlist_title'] = None
                #         entry['thumbnail'] = info['thumbnail']
                #         entry['playlist_url'] = url
                #
                #         common_title = entry['title']
                #         try:
                #             available_format.append(info['formats'])
                #         except:
                #             available_format.append(info['format'])
                #             # print(available_format)
                #         # entry['formats'] = info['formats']
                #
                #         self.myself.download_entries.append(entry)
                #     except Exception as e:
                #         self.myself.busy = False
                #         print(f"An Error occurred in 'get download entries: {e}")
                #
                #
                # # Extract available formats [ update self.available_format here ]
                # # ----------------------------------------------------------------
                # self.entry_messages = "Extracting available formats..."
                # self.myself.available_formats.clear()
                #
                # try:
                #     check = None
                #     if type(available_format[0]) is str:
                #         check = available_format
                #         for w in check:
                #             try:
                #                 filesize = w['filesize']
                #                 filesize = GeneralFunctions().convert_size(filesize)
                #             except Exception as e:
                #                 filesize = "Unknown file size"
                #
                #             self.myself.available_formats.append(w)
                #             self.myself.comboBoxSelectFormat.addItem(f"{str(w)} : {filesize}")
                #     else:
                #         check = available_format[0]
                #         for w in check:
                #             try:
                #                 filesize = w['filesize']
                #                 filesize = GeneralFunctions().convert_size(filesize)
                #             except Exception as e:
                #                 filesize = "Unknown file size"
                #
                #             self.myself.available_formats.append(w)
                #             # +++>
                #             # print(w['format'])
                #             code = str(w['format']).split(" ")[0]
                #             quality = str(w['format']).split(" ")[-1].replace("(","").replace(")", "")
                #             dim = str(w['format']).replace(code,"").replace(quality,"").replace("-","").replace("(","").replace(")", "").strip()
                #
                #             format_w = f"[{quality}] - [{dim}] - [{code}] "
                #             #
                #             self.myself.comboBoxSelectFormat.addItem(f"{format_w} : {filesize}")
                #             # +++>
                #             # self.myself.comboBoxSelectFormat.addItem(f"{str(w['format'])} : {filesize}")
                #
                # except:
                #     self.myself.comboBoxSelectFormat.clear()
                #     self.myself.comboBoxSelectFormat.addItem("No Format Detected!")
                #     self.myself.available_formats.clear()
                #     pass
                #
                # # get the common title [update self.common_title here]
                # # (playlist title in playlist and video title in non playlist)
                # # ------------------------------------------------------------------------------------
                # self.myself.common_title = common_title
                #
                # print('finished!')
                # # self.entry_messages = "Completed!"
                # # time.sleep(0.5)
            else:
                self.entry_messages = f"Error!:{self.info_logger.innerErrorMessage}"
                self.is_running = False

            self.myself.busy = False
            self.is_running = False
        except Exception as e:
            self.myself.busy = False
            print(f"An Error Occurred in getEntryThread >  'get download entries' : {e}")

    def process_channel_entries(self, info):
        pass

    def process_non_channel_entries(self, info, url):
        isPlaylist = None
        common_title = ""
        self.availableFormat.clear()
        try:
            self.info_logger.innerMessage = ""  # to stop broadcasting inner message
            try:
                print(info['requested_entries'])
                isPlaylist = True
            except Exception as e:
                isPlaylist = False

            # > Extracting video data
            # > REQUIRED: [info, isPlaylist, url]
            # -------------------------------------------------------------
            self.entry_messages = "Extracting Required Video data..."
            self.myself.private_video_count = 0
            available_format = []

            if isPlaylist:
                for d in info['entries']:
                    if d is not None:
                        # entry = {}
                        data = {}

                        # entry['is_playlist'] = isPlaylist
                        data['is_playlist'] = isPlaylist

                        # entry['title'] = GeneralFunctions().screen_the_title(d['title'])
                        data['title'] = GeneralFunctions().screen_the_title(d['title'])

                        # entry['url'] = d['webpage_url']
                        data['url'] = d['webpage_url']

                        # entry['playlist_index'] = d['playlist_index']
                        data['playlist_index'] = d['playlist_index']

                        # entry['playlist_title'] = GeneralFunctions().screen_the_title(d['playlist_title'])
                        data['playlist_title'] = GeneralFunctions().screen_the_title(d['playlist_title'])

                        # entry['thumbnail'] = d['thumbnail']
                        data['thumbnail'] = d['thumbnail']

                        # entry['playlist_url'] = url
                        data['playlist_url'] = url

                        # available_format.append(d['formats'])
                        data['available_formats'] = d['formats']

                        # common_title = d['playlist_title']
                        data['common_title'] = d['playlist_title']

                        # self.myself.download_entries.append(entry)
                        self.push_video_data(data=data)
                    else:
                        self.myself.private_video_count += 1  # [ update self.private_video_count here ]
            else:
                # print(info)
                try:
                    # entry = {}
                    data = {}
                    # entry['is_playlist'] = isPlaylist
                    data['is_playlist'] = isPlaylist

                    # entry['title'] = GeneralFunctions().screen_the_title(info['title'])
                    data['title'] = GeneralFunctions().screen_the_title(info['title'])

                    # entry['url'] = info['webpage_url']
                    data['url'] = info['webpage_url']

                    # entry['playlist_index'] = None
                    data['playlist_index'] = None

                    # entry['playlist_title'] = None
                    data['playlist_title'] = None

                    # entry['thumbnail'] = info['thumbnail']
                    data['thumbnail'] = info['thumbnail']

                    # entry['playlist_url'] = url
                    data['playlist_url'] = url

                    # common_title = entry['title']
                    data['common_title'] = data['title']
                    try:
                        # available_format.append(info['formats'])
                        data['available_formats'] = info['formats']
                    except:
                        # available_format.append(info['format'])
                        data['available_formats'] = info['format']

                    # self.myself.download_entries.append(entry)
                    self.push_video_data(data=data)
                except Exception as e:
                    self.myself.busy = False
                    print(f"An Error occurred in 'get download entries: {e}")

            print("Next: pushing the available formats")
            # > Extract available formats [ update self.available_format here ]
            # > REQUIRED: available_format
            # ----------------------------------------------------------------
            self.push_available_formats(self.availableFormat)
            # self.entry_messages = "Extracting available formats..."
            # self.myself.available_formats.clear()
            # try:
            #     available_format.extend(self.availableFormat)
            #     check = None
            #     if type(available_format[0]) is str:
            #         check = available_format
            #         for w in check:
            #             try:
            #                 filesize = w['filesize']
            #                 filesize = GeneralFunctions().convert_size(filesize)
            #             except Exception as e:
            #                 filesize = "Unknown file size"
            #
            #             self.myself.available_formats.append(w)
            #             self.myself.comboBoxSelectFormat.addItem(f"{str(w)} : {filesize}")
            #     else:
            #         check = available_format[0]
            #         for w in check:
            #             try:
            #                 filesize = w['filesize']
            #                 filesize = GeneralFunctions().convert_size(filesize)
            #             except Exception as e:
            #                 filesize = "Unknown file size"
            #
            #             self.myself.available_formats.append(w)
            #             # +++>
            #             # print(w['format'])
            #             code = str(w['format']).split(" ")[0]
            #             quality = str(w['format']).split(" ")[-1].replace("(","").replace(")", "")
            #             dim = str(w['format']).replace(code,"").replace(quality,"").replace("-","").replace("(","").replace(")", "").strip()
            #
            #             format_w = f"[{quality}] - [{dim}] - [{code}] "
            #             #
            #             self.myself.comboBoxSelectFormat.addItem(f"{format_w} : {filesize}")
            #             # +++>
            #             # self.myself.comboBoxSelectFormat.addItem(f"{str(w['format'])} : {filesize}")
            #
            # except:
            #     self.myself.comboBoxSelectFormat.clear()
            #     self.myself.comboBoxSelectFormat.addItem("No Format Detected!")
            #     self.myself.available_formats.clear()
            #     pass

            print('Next: get commoon title')
            # > get the common title [update self.common_title here]
            # > REQUIRED: common_title
            # (playlist title in playlist and video title in non playlist)
            # ------------------------------------------------------------------------------------
            self.myself.common_title = common_title

            print('finished!')
        except Exception as e:
            print(f"An Error occurred in 'process non channel entries': {e}")

    def push_video_data(self, data):
        try:
            # get entry data
            entry = {}
            entry['is_playlist'] = data['is_playlist']
            entry['title'] = data['title']
            entry['url'] = data['url']
            entry['playlist_index'] = data['playlist_index']
            entry['playlist_title'] = data['playlist_title']
            entry['thumbnail'] = data['thumbnail']
            entry['playlist_url'] = data['playlist_url']

            # set common title
            common_title = data['common_title']

            # update available formats
            self.availableFormat.append(data['available_formats'])

            # update download entries that resides with parent
            self.myself.download_entries.append(entry)
        except Exception as e:
            print(f"An error occurred in 'Push video data' : {e}")
            pass

    def push_available_formats(self, availableFormat):
        try:
            available_format = []
            self.entry_messages = "Extracting available formats..."
            self.myself.available_formats.clear()
            try:
                available_format.extend(availableFormat)
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
                        # +++>
                        # print(w['format'])
                        code = str(w['format']).split(" ")[0]
                        quality = str(w['format']).split(" ")[-1].replace("(", "").replace(")", "")
                        dim = str(w['format']).replace(code, "").replace(quality, "").replace("-", "").replace("(",
                                                                                                               "").replace(
                            ")", "").strip()

                        format_w = f"[{quality}] - [{dim}] - [{code}] "
                        #
                        self.myself.comboBoxSelectFormat.addItem(f"{format_w} : {filesize}")
                        # +++>
                        # self.myself.comboBoxSelectFormat.addItem(f"{str(w['format'])} : {filesize}")

            except:
                self.myself.comboBoxSelectFormat.clear()
                self.myself.comboBoxSelectFormat.addItem("No Format Detected!")
                self.myself.available_formats.clear()

        except Exception as e:
            print(f"An Error occurred in 'push available formats': {e}")

    # [1c]
    class InfoLogger(object):
        innerMessage = "waiting..."
        mainmsg = ""
        submsg = ""
        privateError = False
        innerErrorMessage = ""
        total = []
        video_counter = 0
        playlistIdList = []
        channelIdList = []

        playlistVideoIdData = {}
        channelVideoIdData = {}
        currentPlaylistId = ""

        def debug(self, msg):
            print(msg)
            # trying to get playlist id
            if '[youtube:tab]' in str(msg) and 'Downloading webpage' in str(msg):
                # [youtube:tab] PLsUp7t2vRqx8Akc2GstIMjZ7SPUoGE_Ln: Downloading webpage
                id = str(msg).split(" ")[1].replace(":", "").strip()
                if id not in self.playlistIdList:
                    self.playlistIdList.append(id)
                    self.currentPlaylistId = id

                    # try to initialize it with an empty string value
                    pvd = self.currentPlaylistId not in self.playlistVideoIdData
                    cvd = self.currentPlaylistId not in self.channelVideoIdData
                    if pvd is True and cvd is True:
                        result = "@" in str(self.currentPlaylistId)
                        print(f'{result}--{self.currentPlaylistId}')
                        if result is False:
                            # playlist data extraction
                            self.playlistVideoIdData[self.currentPlaylistId] = []
                        else:
                            # channels data extraction
                            self.channelVideoIdData[self.currentPlaylistId] = []

            # trying to get each video id  in playlist only
            if '[youtube]' in str(msg) and 'Downloading webpage' in str(msg):
                # [youtube] ESKmMtG-zYY: Downloading webpage
                videoId = str(msg).split(" ")[1].replace(":", "").strip()
                if self.currentPlaylistId != "":
                    ans = '@' in str(self.currentPlaylistId)
                    if ans is False:
                        # playlist data
                        self.playlistVideoIdData[self.currentPlaylistId].append(videoId)
                    else:
                        # channels data
                        self.channelVideoIdData[self.currentPlaylistId].append(videoId)

                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                print()
                print(self.playlistVideoIdData)
                print(self.channelVideoIdData)
                print()
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

            if '[download] Downloading video' in str(msg) and 'of' in str(msg):
                self.video_counter += 1
                # if self.video_counter > 5:
                #     signal.signal(signal.SIGTERM, youtube_dl.YoutubeDL.download)

                all = str(msg).split(" of ")[-1].strip()
                if all not in self.total:
                    self.total.append(all)
                    print()
                    print(f"[[[[ {self.total} ]]]]")
                    print()

            if '[download]' in str(msg):
                self.mainmsg = str(msg).replace('[download]', "").replace("Downloading", "Extracting Data for")
            else:
                self.submsg = str(msg).split(":")[1].replace("tab]", "Analyzing ")
                # self.submsg = "Analysing the url..."

                # print(msg)
            if self.mainmsg != "":
                if len(self.total) <= 1:
                    self.innerMessage = f"[ PLAYLIST DETECTED ] - {self.video_counter} Videos\n[ {self.mainmsg} ] {self.submsg}"
                else:
                    self.innerMessage = f"[ MULTIPLE PLAYLIST OR CHANNEL DOWNLOAD DETECTED ] - {len(
                        self.total)} playlists : {self.video_counter} Videos\n[ {self.mainmsg} ] {self.submsg}"

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
