from . import CustomBaseException

from fastapi import status


class AuthTokenProvidedException(CustomBaseException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "TokenAlreadyProvided",
            "Authorization token is already present in the request."
        )