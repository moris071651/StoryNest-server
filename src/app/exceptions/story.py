from . import CustomBaseException

from fastapi import status

class NoSuchStoryException(CustomBaseException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            "NoSuchStory",
            "A story with this id does not exists."
        )