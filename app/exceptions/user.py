from . import CustomBaseException

from fastapi import status

class EmailAlreadyTakenException(CustomBaseException):
    def __init__(self):
        super().__init__(
            status.HTTP_409_CONFLICT,
            "Email Already Taken",
            "The provided email is already taken by another user."
        )