from . import CustomBaseException

from fastapi import status

class UserAlreadyExistsException(CustomBaseException):
    def __init__(self):
        super().__init__(
            status.HTTP_409_CONFLICT,
            "UserAlreadyExists",
            "A user with this email already exists."
        )


class AuthTokenProvidedException(CustomBaseException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "TokenAlreadyProvided",
            "Authorization token is already present in the request."
        )

class InvalidAuthTokenProvidedException(CustomBaseException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "TokenAlreadyProvided",
            "Authorization token is already present in the request."
        )


class InvalidCredentialsException(CustomBaseException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "InvalidCredentials",
            "The email or password provided is incorrect."
        )