import yt_dlp as youtube_dl     #yt-dlp-2022.1.21, yt-dlp 2022.3.8.2 ---- yt-dlp==2022.8.19
import os
import subprocess
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import time
import signal
from dialogs import MessageBox
from videoDatabase import VideoDatabase

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
            self.milestone = False
            self.emit_data['milestone'] = False

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

                if self.milestone is True:

                    self.emit_data['milestone'] = True
                    self.any_signal.emit(self.emit_data)
                    time.sleep(1)
                    self.milestone = False
                else:
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

    def get_url_type(self, info):
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

            # > set info extraction/ download options
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

            # > Extract video info
            # -----------------------
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            # > Process the video info
            # -----------------------------
            if info is not None:
                # get url type: single, playlist or channel
                urlType = self.get_url_type(info)

                if urlType == 'channel':
                    self.process_channel_entries(info, url)
                else:
                    self.process_non_channel_entries(info, url)
            else:
                self.entry_messages = f"Error!:{self.info_logger.innerErrorMessage}"
                self.is_running = False

            self.myself.busy = False
            self.is_running = False

            # reset channel info for next url to be added
            self.myself.channelDownload = False
            self.myself.channelName = None
        except Exception as e:
            self.myself.busy = False
            print(f"An Error Occurred in getEntryThread >  'get download entries' : {e}")

    def process_channel_entries(self, info, url):
        try:
            try:
                channel_name = str(info['entries'][0]['entries'][0]['channel']).replace(" ","_")
                url_basename = str(info['entries'][0]['entries'][0]['webpage_url_basename']).replace(" ","_")
                # to be used in main window to create a folder for channel downloads
                self.myself.channelDownload = True
                self.myself.channelName = f"{channel_name}__{url_basename}"
            except Exception as e:
                print(e)
                input('wait for error:')


            channels_entries = info['entries'][0]['entries']

            # test purpose
            for index, c in enumerate(channels_entries):
                with open(f"testFolder\\Channels - {index}", 'w', encoding='utf-8') as f:
                    f.write(str(c))

            for playlist_data in channels_entries:
                url = playlist_data['webpage_url']
                info = playlist_data

                self.process_non_channel_entries(info, url)


        except Exception as e:
            print(f"An Error Occurred in 'Proccess Channel Entries': {e}")
        pass

    def process_non_channel_entries(self, info, url):
        isPlaylist = None
        common_title = ""
        self.availableFormat.clear()
        try:
            self.info_logger.innerMessage = "" # to stop broadcasting inner message

            # 1. > Detect if extracted info is a playlist or single video and set isPlaylist value
            # -----------------------------------------------------------------------------------
            try:
                print(info['requested_entries'])
                isPlaylist = True
            except Exception as e:
                isPlaylist = False

            # 2. > Extracting video data
            # -------------------------------------------------------------
            self.entry_messages = "Extracting Required Video data..."
            self.myself.private_video_count = 0
            available_format = []

            if isPlaylist:
                try:
                    url_basename = str(info['webpage_url_basename']).replace(" ", "_")
                    channel_name = str(info['channel']).replace(" ", "_")
                    # print(url_basename)
                    # input("wait for basename:")
                    if url_basename != 'playlist':
                        self.myself.channelDownload = True
                        self.myself.channelName = f"{channel_name}__{url_basename}"
                except:
                    print(f"E NO DEY.........................................")
                    input("wait for basename:")
                    pass
                # get available video info and push it to main window. also set available formats for playlist video
                self.process_playlist_info(info=info, url=url)
            else:
                # get available video info and push it to main window. also set available formats for non playlist video
                self.process_non_playlist_info(info=info, url=url)

            # 3. > Extract available formats [ update self.available_format here ]
            # ----------------------------------------------------------------
            # push available format to main window for display.
            self.push_available_formats(self.availableFormat)

            # 4. > get the common title [update self.common_title here]
            # ------------------------------------------------------------------------------------
            self.myself.common_title = common_title


            print('finished!')
            # set a signal that a milestone has been completed.
            # it could be the only, any or the last one
            self.milestone = True

            # trigger a settings in main to check if previous milestone process has been completed
            # this help to wait before initiating another one
            self.myself.milestone_ready = False

            # wait for last milestone to be processed before proceeding
            while True:
                if self.myself.milestone_ready is True:
                    break
                time.sleep(0.1)

        except Exception as e:
            print(f"An Error occurred in 'process non channel entries': {e}")

    def process_playlist_info(self, info, url):
        try:
            for d in info['entries']:
                if d is not None:
                    data = {}
                    data['is_playlist'] = True
                    data['title'] = GeneralFunctions().screen_the_title(d['title'])
                    data['url'] = d['webpage_url']
                    data['playlist_index'] = d['playlist_index']
                    data['playlist_title'] = GeneralFunctions().screen_the_title(d['playlist_title'])
                    data['thumbnail'] = d['thumbnail']
                    data['playlist_url'] = url
                    data['available_formats'] = d['formats']
                    data['common_title'] = d['playlist_title']
                    self.push_video_data(data=data)
                else:
                    self.myself.private_video_count += 1  # [ update self.private_video_count here ]
        except Exception as e:
            print(f"An Error Occurred in 'process playlist info': {e}")
        pass

    def process_non_playlist_info(self, info, url):
        try:
            data = {}
            data['is_playlist'] = False
            data['title'] = GeneralFunctions().screen_the_title(info['title'])
            data['url'] = info['webpage_url']
            data['playlist_index'] = None
            data['playlist_title'] = None
            data['thumbnail'] = info['thumbnail']
            data['playlist_url'] = url
            data['common_title'] = data['title']
            try:
                data['available_formats'] = info['formats']
            except:
                data['available_formats'] = info['format']

            self.push_video_data(data=data)

        except Exception as e:
            self.myself.busy = False
            print(f"An Error Occurred in 'process playlist info': {e}")
        pass

    def push_video_data(self, data):
        try:
            # get entry data
            test_url = data['url']
            url_exists = VideoDatabase().is_url_exists_in_database(test_url)
            if url_exists is False:
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
            else:
                self.myself.duplicateVideoEntry += 1
                print("<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o")
                print(f"URL '{test_url}' FOUND SOMEHOW IN THE DATABASE. SKIPPING IT.....")
                print("<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o<>o")
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
        playlist_counter = 0
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
                id = str(msg).split(" ")[1].replace(":","").strip()
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
                            self.channelVideoIdData[self.currentPlaylistId] =[]

            # trying to get each video id  in playlist only
            if '[youtube]' in str(msg) and 'Downloading webpage' in str(msg):
                # [youtube] ESKmMtG-zYY: Downloading webpage
                videoId = str(msg).split(" ")[1].replace(":","").strip()
                if self.currentPlaylistId != "":
                    ans = '@' in str(self.currentPlaylistId)
                    if ans is False:
                        # playlist data
                        self.playlistVideoIdData[self.currentPlaylistId].append(videoId)
                    else:
                        # channels data
                        self.channelVideoIdData[self.currentPlaylistId].append(videoId)

            if '[download] Downloading video' in str(msg) and 'of' in str(msg):
                self.video_counter += 1

                all = str(msg).split(" of ")[-1].strip()
                first = str(msg).split(" of ")[0].strip().split(" ")[-1]

                if int(first) == 1:
                    self.playlist_counter += 1

            if '[download]' in str(msg):
                print(f"[SUB1] -  {str(msg)}")
                self.mainmsg = str(msg).replace('[download]',"").replace("Downloading", "Extracting Data for")
            else:
                print(f"[SUB] -  {str(msg)}")
                self.submsg = str(msg).split(":")[1].replace("tab]","Analyzing ")
                self.submsg = self.submsg.replace("Downloading android player API JSON", "Analyzing JSON...")
                self.submsg = self.submsg.replace("Downloading webpage", "Scanning webpage...")
                # self.submsg = "Analysing the url..."

                # print(msg)
            if self.mainmsg != "":
                if self.playlist_counter <= 1:
                    self.innerMessage = f"[ PLAYLIST DETECTED ] - {self.video_counter} Videos\n[ {self.mainmsg} ] {self.submsg}"
                else:
                    self.innerMessage = f"[ MULTIPLE PLAYLIST OR CHANNEL DOWNLOAD DETECTED ] - {self.playlist_counter} playlists : {self.video_counter} Videos\n[ {self.mainmsg} ] {self.submsg}"

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
