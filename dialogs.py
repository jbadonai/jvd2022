from ui import RegisterDialog_, msgBox_
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from generalFunctions import GeneralFunctions
from runtimeStyleSheet import ColorScheme, MessageBoxStyleSheet, RegisterDialogStyleSheet


class RegisterDialog(QDialog, RegisterDialog_.Ui_Dialog):
    def __init__(self):
        super(RegisterDialog, self).__init__()
        self.setupUi(self)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Register!")
        self.buttonCancel.clicked.connect(self.reject)
        self.buttonRegister.clicked.connect(self.accept)
        self.buttonShowHidePassword.clicked.connect(self.show_hide_password)
        self.data = {}
        self.textUsername.setFocus()
        self.username = None
        self.email = None
        self.password = None
        self.labelWarningMessage.setVisible(False)
        self.generalFunction = GeneralFunctions()


        # stylesheet
        self.my_color_scheme = ColorScheme()
        self.my_stylesheet = RegisterDialogStyleSheet(self, self.my_color_scheme.dark_theme())
        self.my_stylesheet.apply_stylesheet()  # apply stylesheet to self



    def show_hide_password(self):
        if self.buttonShowHidePassword.isChecked():
            self.buttonShowHidePassword.setIcon(QIcon(":/white icons/White icon/eye-off.svg"))
            self.textPassword.setEchoMode(self.textPassword.EchoMode.Normal)
        else:
            self.buttonShowHidePassword.setIcon(QIcon(":/white icons/White icon/eye.svg"))
            self.textPassword.setEchoMode(self.textPassword.EchoMode.Password)
        pass

    def display_warning(self, message):

        self.labelWarningMessage.setVisible(False)
        self.labelWarningMessage.setText(message)
        self.labelWarningMessage.setVisible(True)
        self.adjustSize()


    def reject(self):
        super(RegisterDialog, self).reject()
        # return self.data

    def accept(self):
        if self.textUsername.text() != "" and self.textPassword.text() != "" and self.textEmail.text() != "":
            self.username = self.data['username'] = self.textUsername.text()
            self.email = self.data['email'] = self.textEmail.text()
            self.password = self.data['password'] = self.textPassword.text()

            valid_email = self.generalFunction.check(self.email)

            if valid_email is True:
                super(RegisterDialog, self).accept()
                return self.data
            else:
                self.display_warning("Invalid Email Address. Please provide a valid Email Address")
                self.textEmail.setFocus()
                self.textEmail.selectAll()

        else:
            self.display_warning("Please provide all data. All Fields are mandatory!")



class MessageBox():
    def __init__(self):
        self.Yes = False
        self.No = False

    def show_question(self, title, message):
        message_box = _MBox()
        message_box.question(title, message)
        if message_box.exec():
            self.Yes = message_box.Yes
            self.No = message_box.No

    def show_information(self, title, message):
        message_box = _MBox()
        message_box.information(title, message)
        if message_box.exec():
            return True



class _MBox(QDialog, msgBox_.Ui_Dialog):
    def __init__(self):
        super(_MBox, self).__init__()
        self.setupUi(self)
        self.Yes = False
        self.No = False

        self.buttonNo.clicked.connect(self.accept)
        self.buttonYes.clicked.connect(self.accept)
        self.buttonOk.clicked.connect(self.accept)

        # stylesheet
        self.my_color_scheme = ColorScheme()
        self.my_stylesheet = MessageBoxStyleSheet(self, self.my_color_scheme.dark_theme())
        self.my_stylesheet.apply_stylesheet()  # apply stylesheet to self

    def question(self,title, message):
        self.buttonOk.setVisible(False)
        self.buttonYes.setVisible(True)
        self.buttonNo.setVisible(True)
        self.setWindowTitle(title)
        self.textInfo.setText(message)
        pass

    def information(self,title, message):
        self.buttonOk.setVisible(True)
        self.buttonYes.setVisible(False)
        self.buttonNo.setVisible(False)
        self.setWindowTitle(title)
        self.textInfo.setText(message)

    def reject(self):
        self.Yes = False
        self.No = False
        pass

    def accept(self):
        sender = self.sender()

        if sender.objectName() == self.buttonYes.objectName():
            self.Yes = True
            self.No = False

        if sender.objectName() == self.buttonNo.objectName():
            self.Yes = False
            self.No = True
            
        super(_MBox, self).accept()
        
        pass
