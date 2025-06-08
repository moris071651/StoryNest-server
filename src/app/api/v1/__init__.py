from fastapi import APIRouter
from api.v1 import auth, story, publication, user

router = APIRouter(prefix='/v1')

router.include_router(auth.router)
router.include_router(story.router)
router.include_router(publication.router)
router.include_router(user.router)
