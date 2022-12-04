
from generalFunctions import GeneralFunctions
from apiCalls import ApiCalls
from PyQt5 import QtCore
from exceptionList import *
from dialogs import RegisterDialog
import json
from environment import Config
from videoDatabase import VideoDatabase
from dialogs import MessageBox
from security import JBEncrypter, LicenseGenerator
import time


class Authentications():
    def __init__(self, myself):
        self.generalFunction = GeneralFunctions()
        self.api = ApiCalls()
        self.authThread = {}
        self.msgBox = MessageBox()
        self.myself = myself
        pass

    def check_me_on_server(self):

        def check_on_server_connector(data):
            try:
                print(f"[ data ] :>>>>>>>>>>>>>> { data}")
                if 'error' in data:
                    errordetails = data['error']
                    self.msgBox.show_information("Error!", str(errordetails))
                    raise SoftLandingException

                if 'new_user' in data:
                    newUser = data['new_user']
                    if newUser is True:
                        # start user registration process
                        self.register_new_user()
                    else:
                        ans = data['settings_applied']
                        if ans is True:
                            # self.msgBox.show_information("Updated!", "Client Updated Successfully with data from Server")
                            pass



                pass
            except SoftLandingException:
                pass
            except Exception as e:
                print(f"An error occurred in check on server connector: {e}")
                self.msgBox.show_information("Unhandled Exception!", f"An unhandled error occcured in C.O.S_connector! see details below: \n\n {e}")
                pass

        self.authThread['check me on server'] = CheckMeOnServerThread()
        self.authThread['check me on server'].start()
        self.authThread['check me on server'].any_signal.connect(check_on_server_connector)

    def register_new_user(self):

        def register_connector(data):
            if 'error' in data:
                self.msgBox.show_information("Error!", data['error'])
            if 'registration_status' in data:
                if data['registration_status'] == "Failed":
                    msg = data['details']
                    self.msgBox.show_information("Registration Failed!", f"Registration Failed! \n\nDetails:\n{msg}")
                else:
                    self.msgBox.show_information("Registration Successful!", f"User Registration was Successful!")


            pass

        new_user_data ={}
        try:
            # get registration data
            dialog = RegisterDialog()
            if dialog.exec():
                new_user_data.update(dialog.data)
            else:
                raise DialogCanceledException

            self.msgBox.show_information("Info!", "User Registration in progress! \n\n"
                                                  "We will try to apply your license key to this application once the "
                                                  "registration is successful. But if this fails Please check your "
                                                  "mail for license key and follow the instruction in the mail to "
                                                  "apply your license key.")

            # process the data for new user in a thread
            self.authThread['register'] = RegisterNewUserThread(new_user_data=new_user_data)
            self.authThread['register'].start()
            self.authThread['register'].any_signal.connect(register_connector)
        except DialogCanceledException:
            pass
        except:
            pass

    def monitor_license_key(self):
        def monitor_key_connector(data):
            pass

        self.authThread['monitor_license'] = MonitorKeyThread(myself=self.myself)
        self.authThread['monitor_license'].start()
        self.authThread['monitor_license'].any_signal.connect(monitor_key_connector)

    def stop_monitoring_license_key(self):
        self.authThread['monitor_license'].stop()


# :::::::::::::::::>    THREADS BEGINS HERE <::::::::::::::::::::::::::::::::::::::::

class CheckMeOnServerThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(CheckMeOnServerThread, self).__init__()
        self.api = ApiCalls()
        self.generalFunction = GeneralFunctions()
        self.emit_data ={'new_user': False}
        self.emit_data['settings_applied'] = False

    def stop(self):
        try:
            self.requestInterruption()
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass

    def run(self):
        try:
            print(f"[][][][][ checking ")
            #   1. Check if Server is reachable
            api_reachable = self.api.is_server_reachable()
            if api_reachable is False:
                raise ServerNotReachableException

            #   2. Get system Id on local machine
            local_machine_system_id = self.generalFunction.get_this_machine_id()['id']

            #   3. get system id details from server
            system_id_data = self.api.get_data_by_system_id(local_machine_system_id)

            #   4. check if system id Exist. result will be None if it does not exist
            if system_id_data is not None:  # i.e system id found on server
                #   A. Get user details with this system id
                user_id = system_id_data['owner_id']
                user_data = self.api.get_user_by_id(user_id)
                print(f"user_data:>>>>> {user_data}")
                print(f"system id data:>>>> {system_id_data}")

                # update settings on this machine with the user data found
                ans = self.generalFunction.apply_user_to_this_machine(user_data=user_data, client_data=system_id_data)

                self.emit_data['new_user'] = False
                self.emit_data['settings_applied'] = ans    # gives feedback to the user
                self.any_signal.emit(self.emit_data)

            else:   # i.e System Id not found on the server
                #   A. request for registration (start user registration process)
                self.emit_data['new_user'] = True
                self.any_signal.emit(self.emit_data)
                # now go to process that will create a new user in a new thread
                print(f"[][][][]System ID NOT on server!")

        except ServerNotReachableException:
            self.emit_data['error'] = "Server is not Reachable to confirm your license status. \n\n" \
                                      "1. Please make sure your PC has an active internet connection.\n\n" \
                                      "2. If you have registered, Please check your mail for your license key and instruction on how to apply it.\n\n" \
                                      "3. If you have not registered. Please click 'Activate' button to start.\n\n" \
                                      "If the problem persists, the licensing server might down temporarily. Please " \
                                      "Try again latter or contact jbadonaiventures@yahoo.com to report this error."
            self.any_signal.emit(self.emit_data)
        except:
            pass


class RegisterNewUserThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, new_user_data):
        super(RegisterNewUserThread, self).__init__()
        self.username = new_user_data['username']
        self.email = new_user_data['email']
        self.password = new_user_data['password']
        self.api = ApiCalls()
        self.no_of_clients_allowed = Config().config('NO_OF_CLIENTS_ALLOWED_PER_USER')
        self.emit_data ={}
        self.generalFunction = GeneralFunctions()
        self.database = VideoDatabase()

    def stop(self):
        try:
            self.requestInterruption()
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass

    def attach_this_client_to_user(self, email):
        try:
            #   1. Check if Server is reachable
            api_reachable = self.api.is_server_reachable()
            if api_reachable is False:
                raise ServerNotReachableException

            #   1. Generate activation key and send to the email
            # generate system id and system key
            machineID = self.generalFunction.get_this_machine_id()

            # extract system id and system key
            systemID = machineID['id']
            systemKey = machineID['key']

            # generate license and send as email
            result = self.api.generate_license_and_send_email(systemId=systemID, systemKey=systemKey, email=email)

            # analyse the result of trying to generate and send email
            result_status = result['detail']['status']
            result_details = result['detail']['detail']
            result_user_license  = result['user_license']

            #   check if code generation and mail sending was successful
            if result_status == "Failed":
                raise EmailSendingException

            #   2. update user with client details (add client details to the list of user)
            #   a. get user > then id > use the id to add client details
            user_details = self.api.get_user_by_email(email=email)
            user_id = user_details['id']

            new_client_data = {
                      "systemId": systemID,
                      "systemKey": systemKey,
                      "trialLicenseKey": result_user_license,
                      "fullLicenseKey": "",
                      "trialExpired": False,
                      "trialActivated": False,
                      "active": False,
                      "messageSentSuccessfully": True,
                      "owner_id": user_id
                    }

            new_client_result = self.api.create_new_client(new_client_data)

            if new_client_result.status_code != 201: # successfully created
                raise NewClientCreationException

            #   3. update settings on this pc with this client details
            self.database.update_setting('system_id', new_client_data['systemId'])
            self.database.update_setting('system_key', new_client_data['systemKey'])
            self.database.update_setting('trial_key', new_client_data['trialLicenseKey'])
            self.database.update_setting('license_key', new_client_data['fullLicenseKey'])
            self.database.update_setting('trial_expired', new_client_data['trialExpired'])
            self.database.update_setting('trial_activated', new_client_data['trialActivated'])
            self.database.update_setting('active', new_client_data['active'])
            self.database.update_setting('message_sent_successfully', new_client_data['messageSentSuccessfully'])
            self.database.update_setting('owner', email)

            return True,None

        except EmailSendingException:
            print(result_details)
            return False, result_details
            pass
        except ServerNotReachableException:
            self.emit_data['error'] = "Updating User with new client data failed because Server is not Reachable. Please Try again latter"
            self.any_signal.emit(self.emit_data)
        except NewClientCreationException:
            return False
            pass
        except:
            pass

    def run(self):
        try:
            #   1. Check if Server is reachable
            api_reachable = self.api.is_server_reachable()
            if api_reachable is False:
                raise ServerNotReachableException

            #   1. Check if email exists already on the server. this returns none if email not on server and
            # returns user data with the email if it exists on the server.
            serverUserData = self.api.get_user_by_email(self.email)

            if serverUserData is not None:  # i.e. user with email exists on the server
                #   A. Check no of clients attached to this user (email)

                # converts the data from server into a dictionary for processing in python
                if type(serverUserData) != dict:
                    data = json.loads(serverUserData)
                else:
                    data = serverUserData

                clients = data['clients']
                noOfClients = len(clients)

                if noOfClients > self.no_of_clients_allowed:
                    # do not register this user! Abort registration process
                    self.emit_data['registration_status'] = "Failed"
                    self.emit_data['details'] = f"No of clients allowed has been exceeded for user {self.email}"
                    self.any_signal.emit(self.emit_data)
                else:
                    # attach this client to the the user(email)
                    result1 = self.attach_this_client_to_user(self.email)
                    if result1[0] is True:
                        self.emit_data['registration_status'] = "Success"
                        self.any_signal.emit(self.emit_data)
                    else:
                        self.emit_data['registration_status'] = "Failed"
                        self.emit_data['details'] = f"{result1[1]}"
                        self.any_signal.emit(self.emit_data)

            else:
                # user with email does not exist on server as well as system id
                #   1. Register this new user on the server
                user_data = {
                          "name": self.username,
                          "email": self.email,
                          "password": self.password
                        }
                ans = self.api.create_new_user(user_data=user_data)

                if ans is None:
                    raise UserCreationException

                #   2. Generate license key and send to user via email
                #   3. add this client to the user on the server
                #   4. update settings on this pc with this client data
                # implement 2 - 4
                print('attaching client to user on the server..............')
                result = self.attach_this_client_to_user(self.email)
                if result[0] is True:
                    self.emit_data['registration_status'] = "Success"
                    self.any_signal.emit(self.emit_data)
                else:
                    self.emit_data['registration_status'] = "Failed"
                    self.emit_data['details'] = f"{result[1]}"
                    self.any_signal.emit(self.emit_data)

        except UserCreationException:
            self.emit_data['error'] = "New User Creation on Server Failed. Please Try again latter"
            self.any_signal.emit(self.emit_data)
        except ServerNotReachableException:
            self.emit_data['error'] = "Registration failed because Server is not Reachable. Please Try again latter"
            self.any_signal.emit(self.emit_data)
        except Exception as e:
            self.emit_data['error'] = f"Unhandled Error Occurred. Please report details below to jbadonaiventures@yahoo.com: \n\n{e}"
            self.any_signal.emit(self.emit_data)
            pass


class MonitorKeyThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, myself):
        super(MonitorKeyThread, self).__init__()
        self.database = VideoDatabase()
        self.generalFunction = GeneralFunctions()
        self.myself = myself

    def check_license(self):
        try:
            #   1. check and skip this check if app is fully activated
            full_activation = self.generalFunction.is_fully_activated()
            if full_activation is True:
                raise FullyActivatedException

            #   2. check local db if there is a key
            is_lic_key = self.generalFunction.is_there_trial_key()

            if is_lic_key is False:  # i.e. no license key on local db:
                raise InvalidLicenseException

            # i.e. a license key is on the local db:
            # Extract info from the key
            #   a. get the license from db
            lic = self.generalFunction.get_trial_key()

            #   b. decrypt the license
            licDecrypted = JBEncrypter().decrypt(lic, Config().config("ENCRYPT_PASSWORD"))

            # check if license is not valid
            if licDecrypted is None:
                self.myself.disable_downloading()
                raise InvalidLicenseException

            #   c. separate the content/data stored in the user license
            lic_type, email, system_id, system_key, actual_license = licDecrypted.split("'")

            #   d. check if license has expired or not
            result = LicenseGenerator().is_license_expired(actual_license)
            licExpired = result[0]  # license expired status
            licStatus = result[1]  # remaining days in license
            if licExpired is True:
                self.myself.disable_downloading()
                self.myself.labelActivationStatus.setText("Trial License Expired!")
                self.myself.textOwner.setText(email)
                self.myself.frame_license_info.setVisible(True)
                self.myself.buttonActivate.setVisible(True)
            else:
                self.myself.enable_downloading()
                self.myself.labelActivationStatus.setText(f"Your license will expire in {str(licStatus)}")
                self.myself.textOwner.setText(email)
                self.myself.frame_license_info.setVisible(False)
                self.myself.buttonActivate.setVisible(False)

        except FullyActivatedException:
            pass
        except InvalidLicenseException:
            self.myself.labelActivationStatus.setText("Activation Required!")
            self.myself.textOwner.setText('jbadonaiventures')
            self.myself.frame_license_info.setVisible(True)
            self.myself.buttonActivate.setVisible(True)
            pass

    def stop(self):
        try:
            self.requestInterruption()
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass

    def run(self):
        try:
            while True:
                if self.isInterruptionRequested() is True:
                    break

                self.check_license()
                time.sleep(1)
        except Exception as e:
            pass

