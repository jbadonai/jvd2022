
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
import random


class Authentications():
    def __init__(self, myself):
        self.generalFunction = GeneralFunctions()
        self.api = ApiCalls()
        self.authThread = {}
        self.msgBox = MessageBox()
        self.myself = myself
        # self.activation_in_progress = self.myself.activation_in_progress
        self.message = "Activation Required! \nChecking for existing License. Please Wait ..."
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
                        print(f"[DEBUB][STARTUP] - Registration process started in check_on_server_connector()")
                        self.register_new_user()
                    else:
                        self.myself.activation_in_progress = False
                        print(f"[DEBUB][STARTUP] - server settings applied to system completed. check_me_on_server()")
                        ans = data['settings_applied']
                        if ans is True:
                            # self.msgBox.show_information("Updated!", "Client Updated Successfully with data from Server")
                            pass



                pass
            except SoftLandingException:
                pass
            except Exception as e:
                print(f"An error occurred in check on server connector: {e}")
                enc = JBEncrypter().encrypt(str(e), Config().config('ENCRYPT_PASSWORD'))
                self.msgBox.show_information("Unhandled Exception!", f"An unhandled error occcured in C.O.S_connector! copy and send details below to jbadonaiventures@gmail.com: \n\n {e}")
                pass

        self.authThread['check me on server'] = CheckMeOnServerThread(parent=self)
        self.authThread['check me on server'].start()
        self.authThread['check me on server'].any_signal.connect(check_on_server_connector)

    def check_me_on_server_with_license(self, user_license):

        def check_with_license_connector(data):
            try:
                print(f"[ data ] :>>>>>>>>>>>>>> { data}")
                if 'error' in data:
                    errordetails = data['error']
                    self.msgBox.show_information("Error!", str(errordetails))
                    raise SoftLandingException

                if 'license_activation_status' in data:
                    status = data['license_activation_status']

                    if status == "Failed":
                        self.myself.activation_in_progress = False
                        details = data['details']
                        self.myself.textLicense.clear()
                        self.msgBox.show_information("Failed!", f"License activation Failed!\n\n{details}")
                    else:
                        self.myself.activation_in_progress = False
                        self.msgBox.show_information("Success!", "License Activation was successful!")


            except SoftLandingException:
                self.myself.activation_in_progress = False
                pass
            except Exception as e:
                self.myself.activation_in_progress = False
                print(f"An error occurred in check on server connector: {e}")
                enc = JBEncrypter().encrypt(str(e), Config().config('ENCRYPT_PASSWORD'))
                self.msgBox.show_information("Unhandled Exception!", f"An unhandled error occcured in C.O.S_connector! copy and send details below to jbadonaiventures@gmail.com: \n\n {e}")
                pass

        self.authThread['check me with license'] = CheckMeWithLicenseThread(parent=self, user_license=user_license)
        self.authThread['check me with license'].start()
        self.authThread['check me with license'].any_signal.connect(check_with_license_connector)

    def register_new_user(self):

        def register_connector(data):
            if 'error' in data:
                self.msgBox.show_information("Error!", data['error'])
                self.myself.activation_in_progress = False
            if 'registration_status' in data:
                if data['registration_status'] == "Failed":
                    msg = data['details']
                    self.msgBox.show_information("Registration Failed!", f"Registration Failed! \n\nDetails:\n{msg}")
                    self.myself.activation_in_progress = False
                else:
                    self.msgBox.show_information("Registration Successful!", f"User Registration was Successful!")
                    self.myself.activation_in_progress = False

            pass

        new_user_data ={}
        try:
            print(f"[DEBUB][STARTUP] - showing user registration dialog")
            self.message = "Activation Required! \nRegistration Started! Please Fill the form shown!"
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
            print(f"[DEBUB][STARTUP] - information obtained! processing registration in a new thread")
            # process the data for new user in a thread
            self.authThread['register'] = RegisterNewUserThread(new_user_data=new_user_data, parent=self)
            self.authThread['register'].start()
            self.authThread['register'].any_signal.connect(register_connector)
        except DialogCanceledException:
            print(f"[DEBUB][STARTUP] - registration canceled by user")
            self.myself.activation_in_progress = False
            pass
        except Exception as e:
            enc = JBEncrypter().encrypt(str(e), Config().config('ENCRYPT_PASSWORD'))
            print(f"[DEBUB][STARTUP] - unhandled Exception in Authentication > register_new_user(): {enc}")
            pass

    def monitor_license_key(self):
        def monitor_key_connector(data):
            pass

        self.authThread['monitor_license'] = MonitorKeyThread(myself=self.myself, parent=self)
        self.authThread['monitor_license'].start()
        self.authThread['monitor_license'].any_signal.connect(monitor_key_connector)

    def stop_monitoring_license_key(self):
        self.authThread['monitor_license'].stop()


