from http import HTTPStatus


class ApplicationError(Exception):
    def __init__(self):
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.message = 'APIError'


class NotFoundError(Exception):
    def __init__(self):
        self.code = HTTPStatus.NOT_FOUND
        self.message = 'Not Found'


class ValidationError(Exception):
    def __init__(self):
        self.code = HTTPStatus.BAD_GATEWAY
        self.message = 'The query parameter fullname must consist of at least two words'
