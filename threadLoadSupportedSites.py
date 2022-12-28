from PyQt5 import QtCore
import supported_sites
import time


class SupportedSitesLoaderThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, myself):
        super(SupportedSitesLoaderThread, self).__init__()
        self.emit_data ={}
        self.myself = myself
        pass

    def run(self):
        try:
            ss = supported_sites.get_supported_site()
            total = len(ss)
            col = 4
            row = round(total / col) + 1

            counter = 0
            for i in range(1, row):
                for j in range(1, col + 1):
                    try:
                        # self.emit_data['text'] =ss[counter].split(":")[0]
                        if len(ss[counter]) > 50:
                            tooltip = ss[counter]
                            self.emit_data['text'] =f"{ss[counter][:100]}..."

                        else:
                            self.emit_data['text'] =f"{ss[counter]}"
                            tooltip = None

                        self.emit_data['row'] = i
                        self.emit_data['col'] = j
                        self.emit_data['tooltip'] = tooltip
                        counter += 1
                        # print(self.emit_data)
                        self.myself.ss_loader_busy = True
                        self.any_signal.emit(self.emit_data)

                        while True:
                            if self.myself.ss_loader_busy is False:
                                break
                            time.sleep(0.01)

                    except:
                        continue

            self.emit_data['completed'] = True
            self.any_signal.emit(self.emit_data)
        except Exception as e:
            pass

