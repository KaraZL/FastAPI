from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.mappers.user_mapper import to_user_response
from app.db.models.user import User
from app.models.user import UserCreate

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    def create_user(self, db: Session, user: UserCreate):
        entity = User(name=user.name, age=user.age)
        created = self.repo.save(db, entity)
        return to_user_response(created)
    
    def get_users(self, db: Session):
        users = self.repo.get_all(db)
        return [to_user_response(u) for u in users]
    
#DB → Entity → Mapper → DTO → API