# :::::::::::::::::>    THREADS BEGINS HERE <::::::::::::::::::::::::::::::::::::::::

class CheckMeOnServerThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent):
        super(CheckMeOnServerThread, self).__init__()
        self.generalFunction = GeneralFunctions()
        self.emit_data ={'new_user': False}
        self.emit_data['settings_applied'] = False
        self.myparent = parent  # refres to Authentication class
        # self.api = self.myparent.api
        self.api = ApiCalls()

    def stop(self):
        try:
            self.requestInterruption()
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass

    def run(self):
        try:
            #   1. Check if Server is reachable
            print(f"[DEBUB][STARTUP] - checking if Server is reachable")

            self.myparent.message = "Activation Required! \nContacting Server! Please wait..."
            trials = 0

            # try about 5 times to get working server
            while True:
                trials += 1

                api_reachable = self.api.is_server_reachable()

                #   if the server not reachable
                if api_reachable is False:
                    self.myparent.message = f"Activation Required! \nDefault Server Not reachable! Searching for available backup server. Please wait..."

                    # Check if there is list of available servers in the database
                    available_servers = GeneralFunctions().get_server_list_from_db()

                    if len(available_servers) > 0:
                        # if tested server is available
                        # Get the first one
                        print(f"total servers active: {len(available_servers)}")
                        if len(available_servers) > 1:
                            # try to select a random server from among the available one for this user
                            # to prevent overloading a server if there are multiple availablepr
                            serverNo = random.randint(0, len(available_servers)-1)
                            print(f"Random number choosen: {serverNo}")

                            active_server = available_servers[serverNo]
                            print(f"active server choosen: {active_server}")
                        else:
                            active_server = available_servers[0]
                            print(f"active server choosen: {active_server}")

                        print(f"Server picked ===== >>> {active_server}")

                        # encrypt it
                        encrypt_active_server = JBEncrypter().encrypt(active_server, Config().config('ENCRYPT_PASSWORD'))

                        # save it as default server
                        VideoDatabase().update_setting('default_server', encrypt_active_server)

                    # then try again.
                else:
                    break

                if trials >= 5:
                    # if have tried several times without success raise error
                    print(f"[DEBUB][STARTUP][E] - SERVER NOT REACHABLE")
                    raise ServerNotReachableException

                time.sleep(1)

            self.myparent.message = "Activation Required! \nServer Found! Checking License Info. Please Wait.."
            print(f"[DEBUB][STARTUP] - SERVER OK. Getting machine system id")
            #   2. Get system Id on local machine
            local_machine_system_id = self.generalFunction.get_this_machine_id()['id']

            print(f"[DEBUB][STARTUP] - Checking if system id exists on server")
            #   3. get system id details from server
            system_id_data = self.api.get_data_by_system_id(local_machine_system_id)
            print(f"systemIdData::::<<<<>>>>>: {system_id_data}")

            #   4. check if system id Exist. result will be None if it does not exist
            if system_id_data is not None:  # i.e system id found on server
                print(f"[DEBUB][STARTUP] - System ID found on the server! Getting user attahed...")
                #   A. Get user details with this system id
                user_id = system_id_data['owner_id']
                user_data = self.api.get_user_by_id(user_id)
                print(f"user_data:>>>>> {user_data}")
                print(f"system id data:>>>> {system_id_data}")

                print(f"[DEBUB][STARTUP] - updating this machine with server data")
                # update settings on this machine with the user data found
                ans = self.generalFunction.apply_user_to_this_machine(user_data=user_data, client_data=system_id_data)

                print(f"[DEBUB][STARTUP] - No new user required returned from CheckMeOnServerThread")
                self.emit_data['new_user'] = False
                self.emit_data['settings_applied'] = ans    # gives feedback to the user
                self.any_signal.emit(self.emit_data)

            else:   # i.e System Id not found on the server
                print(f"[DEBUB][STARTUP] - System ID Not found on server")
                #   A. request for registration (start user registration process)
                print(f"[DEBUB][STARTUP] - New user required returned form CheckMeOnServerThread")
                self.emit_data['new_user'] = True
                self.any_signal.emit(self.emit_data)
                # now go to process that will create a new user in a new thread
                print(f"[][][][]System ID NOT on server!")

        except ServerNotReachableException:
            print(f"[DEBUB][STARTUP] - Server Not Reachable Exception in CheckMeOnServerThread")
            self.myparent.myself.activation_in_progress = False
            self.myparent.message = "Activation Required! \nServer Not Reachable! Please click 'Activate' button to try again latter."
            self.emit_data['error'] = "Server is not Reachable to confirm your license status. \n\n" \
                                      "1. Please make sure your PC has an active internet connection.\n\n" \
                                      "2. If you have registered, Please check your mail for your license key and instruction on how to apply it.\n\n" \
                                      "3. If you have not registered. Please click 'Activate' button to start.\n\n" \
                                      "If the problem persists, the licensing server might be down temporarily. Please " \
                                      "Try again latter or contact jbadonaiventures@yahoo.com to report this error."
            self.any_signal.emit(self.emit_data)
        except:
            pass


class CheckMeWithLicenseThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent, user_license):
        super(CheckMeWithLicenseThread, self).__init__()
        self.generalFunction = GeneralFunctions()
        self.emit_data ={'new_user': False}
        self.emit_data['settings_applied'] = False
        self.myparent = parent  # refres to Authentication class
        self.api = ApiCalls()
        self.no_of_clients_allowed = Config().config('NO_OF_CLIENTS_ALLOWED_PER_USER')
        self.license = user_license
        self.database = VideoDatabase()
        self.user_license_dec = JBEncrypter().decrypt(self.license, Config().config('ENCRYPT_PASSWORD'))
        self.licType, self.licEmail, self.licSystemId, self.licSystemKey, self.licUserLicense = self.user_license_dec.split("'")

    def stop(self):
        try:
            self.requestInterruption()
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass


    def attach_this_client_to_user(self, email):
        try:
            #   1. Check if Server is reachable
            print(f"[DEBUB][LICENSE ACTIVATION] - Checking if server is still reachable before attaching client to user")
            api_reachable = self.api.is_server_reachable()
            if api_reachable is False:
                raise ServerNotReachableException

            #   1. Generate activation key and send to the email
            # generate system id and system key
            machineID = self.generalFunction.get_this_machine_id()

            # extract system id and system key
            systemID = machineID['id']
            systemKey = machineID['key']

            # print(f"[DEBUB][STARTUP][REGISTRATION] - Generate and send license on server...")
            # # generate license and send as email
            # result = self.api.generate_license_and_send_email(systemId=systemID, systemKey=systemKey, email=email)
            #
            # # analyse the result of trying to generate and send email
            # result_status = result['detail']['status']
            # result_details = result['detail']['detail']
            result_user_license  = self.license

            # #   check if code generation and mail sending was successful
            # if result_status == "Failed":
            #     print(f"[DEBUB][STARTUP][REGISTRATION] - license generation and sending Failed on server")
            #     raise EmailSendingException

            print(f"[DEBUB][LICENSE ACTIVATION] - update pc/server data")
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
            print(f"[DEBUB][LICENSE ACTIVATION] - adding client to user server data")
            new_client_result = self.api.create_new_client(new_client_data)
            print(new_client_result)

            if new_client_result.status_code != 201: # successfully created
                raise NewClientCreationException

            print(f"[DEBUB][STARTUP][REGISTRATION] - updating local settings with user data")
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

            return True, None

        except ServerNotReachableException:
            self.emit_data['error'] = "Updating User with new client data failed because Server is not Reachable. Please Try again latter"
            self.any_signal.emit(self.emit_data)
        except NewClientCreationException:
            return False, None
        except Exception as e:
            return False, e


    def run(self):
        try:
            #   1. Check if Server is reachable
            print(f"[DEBUB][LICENSE ACTIVATION] - checking if Server is reachable")

            self.myparent.message = "Activation Required! \nContacting Server! Please wait..."
            trials = 0

            # try about 5 times to get working server
            while True:
                trials += 1

                api_reachable = self.api.is_server_reachable()

                #   if the server not reachable
                if api_reachable is False:
                    self.myparent.message = f"Activation Required! \nDefault Server Not reachable! Searching for available backup server. Please wait..."

                    # Check if there is list of available servers in the database
                    available_servers = GeneralFunctions().get_server_list_from_db()

                    if len(available_servers) > 0:
                        # if tested server is available
                        # Get the first one
                        print(f"total servers active: {len(available_servers)}")
                        if len(available_servers) > 1:
                            # try to select a random server from among the available one for this user
                            # to prevent overloading a server if there are multiple availablepr
                            serverNo = random.randint(0, len(available_servers)-1)
                            print(f"Random number choosen: {serverNo}")

                            active_server = available_servers[serverNo]
                            print(f"active server choosen: {active_server}")
                        else:
                            active_server = available_servers[0]
                            print(f"active server choosen: {active_server}")

                        print(f"Server picked ===== >>> {active_server}")

                        # encrypt it
                        encrypt_active_server = JBEncrypter().encrypt(active_server, Config().config('ENCRYPT_PASSWORD'))

                        # save it as default server
                        VideoDatabase().update_setting('default_server', encrypt_active_server)

                    # then try again.
                else:
                    break

                if trials >= 5:
                    # if have tried several times without success raise error
                    print(f"[DEBUB][STARTUP][E] - SERVER NOT REACHABLE")
                    raise ServerNotReachableException

                time.sleep(1)

            self.myparent.message = "Activation Required! \nServer Found! Checking License Info. Please Wait.."
            print(f"[DEBUB][LICENSE ACTIVATION] - SERVER OK. Getting machine system id")
            #   2. Get system Id on local machine
            local_machine_system_id = self.generalFunction.get_this_machine_id()['id']

            # 3. check if client attached to email has not been exceeded

            # check the email in the license on the server
            serverUserData = self.api.get_user_by_email(self.licEmail)

            if serverUserData is not None:  # i.e. user with email on the license exists on the server
                #   A. Check no of clients attached to this user (email)
                print(f"[DEBUB][LICENSE ACTIVATION] - checking no of clients attached to user exceeded allowed")

                # converts the data from server into a dictionary for processing in python
                if type(serverUserData) != dict:
                    data = json.loads(serverUserData)
                else:
                    data = serverUserData

                clients = data['clients']
                noOfClients = len(clients)

                if noOfClients > self.no_of_clients_allowed:
                    print(f"[DEBUB][LICENSE ACTIVATION] - client allow exceeded")
                    # do not activate license for this user on this machine! Abort license activation process
                    self.emit_data['license_activation_status'] = "Failed"
                    self.emit_data['details'] = f"No of clients allowed has been exceeded for this user {self.licEmail}"
                    self.any_signal.emit(self.emit_data)
                else:
                    # attach this client to the the user(email)
                    print(f"[DEBUB][LICENSE ACTIVATION] - additional client allowed to be added to user")
                    result1 = self.attach_this_client_to_user(self.licEmail)
                    if result1[0] is True:
                        self.emit_data['license_activation_status'] = "Success"
                        self.any_signal.emit(self.emit_data)
                    else:
                        self.emit_data['license_activation_status'] = "Failed"
                        self.emit_data['details'] = f"{result1[1]}"
                        self.any_signal.emit(self.emit_data)

            else:
                self.emit_data['license_activation_status'] = "Failed"
                self.emit_data['details'] = "License supplied is not Allowed! Please Click 'Activate' button to get your free trial license"
                self.any_signal.emit(self.emit_data)
                pass

        except ServerNotReachableException:
            print(f"[DEBUB][STARTUP] - Server Not Reachable Exception in CheckMeOnServerThread")
            self.myparent.myself.activation_in_progress = False
            self.myparent.message = "Activation Required! \nServer Not Reachable! Please click 'Activate' button to try again latter."
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

    def __init__(self, new_user_data, parent):
        super(RegisterNewUserThread, self).__init__()
        self.username = new_user_data['username']
        self.email = new_user_data['email']
        self.password = new_user_data['password']
        self.api = ApiCalls()
        self.no_of_clients_allowed = Config().config('NO_OF_CLIENTS_ALLOWED_PER_USER')
        self.emit_data ={}
        self.generalFunction = GeneralFunctions()
        self.database = VideoDatabase()
        self.myparent = parent
        # self.api = self.myparent.api

    def stop(self):
        try:
            self.requestInterruption()
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass

    def attach_this_client_to_user(self, email):
        try:
            #   1. Check if Server is reachable
            print(f"[DEBUB][STARTUP][REGISTRATION] - Checking if server is still reachable before attaching client to user")
            api_reachable = self.api.is_server_reachable()
            if api_reachable is False:
                raise ServerNotReachableException

            #   1. Generate activation key and send to the email
            # generate system id and system key
            machineID = self.generalFunction.get_this_machine_id()

            # extract system id and system key
            systemID = machineID['id']
            systemKey = machineID['key']

            print(f"[DEBUB][STARTUP][REGISTRATION] - Generate and send license on server...")
            # generate license and send as email
            result = self.api.generate_license_and_send_email(systemId=systemID, systemKey=systemKey, email=email)

            # analyse the result of trying to generate and send email
            result_status = result['detail']['status']
            result_details = result['detail']['detail']
            result_user_license  = result['user_license']

            #   check if code generation and mail sending was successful
            if result_status == "Failed":
                print(f"[DEBUB][STARTUP][REGISTRATION] - license generation and sending Failed on server")
                raise EmailSendingException

            print(f"[DEBUB][STARTUP][REGISTRATION] - update pc/server data")
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
            print(f"[DEBUB][STARTUP][REGISTRATION] - adding client to user server data")
            new_client_result = self.api.create_new_client(new_client_data)
            print(new_client_result)

            if new_client_result.status_code != 201: # successfully created
                raise NewClientCreationException

            print(f"[DEBUB][STARTUP][REGISTRATION] - updating local settings with user data")
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
            print(f"[DEBUB][STARTUP] - checking if server is reachable before starting registration")
            api_reachable = self.api.is_server_reachable()
            if api_reachable is False:
                raise ServerNotReachableException

            self.myparent.message = "Registration in progress! Please Wait..."
            #hide activation button:
            self.myparent.myself.buttonActivate.setVisible(False)

            print(f"[DEBUB][STARTUP][REGISTRATION] - SERVER REACHABLE! checking if email to be registered exist on server")
            #   1. Check if email exists already on the server. this returns none if email not on server and
            # returns user data with the email if it exists on the server.
            serverUserData = self.api.get_user_by_email(self.email)

            if serverUserData is not None:  # i.e. user with email exists on the server
                #   A. Check no of clients attached to this user (email)
                print(f"[DEBUB][STARTUP]REGISTRATION] - checking no of clients attached to user exceeded allowed")

                # converts the data from server into a dictionary for processing in python
                if type(serverUserData) != dict:
                    data = json.loads(serverUserData)
                else:
                    data = serverUserData

                clients = data['clients']
                noOfClients = len(clients)

                if noOfClients > self.no_of_clients_allowed:
                    print(f"[DEBUB][STARTUP][REGISTRATION] - client allow exceeded")
                    # do not register this user! Abort registration process
                    self.emit_data['registration_status'] = "Failed"
                    self.emit_data['details'] = f"No of clients allowed has been exceeded for user {self.email}"
                    self.any_signal.emit(self.emit_data)
                else:
                    # attach this client to the the user(email)
                    print(f"[DEBUB][STARTUP][REGISTRATION] - additional client allowed to be added to user")
                    result1 = self.attach_this_client_to_user(self.email)
                    if result1[0] is True:
                        self.emit_data['registration_status'] = "Success"
                        self.any_signal.emit(self.emit_data)
                    else:
                        self.emit_data['registration_status'] = "Failed"
                        self.emit_data['details'] = f"{result1[1]}"
                        self.any_signal.emit(self.emit_data)

            else:
                print(f"[DEBUB][STARTUP][REGISTRATION] - Email not found on server! New registration to be done")
                # user with email does not exist on server as well as system id
                #   1. Register this new user on the server
                user_data = {
                          "name": self.username,
                          "email": self.email,
                          "password": self.password
                        }
                print(f"[DEBUB][STARTUP][REGISTRATION] - Creating user on the server...")
                ans = self.api.create_new_user(user_data=user_data)

                if ans is None:
                    print(f"[DEBUB][STARTUP][REGISTRATION] - User creation Failed")
                    raise UserCreationException

                #   2. Generate license key and send to user via email
                #   3. add this client to the user on the server
                #   4. update settings on this pc with this client data
                # implement 2 - 4
                print('attaching client to user on the server..............')
                print(f"[DEBUB][STARTUP][REGISTRATION] - attaching this client to the new user created")
                result = self.attach_this_client_to_user(self.email)
                if result[0] is True:
                    self.emit_data['registration_status'] = "Success"
                    self.any_signal.emit(self.emit_data)
                else:
                    self.emit_data['registration_status'] = "Failed"
                    self.emit_data['details'] = f"{result[1]}"
                    self.any_signal.emit(self.emit_data)


        except UserCreationException:
            self.myparent.message = "Activation Required! \nRegistration Failed. Please Try Again!"
            # hide activation button:
            self.myparent.myself.buttonActivate.setVisible(True)

            self.emit_data['error'] = "New User Creation on Server Failed. Please Try again latter"
            self.any_signal.emit(self.emit_data)
        except ServerNotReachableException:
            self.emit_data['error'] = "Registration failed because Server is not Reachable. Please Try again latter"
            self.any_signal.emit(self.emit_data)
        except Exception as e:
            enc = JBEncrypter().encrypt(str(e), Config().config('ENCRYPT_PASSWORD'))
            self.emit_data['error'] = f"Unhandled Error Occurred Register new user Thread. Please copy and report details below to jbadonaiventures@yahoo.com: \n\n{e}"
            self.any_signal.emit(self.emit_data)
            pass


class MonitorKeyThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, myself,parent):
        super(MonitorKeyThread, self).__init__()
        self.database = VideoDatabase()
        self.generalFunction = GeneralFunctions()
        self.myself = myself
        self.myparent = parent
        self.counter = 0

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
                self.counter = 0
                self.myself.disable_downloading()
                self.myself.labelActivationStatus.setText("Trial License Expired!")
                self.myself.textOwner.setText(email)
                self.myself.frame_license_info.setVisible(True)
                self.myself.buttonActivate.setVisible(True)
            else:
                self.counter = 0
                self.myself.enable_downloading()
                self.myself.labelActivationStatus.setText(f"Your license will expire in {str(licStatus)}")
                self.myself.textOwner.setText(email)
                self.myself.frame_license_info.setVisible(False)
                self.myself.buttonActivate.setVisible(False)

        except FullyActivatedException:
            pass
        except InvalidLicenseException:
            if self.myself.activation_in_progress is False:
                self.counter = 0
                self.myself.labelActivationStatus.setText("Activation Required!")
            else:
                self.counter += 1
                self.myself.labelActivationStatus.setText(f"{self.myparent.message} [ {self.generalFunction.format_seconds(self.counter)} ]")

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

