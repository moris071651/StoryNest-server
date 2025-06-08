from uuid import UUID
from fastapi import APIRouter, Request
from exceptions.auth import UnauthenticatedUserException
from utils.security import get_auth_user

from services import comment as service
from schemas.comment import Comment, CommentCreate, CommentUpdate


router = APIRouter(prefix='/stories', tags=["Comments"])


@router.get('/{story_id}/comments/')
def get_comments(story_id: UUID) -> Comment:
    pass


@router.post('/{story_id}/comments/')
def create_comment(request: Request, story_id: UUID, comment: CommentCreate) -> Comment:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()

    return service.create_comment(
        author_id=user_id,
        story_id=story_id,
        content=comment.content
    )


@router.get('/{story_id}/comments/{comment_id}')
def get_comment(request: Request, story_id: UUID, comment_id: UUID) -> Comment:
    pass


@router.delete('/{story_id}/comments/{comment_id}')
def delete_comment(request: Request, story_id: UUID, comment_id: UUID):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()
    
    service.delete_comment(
        user_id=user_id,
        story_id=story_id,
        comment_id= comment_id
    )


@router.patch('/{story_id}/comments/{comment_id}')
def update_comment(request: Request, story_id: UUID, comment_id: UUID, comment: CommentUpdate):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()
    
    return service.update_comment(
        user_id=user_id,
        story_id=story_id,
        comment_id= comment_id,
        content=comment.content
    )
