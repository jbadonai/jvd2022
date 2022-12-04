class ErrorFlag():
    def __init__(self):
        super(ErrorFlag, self).__init__()
        self.error_detected = False
        self.error_details = None
        self.error_Location = None


class EmergencyError(Exception):
    pass


class InternetError(Exception):
    pass


class UnsupportedURLError(Exception):
    pass


class PrivateVideoError(Exception):
    pass


class StoppedByUserException(Exception):
    pass


class RestartException(Exception):
    pass


class NotActivatedException(Exception):
    pass


class DisposableEmailException(Exception):
    pass


class SystemIDMistmatchException(Exception):
    pass

class ServerNotReachableException(Exception):
    pass

class DialogCanceledException(Exception):
    pass

class EmailSendingException(Exception):
    pass

class NewClientCreationException(Exception):
    pass

class SoftLandingException(Exception):
    pass

class UserCreationException(Exception):
    pass

class FullyActivatedException(Exception):
    pass

class InvalidLicenseException(Exception):
    pass

