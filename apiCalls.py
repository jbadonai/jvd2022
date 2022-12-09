from environment import Config
import requests
from videoDatabase import VideoDatabase
import json
from getServerLists import GetServerLists
from PyQt5 import QtCore
import time
from videoDatabase import VideoDatabase
from security import JBEncrypter, JBHash
from exceptionList import *

# default_server = VideoDatabase().get_settings('default_server')
# default_server = JBEncrypter().decrypt(default_server, Config().config('ENCRYPT_PASSWORD'))
server_checker = GetServerLists()


class ApiCalls():
    def __init__(self):
        self.server = self.get_default_server()
        self.serverFound = False
        self.threadController = {}
        self.new_server_found = False
        self.server_search_status = "Started!"

    def get_default_server(self):
        return Config().config('LOCAL_SERVER_ADDRESS')

        default_server = VideoDatabase().get_settings('default_server')
        default_server = JBEncrypter().decrypt(default_server, Config().config('ENCRYPT_PASSWORD'))

        if default_server.__contains__('ngrok'):
            # this helps to remove landing page introduced by ngrok
            self.initialize_ngrok(default_server)

        return default_server

    def look_for_available_server(self):

        def available_server_connector(data):
            print(f"DATA: {data}")
            if 'server' in data:
                self.server = data['server']
                print(f"AVAILABLE SERVERS DETECTED: {self.server}")
                self.new_server_found = True

            if 'message' in data:
                self.server_search_status = data['message']

        self.threadController['search_new_server'] = ServerListCheckerThread(self)
        self.threadController['search_new_server'].start()
        self.threadController['search_new_server'].any_signal.connect(lambda: available_server_connector())

    def _get_data_from_result(self, result):
        # get the server response which might be error or actual data
        text = result.text
        code = result.status_code

        # convert server response to dictionary
        data = json.loads(text)
        # check if server response contains status code which indicate error
        if 'status_code' in data or code != 200:
            return None

        # return data if no error
        return data

    def initialize_ngrok(self, server):
        header = {'ngrok-skip-browser-warning': 'True'}
        result = requests.get(url=server, headers=header)

    def server_list_is_server_reachable(self, server):
        try:
            # self.initialize_ngrok()
            print(f"[DEBUB][STARTUP] - checking '{server}'...")
            result = requests.get(server)
            status_code = result.status_code
            text = result.text
            if status_code == 200:
                return True
            return False
        except Exception as e:
            return False

    def is_server_reachable(self):
        try:
            self.server = self.get_default_server()
            print(f"[DEBUB][STARTUP] - checking '{self.server}'...")
            result = requests.get(self.server)
            status_code = result.status_code
            text = result.text
            print(status_code,"<::::>", text)
            if status_code == 200:
                return True
            return False
        except Exception as e:
            return False

    def get_data_by_system_id(self, system_id):
        try:
            # get updated server
            self.server = self.get_default_server()
            # print(f'[][]DEFAULT SERVER::::> {self.server}:::sid: {system_id}')

            # query system id on the server
            result = requests.get(f"{self.server}client/{system_id}")
            print(f"REsult::::<<>>: {result.text}")
            print(f"REsult::::<<>>: {result}")

            # convert server response to dictionary
            data = self._get_data_from_result(result)

            # return data if no error
            return data

        except Exception as e:
            return None

    def get_user_by_id(self, id):
        try:
            # get updated server
            self.server = self.get_default_server()

            # query system id on the server
            result = requests.get(f"{self.server}user/?id={id}")

            # convert server response to dictionary
            data = self._get_data_from_result(result)

            # return data if no error
            return data

        except Exception as e:
                return None

    def get_user_by_email(self, email):
        try:
            # get updated server
            self.server = self.get_default_server()

            # query system id on the server
            result = requests.get(f"{self.server}user/?email={email}")

            # convert server response to dictionary
            data = self._get_data_from_result(result)

            # return data if no error
            return data

        except Exception as e:
                return None

    def generate_license_and_send_email(self, systemId, systemKey, email):
        try:
            # get updated server
            self.server = self.get_default_server()

            p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))

            # query system id on the server
            result = requests.get(f"{self.server}license/?systemId={systemId}&systemKey={systemKey}&email={email}&pp={p[1]}")
            data = json.loads(result.text)
            return data

        except Exception as e:
            return None

    def create_new_client(self, data):
        # get updated server
        self.server = self.get_default_server()

        p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))

        result = requests.post(f"{self.server}client/?pp={p[1]}", json=data)

        return result

        pass

    def create_new_user(self, user_data):
        # get updated server
        self.server = self.get_default_server()
        p = JBHash().hash_message_with_nonce(Config().config('ENCRYPT_PASSWORD'))
        result = requests.post(f"{self.server}user?pp={p[1]}", json=user_data )

        if result.status_code == 201:
            return result.text
        else:
            print(f'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            print(result.text)
            return None


class ServerListCheckerThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent):
        super(ServerListCheckerThread, self).__init__()
        self.data_emit = {}
        self.myparent = parent
        self.available_servers = []
        pass

    def server_list_is_server_reachable(self,server):
        try:
            # self.initialize_ngrok()
            # print(f"[DEBUB][STARTUP] - checking '{server}'...")
            result = requests.get(server)
            status_code = result.status_code
            text = result.text
            if status_code == 200:
                return True
            return False
        except Exception as e:
            return False

    def check_servers(self):
        try:
            server_list = server_checker.get_server_list(Config().config("SERVER_CHECK_USERNAME"),
                                                         Config().config("SERVER_CHECK_PASSWORD"))
            print(server_list)
            for index, server in enumerate(server_list):
                # trying to give feedback of what is happening here
                self.data_emit['message'] = f"Checking [ {index + 1}/{len(server_list)} ] - {server}"
                self.any_signal.emit(self.data_emit)

                self.myparent.server_search_status =f"Checking [ {index + 1}/{len(server_list)} ] - {server}"

                print(f'checking server: {server}')

                available = self.server_list_is_server_reachable(server)
                print(f"avaiable? --- {available}")
                if available is True:
                    print(f'[{server}] OK')
                    self.available_servers.append(server)
        except:
            pass

    def stop(self):
        try:
            self.requestInterruption()
        except:
            pass

    def run(self):
        self.data_emit['message'] = "Starting now..........................."
        self.any_signal.emit(self.data_emit)
        try:
            print("checking for available server........")

            self.check_servers()
            print()
            print(f"FINAL SERVER OBTAINED IN TRHEAd before emiting: {self.available_servers}")
            self.data_emit['server'] = self.available_servers
            self.any_signal.emit(self.data_emit)
            print(f"it should have been emitted now")
            self.myparent.new_server_found = True

        except Exception as e:
            pass


