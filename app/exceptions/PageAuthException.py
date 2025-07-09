from app.exceptions.SystemException import SystemException


class PageAuthException(SystemException):
    def __init__(self, message="System Exception", code=4000):
        super().__init__(message, code)
        self.message = message
        self.code = code