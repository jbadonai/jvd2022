from environment import Config
import requests
from videoDatabase import VideoDatabase
import json

# server = Config().config("LOCAL_SERVER_ADDRESS")
server = Config().config("AWS_SERVER_ADDRESS")
ngrok_server = "https://8d59-41-190-12-99.eu.ngrok.io/"
# server = "https://jbadonai-server.el.r.appspot.com/"


class ApiCalls():
    def __init__(self):
        self.server = Config().config('SERVER_ADDRESS')

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

    def initialize_ngrok(self, ngrok_address):
        header = {'ngrok-skip-browser-warning': 'True'}
        result = requests.get(url=ngrok_address, headers=header)


    def is_server_reachable(self):
        try:
            # self.initialize_ngrok()

            result = requests.get(server)
            status_code = result.status_code
            text = result.text
            if status_code == 200:
                return True
            return False
        except Exception as e:
            return False

    def get_data_by_system_id(self, system_id):
        try:
            # query system id on the server
            result = requests.get(f"{server}client/{system_id}")

            # convert server response to dictionary
            data = self._get_data_from_result(result)

            # return data if no error
            return data

        except Exception as e:
            return None

    def get_user_by_id(self, id):
        try:
            # query system id on the server
            result = requests.get(f"{server}user/?id={id}")

            # convert server response to dictionary
            data = self._get_data_from_result(result)

            # return data if no error
            return data

        except Exception as e:
                return None

    def get_user_by_email(self, email):
        try:
            # query system id on the server
            result = requests.get(f"{server}user/?email={email}")

            # convert server response to dictionary
            data = self._get_data_from_result(result)

            # return data if no error
            return data

        except Exception as e:
                return None

    def generate_license_and_send_email(self, systemId, systemKey, email):
        try:
            # query system id on the server
            result = requests.get(f"{server}license/?systemId={systemId}&systemKey={systemKey}&email={email}")
            data = json.loads(result.text)
            return data

        except Exception as e:
            return None

    def create_new_client(self, data):
        result = requests.post(f"{server}client/", json=data)

        return result

        pass

    def create_new_user(self, user_data):
        result = requests.post(f"{server}user", json=user_data )

        if result.status_code == 201:
            return result.text
        else:
            print(f'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            print(result.text)
            return None

