🚀 Lesson 4 — SQLAlchemy (ORM, Sessions, Repository Pattern)
🎯 Goal

By the end, you will:

Understand how **SQLAlchemy works
Create database models
Use sessions (like DbContext)
Implement a clean repository pattern
Think in a .NET → Python mapping

🧠 1. Mental Model (VERY IMPORTANT)
Concept	SQLAlchemy	ASP.NET
ORM	SQLAlchemy	Entity Framework
DbContext	Session	DbContext
Entity	Model class	Entity class
Query	session.query()	LINQ

👉 If you understand EF Core, you're already 70% there.

⚙️ 2. Install Dependencies
pip install sqlalchemy

👉 We’ll use SQLite for now (no install needed)

📁 3. Update Project Structure

We start organizing like a real backend:

app/
 ├── main.py
 ├── api/
 ├── models/        ← Pydantic (DTOs)
 ├── db/
 │    ├── base.py
 │    ├── session.py
 │    └── models/   ← SQLAlchemy entities
 ├── repositories/

 🧱 4. Database Setup
db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

👉 Equivalent:

services.AddDbContext<AppDbContext>()

🧱 5. Base Class (like EF Core ModelBuilder root)
db/base.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

🧱 6. Create Your First Entity
db/models/user.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

👉 Equivalent:

public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public int Age { get; set; }
}

⚙️ 7. Create the Database Tables

Temporary (we’ll replace with Alembic later):

from app.db.session import engine
from app.db.base import Base
from app.db.models import user

Base.metadata.create_all(bind=engine)

👉 Run it once → creates test.db

🔥 8. Session = DbContext
Add dependency (important)
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

👉 Equivalent:

scoped DbContext per request


🧱 9. Repository Pattern (Senior Move)
repositories/user_repository.py
from sqlalchemy.orm import Session
from app.db.models.user import User

class UserRepository:

    def create(self, db: Session, name: str, age: int):
        user = User(name=name, age=age)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_all(self, db: Session):
        return db.query(User).all()

👉 Equivalent:

EF repository / service layer

🔗 10. Use It in FastAPI
Update route:
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

repo = UserRepository()

@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return repo.create(db, user.name, user.age)
💥 What just happened

This line:

db: Session = Depends(get_db)

👉 is Dependency Injection

👉 Equivalent:

public UserController(AppDbContext db)

🧠 11. Flow (Important)

Request →
FastAPI →
Dependency Injection →
Repository →
Database

👉 Clean architecture ready

⚠️ Important Warning (Senior Detail)

Right now:

You are returning SQLAlchemy models directly ❌

👉 In Lesson 3 terms:

you should use response_model

We’ll fix that soon.

🔥 Key Takeaways
Session = DbContext
Models ≠ Pydantic models
Repository = clean separation
FastAPI DI is powerful
Architecture is now scalable
🧠 Interview Gold

Say this:

“I use SQLAlchemy sessions as a unit-of-work similar to DbContext, injected per request, and encapsulate data access inside repositories to keep the API layer clean.”


##################################################

🧱 Where to put Step 7 (create tables)
❌ Don’t leave it floating somewhere

You should NOT:

paste it randomly
run it manually in REPL
leave it unstructured

✅ Proper place (for now): main.py

Update your main.py like this:

from fastapi import FastAPI
from app.api.routes import router

from app.db.session import engine
from app.db.base import Base
import app.db.models.user  # IMPORTANT (registers model)

app = FastAPI()

# Create tables on startup (TEMPORARY)
Base.metadata.create_all(bind=engine)

app.include_router(router)
🧠 Why this works

This line:

Base.metadata.create_all(bind=engine)

👉 scans all imported models and creates tables

⚠️ And THIS is critical:

import app.db.models.user

👉 Without it:

SQLAlchemy doesn’t “see” your model
table won’t be created

🧱 Where to put Step 8 (get_db)

👉 You have 2 clean options

✅ Option A (simple, fine for now)

Put it directly in your route file:

# app/api/routes.py

from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
✅ Option B (better architecture — recommended)

Create a dedicated file:

app/db/dependencies.py
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Then use it:

from app.db.dependencies import get_db

👉 This is cleaner and scales better.

🔥 Senior Insight

Right now we are doing:

Base.metadata.create_all(...)

👉 This is ONLY for learning

In real projects:

you NEVER auto-create tables
you use migrations (next lesson 👉 Alembic)
🧠 ASP.NET Equivalent

This:

create_all()

👉 is like:

context.Database.EnsureCreated();

And later we’ll move to:

context.Database.Migrate();

👉 = Alembic

##############################################

