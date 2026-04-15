from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


def get_user_repository():
    return UserRepository()


def get_user_service(
        db: Session = Depends(get_db),
        repo: UserRepository = Depends(get_user_repository)
):
    return UserService(repo)
