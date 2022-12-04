from PyQt5 import QtCore
import time
from security import JBHash, LicenseGenerator, JBEncrypter
from videoDatabase import VideoDatabase
from environment import Config
from generalFunctions import GeneralFunctions


class LicenseChecker():
    def __init__(self, myself):
        self.threadController = {}
        self.myself = myself

    def start(self):
        def license_connector(data):
            try:
                # print("[DATA] ", data)
                pass
            except Exception as e:
                print(f"An Error Occurred in License checker > license connector : {e}")
        try:
            self.threadController['license checker'] = _LicenseCheckerThread(self.myself)
            self.threadController['license checker'].start()
            self.threadController['license checker'].any_signal.connect(license_connector)
        except Exception as e:
            print(f"An Error Occurred in 'License Checker' > start: {e}")
        pass

    def stop(self):
        try:
            self.threadController['license checker'].stop()
            pass
        except Exception as e:
            print(f"An Error Occurred in 'License checker'>'stop' : {e}")
        pass


class _LicenseCheckerThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(dict)

    def __init__(self, myself):
        super(_LicenseCheckerThread, self).__init__()
        try:
            self.is_running = False
            self.dataToEmit = {}
            self.myself = myself
            self.timerConstant = 0
            self.general_function = GeneralFunctions()

        except Exception as e:
            print(f"An Error Occurred in license checker thread > __init__(): \n >>{e}")

    def stop(self):
        try:
            self.requestInterruption()
            self.is_running = False
        except Exception as e:
            print(f"An Error Occurred in geEntryThread > stop: {e}")
            pass

    def check_activation_status(self):
        trialActivated = self.myself.generalFunction.is_trial_activated()
        trialExpired = self.myself.generalFunction.is_trial_expired()
        fullyActivated = self.myself.generalFunction.is_fully_activated()

        if trialActivated is False and trialExpired is False and fullyActivated is False:
            self.myself.labelActivationStatus.setText("Activation Required! Click on Activate Button to Activate your Free Trial License!")
            self.myself.labelActivationStatus.setToolTip("Click on 'Activate' button in the toolbar to Activate your Free Trial License")

    def get_license_remaining_days(self):
        try:
            # get license srored in the database
            lic = self.myself.database.get_settings('trial_key')

            # decrypt it to get the actual content
            decryptedLicense = JBEncrypter().decrypt(lic, Config().config("ENCRYPT_PASSWORD"))
            # print(f"dec license: {decryptedLicense}")

            # split it to get actual license. as it contains both email and license separated by '
            userLicense = decryptedLicense.split("'")[1]

            # check if the extracted license has expired. this returns 2 data, boolen and time remaning
            data = LicenseGenerator().is_license_expired(userLicense)
            license_expired = data[0]

            # extract time remaining from the license
            if license_expired is False:
                daysRemaining = data[1]
            else:
                daysRemaining = "License Expired!"
                VideoDatabase().update_setting('trial_expired',True)

            return daysRemaining

            pass
        except Exception as e:
            print(f"An Error Occurred in get license remaining days: {e}")

    def activation_monitor_bak(self):
        try:
            # Activation monitors
            # self.check_activation_status()
            self.timerConstant = 0  # reset every 1 second

            owner = self.myself.database.get_settings('owner')  # get owner stored in the database
            self.myself.textOwner.setText(owner)  # display owner in the tool bar

            # check if there is an active license
            if self.myself.authentications.is_licence_active() is True:
                # check if trial or
                # self.textAddNewURL.setEnabled(True)
                self.myself.textAddNewURL.setPlaceholderText("Paste Video Url here!")
                self.myself.buttonActivate.setVisible(False)  # hide activate button
                self.myself.frame_license_info.setVisible(False)  # hide license window

                days_remaining = self.get_license_remaining_days()

                # display the time reamining.
                self.myself.labelActivationStatus.setText(f"Your license will expire in {str(days_remaining)}")
                pass
            else:
                # if there is no active license recorded in the database
                trialExipired = self.general_function.is_trial_expired()
                if trialExipired is False:
                    self.myself.textAddNewURL.setPlaceholderText(
                        "Paste Url here! Please Activate trail License or Full License First.")
                    if self.general_function.is_message_sent_successful() is False:
                        self.myself.buttonActivate.setVisible(True)  # show the activate button
                        self.myself.labelActivationStatus.setText(f"Activation Required! Please Click the 'Activate' button for your Free Trial License")
                    else:
                        # temporary owner check
                        temp_owner = self.myself.database.get_settings('temp_owner')
                        owner = self.myself.database.get_settings('owner')
                        if owner == "jbadonaiventures" and temp_owner != "":
                            self.myself.labelEmailAddress.setText(temp_owner)
                            self.myself.buttonActivate.setVisible(False)
                            self.myself.labelActivationStatus.setText("Activation Required! Please check your mail.")
                            self.myself.labelActivationStatus.setToolTip(
                                f"Check Your mail '{temp_owner}' for License code. \nOpen Settings "
                                f"panel, "
                                f"Paste your license code and press 'Activate License' button.")
                            self.myself.frame_settings.setVisible(True)
                else:
                    # TRIAL PERIOD EXPIRED!

                    self.myself.labelActivationStatus.setText(f"Trial Period has Expired!")
                    self.myself.labelActivationStatus.setToolTip("Check your mail on instruction on how to renew your license!")
                    self.myself.labelEmailAddress.setText(owner)

                    te = self.general_function.is_trial_expired()
                    if te is False:
                        self.database.update_setting('trial_expired', True)

                self.myself.frame_license_info.setVisible(True)  # show the license window

            pass
        except Exception as e:
            print(f"An Error Occurred in activation monitor in timer: {e}")

    def activation_monitor(self):
        try:
            # Activation monitors
            self.timerConstant = 0  # reset every 1 second

            owner = self.myself.database.get_settings('owner')  # get owner stored in the database
            self.myself.textOwner.setText(owner)  # display owner in the tool bar

            trial_license_key = VideoDatabase().get_settings('trial_key')
            full_license_key = VideoDatabase().get_settings('license_key')
            trial_expired = self.general_function.is_trial_expired()

            print(f"License Expired: {trial_expired}<>{type(trial_expired)}")

            # if trial has not expired we will be looking at trial key else key expeted is full
            if trial_expired is False:
                license = trial_license_key
            else:
                license = full_license_key

            if license == "":
                #  NO LICENSE YET
                self.myself.activated = False   # keep track of app activation status
                self.myself.buttonActivate.setVisible(True) # show activate button
                self.myself.frame_license_info.setVisible(True)  # show license window
                temp_owner = self.myself.database.get_settings('owner')
                self.myself.labelEmailAddress.setText(temp_owner)
                if trial_expired is False:
                    self.myself.labelActivationStatus.setText("Activation Required! \nPlease click the 'Activate' button below to get your Free Trial License!")
                else:
                    self.myself.labelActivationStatus.setText("Activation Required! Please get you Paid License!")
                pass
            else:
                self.myself.activated = True    # keep track of app activation status
                self.myself.buttonActivate.setVisible(False)    # hide activate button
                self.myself.frame_license_info.setVisible(False)  # hide license window

                data = JBEncrypter().decrypt(license, Config().config('ENCRYPT_PASSWORD'))
                email, trialLicense, systemID, fullLicense =data.split("'")
                ans = LicenseGenerator().is_license_expired(trialLicense)
                license_expired = bool(ans[0])
                days_remaining = ans[1]

                if license_expired is False:
                    self.myself.labelActivationStatus.setText(f"Your license will expire in {str(days_remaining)}")
                else:
                    self.myself.labelActivationStatus.setText(f"Your Trial License has expired. Please get a Paid License! Thank You.")
                    te = self.general_function.is_trial_expired()
                    if te is False:
                        #   1. update data on the server

                        # 2. change the settings locally
                        VideoDatabase().update_setting('trial_expired', True)


        except Exception as e:
            print(f"An Error Occurred in activation monitor in timer: {e}")

    def run(self):
        try:
            self.is_running = True

            while True:
                if self.isInterruptionRequested() is True:
                    break

                if self.is_running is False:
                    break

                self.activation_monitor()

                # 1. CONTACT SERVER

                # 2. ON FIRST RUN GET A UNIQUE ID FROM THE SERVER - SEND UNIQUE DATA TO SERVER TO REGISTER ON SERVER

                # 3. ON FIRST RUN RECEIVE A TRIAL KEY FROM THE SERVER AND APPLY

                # 4. STORE BASIC DATA ON THE SERVER

                licenseKey = VideoDatabase().get_settings("license_key")
                trialKey = VideoDatabase().get_settings("trial_key")
                fullyActivated = VideoDatabase().get_settings("fully_activated")
                trialActivated = VideoDatabase().get_settings("trial_activated")
                trialLicense = VideoDatabase().get_settings("trial_key")
                full_license = VideoDatabase().get_settings("license_key")


                time.sleep(1)

        except Exception as e:
            print(f"An Error occurred in getInternetDownloadSpeed > 'run' : {e}")

