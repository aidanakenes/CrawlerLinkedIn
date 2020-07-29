class ApplicationError(Exception):
    def __init__(self):
        self.code = 'APIError',
        self.message = f'Failed to parse page for link'


class RegexError(ApplicationError):
    def __init__(self):
        self.code = 'APIError',
        self.message: str = 'Failed to parse regex'


class AuthenticationError(ApplicationError):
    def __init__(self):
        self.code = 'APIError',
        self.message: str = 'Failed to login'


class BeautifulSoupError(ApplicationError):
    def __init__(self):
        self.code = 'APIError',
        self.message: str = 'Failed to parse with BeautifulSoup'
