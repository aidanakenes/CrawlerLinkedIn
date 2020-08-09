from http import HTTPStatus


class CustomException(Exception):
    def __init__(self):
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.message = 'APIError'


class ApplicationError(CustomException):
    def __init__(self):
        super().__init__()
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.message = 'APIError'


class NotFound(CustomException):
    def __init__(self):
        super().__init__()
        self.code = HTTPStatus.NOT_FOUND
        self.message = 'Not Found'


class ValidationError(CustomException):
    def __init__(self):
        super().__init__()
        self.code = HTTPStatus.BAD_REQUEST
        self.message = 'The query parameter fullname must consist of at least two words'


class IDValidationError(CustomException):
    def __init__(self):
        super().__init__()
        self.code = HTTPStatus.BAD_REQUEST
        self.message = 'Public id parameter can contain only letters, numbers and dash'
