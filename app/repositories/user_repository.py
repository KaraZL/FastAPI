from sqlalchemy.orm import Session
from app.db.models.user import User

class UserRepository:
    def create(self, db: Session, name: str, age: int):
        user = User(name=name, age=age)
        db.add(User)
        db.commit()
        db.refresh(user)
        return user
    
    def get_all(self, db: Session):
        return db.query(User).all()