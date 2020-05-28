class AuthorizationError(Exception):
    """
Raise when there is an issue with the user's config file
"""
    def __init__(self):
        self.expression = "There is an issue with your config file"
        self.message = "There is an issue with your config file"
class ICD11CodeError(ValueError):
    """Raise when an ICD11 code is correctly formatted but leads to an error when used with the api"""
