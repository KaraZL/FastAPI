from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.models.user import UserCreate, UserResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

repo = UserRepository()

@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)): #public UserController(AppDbContext db) : db: Session = Depends(get_db) is Dependency Injection
    return repo.create(db, user.name, user.age)

@router.get("/users", response_model=UserResponse)
def get_all(db: Session = Depends(get_db)):
    return repo.get_all(db)


'''
from fastapi import APIRouter
from app.models.user import UserCreate, UserResponse
from app.models.product import ProductCreate
from app.models.order import OrderCreate, OrderResponse


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/hello/{name}")
def say_hello(name: str):
    return {"status": f"hello {name}"}


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return user

@router.post("/products")
def create_product(product: ProductCreate):
    return {
        "name": f"Product {product.name}",
        "price": product.price,
        "in_stock": product.in_stock 
    }

@router.post("/orders",response_model=OrderResponse)
def create_order(order: OrderCreate):
    return order
'''
