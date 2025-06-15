from fastapi import APIRouter
from . import auth, story, publication, user, comment, tag

router = APIRouter(prefix='/v1')

router.include_router(auth.router)
router.include_router(story.router)
router.include_router(publication.router)
router.include_router(user.router)
router.include_router(comment.router)
router.include_router(tag.router)
