class ApplicationError(Exception):
    pass


class RegexError(ApplicationError):
    pass


class AuthenticationError(ApplicationError):
    pass


class BeautifulSoupError(ApplicationError):
    pass
