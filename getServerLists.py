import pyrebase

class GetServerLists():
    def __init__(self):
        self.firebaseConfig = {
            'apiKey': "AIzaSyCKIe-C7cLgTcQti7-2sjpY8St0ZHkILXI",
            'authDomain': "video-downloader-auth.firebaseapp.com",
            'databaseURL': "https://video-downloader-auth-default-rtdb.firebaseio.com",
            'projectId': "video-downloader-auth",
            'storageBucket': "video-downloader-auth.appspot.com",
            'messagingSenderId': "98278757450",
            'appId': "1:98278757450:web:3c9752f1e27404c5b802b3",
            'measurementId': "G-J6FR4943V9"
        }

        self.firebase = pyrebase.initialize_app(self.firebaseConfig)

        self.db = self.firebase.database()
        self.auth = self.firebase.auth()
        self.storage = self.firebase.storage()

    def authenticate(self,username, password):
        try:
            result = self.auth.sign_in_with_email_and_password(username, password)
            idToken = result['idToken']
            return idToken
        except:
            return None

    # def add_new_server(self,server_name, server_address, token):
    #     try:
    #         data = {'server_address': server_address}
    #
    #         ans = db.child('ServerList').child(f"{server_name}").set(data, token=token)
    #         return True
    #     except:
    #         return False

    def get_server_list(self, username, password):
            try:
                serverList = []
                token = self.authenticate(username, password)
                servers = self.db.child("ServerList").get(token=token)
                for server in servers.each():
                    serverList.append(server.val()['server_address'])

                return serverList
            except:
                return None
                pass