class FindServerListThread(QtCore.QThread):
    find_server_signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(FindServerListThread, self).__init__()
        self.data_emit = {}
        self.available_servers = []

    def server_list_is_server_reachable(self,server):
        try:
            # self.initialize_ngrok()
            # print(f"[DEBUB][STARTUP] - checking '{server}'...")
            result = requests.get(server)
            status_code = result.status_code
            text = result.text
            if status_code == 200:
                return True
            return False
        except Exception as e:
            return False

    def check_servers(self):
        try:
            server_list = server_checker.get_server_list(Config().config("SERVER_CHECK_USERNAME"),
                                                         Config().config("SERVER_CHECK_PASSWORD"))

            if server_list is None or len(server_list) == 0:
                raise SoftLandingException

            for index, server in enumerate(server_list):
                # trying to give feedback of what is happening here
                self.data_emit['message'] = f"Checking [ {index + 1}/{len(server_list)} ] - {server}"
                self.find_server_signal.emit(self.data_emit)

                available = self.server_list_is_server_reachable(server)
                if available is True:
                    self.available_servers.append(server)

        except SoftLandingException:
            pass
        except:
            pass

    def stop(self):
        try:
            self.requestInterruption()
        except:
            pass

    def run(self):
        try:
            print("checking for available server........")
            self.check_servers()
            self.data_emit['server'] = self.available_servers
            self.find_server_signal.emit(self.data_emit)
        except Exception as e:
            pass
