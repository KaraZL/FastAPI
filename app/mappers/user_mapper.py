from app.db.models.user import User
from app.models.user import UserResponse

def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        age=user.age
    )