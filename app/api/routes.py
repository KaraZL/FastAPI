from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.user_service import UserService
from app.models.user import UserCreate, UserResponse
from app.dependencies import get_user_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#services = UserService()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/users", request_model=)
def create_user(user: UserCreate, db: Session = Depends(get_user_service)): #public UserController(AppDbContext db) : db: Session = Depends(get_db) is Dependency Injection -> true DI -> Depends(et_user_service)
    return services.create_user(db, user.name, user.age)

@router.get("/users", response_model=list[UserResponse])
def get_all(db: Session = Depends(get_db)):
    return services.get_users(db)