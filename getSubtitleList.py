import yt_dlp as youtube_dl
from PyQt5 import QtCore
import time


class GetSubtitleList():
    def __init__(self, url):
        # self.myparent = myparent
        self.threadController = {}
        self.url = url

    def get_subtitle_list(self):
        def get_list_connector(data):
            print(data)
            pass

        self.threadController['get_list'] = ThreadGetSubtitleList(self.url)
        self.threadController['get_list'].start()
        self.threadController['get_list'].any_signal.connect(get_list_connector)


class ThreadGetSubtitleList(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, url):
        super(ThreadGetSubtitleList, self).__init__()
        self.data_emit = {}
        self.url = url
        print('here3')

    def get_subtitle_list(self, url):
        subtitle_lang = []
        ydl_opts = {
            'postprocesor-args': 'loglevel quiet, -8',
            'nopart': True,
            'quiet': True,
            'ignoreerrors': True,
            'subtitle': '--list-subs --skip-download',
        }

        # Extract video info
        # -----------------------
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print()
            subtitle = info['subtitles']
            print(len(subtitle))
            for i in subtitle:
                # print(i)
                subtitle_lang.append(i)
                # print()

        return subtitle_lang

    def run(self):
        print('here22')
        try:
            print('here22')
            ans = self.get_subtitle_list(self.url)

            if len(ans) > 0:
                self.data_emit['subtitle'] = ans
                self.any_signal.emit(self.data_emit)
                print(ans)
            else:
                self.data_emit['subtitle'] = None
                self.any_signal.emit(self.data_emit)
                print(None)
            pass
        except Exception as e:
            print(e)
            pass



