# Standard Library imports

# Core Flask imports

# Third-party imports

# App imports


class Error(Exception):
    def __init__(self, value=""):
        if not hasattr(self, "value"):
            self.value = value

    def __str__(self):
        return repr(self.value)


class EmailAddressAlreadyExistsError(Error):
    message = "There is already an account associated with this email address."
    internal_error_code = 40902


class InternalDbError(Error):
    message = "Sorry, we had a problem with that request. Please try again later or contact customer support."  # noqa: E501
    internal_error_code = 50001


class CouldNotVerifyLogin(Error):
    message = "You have entered an invalid email or password. Please try again."
    internal_error_code = 40101


class PermissionsDeniedError(Error):
    message = "Sorry, you don't have the necessary permissions. Please contact your admin or customer support."  # noqa: E501
    internal_error_code = 40301
