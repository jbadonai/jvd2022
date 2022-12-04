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