🚀 Lesson 6 — Clean Architecture (Proper Layering)
🎯 Goal

By the end, you will:

Separate concerns properly
Avoid leaking ORM models
Introduce DTO ↔ Entity mapping
Structure your project like a real microservice
Speak confidently about architecture
🧠 1. The Problem in Your Current Code

Right now:

Route → Service → Repository → DB

✔ Good
BUT:

👉 You are returning SQLAlchemy entities directly

That means:

ORM leaks into API ❌
tight coupling ❌
hard to evolve ❌

✅ 2. Target Architecture (Clean)
API Layer        → FastAPI routes
Application      → Services (business logic)
Domain           → Entities (optional advanced)
Infrastructure   → Repositories (DB)
DTO Layer        → Pydantic models
🔥 Golden Rule

❌ Never return database entities to the outside world
✅ Always return DTOs (Pydantic models)

🧱 3. Separate DTO vs Entity

You already have:

DTO (Pydantic)
# app/models/user.py

class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    age: int

    model_config = ConfigDict(from_attributes=True)
Entity (SQLAlchemy)
# app/db/models/user.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
⚠️ Current problem

You are doing:

return repo.get_all(db)

👉 That returns User (ORM)

✅ 4. Introduce Mapping (VERY IMPORTANT)
Create mapper
app/mappers/user_mapper.py
from app.db.models.user import User
from app.models.user import UserResponse

def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        age=user.age
    )
🔁 5. Use it in Service Layer
from app.mappers.user_mapper import to_user_response

class UserService:

    def get_users(self, db: Session):
        users = self.repo.get_all(db)
        return [to_user_response(u) for u in users]
🔥 Now your flow is clean
DB → Entity → Mapper → DTO → API
🧠 ASP.NET Equivalent

This is exactly like:

Entity Framework entity
→ AutoMapper
→ DTO returned by controller
⚡ 6. Even Cleaner: Input Mapping

Instead of:

repo.create(db, name, age)

Do:

def create_user(self, db: Session, user: UserCreate):
    entity = User(name=user.name, age=user.age)
    created = self.repo.save(db, entity)
    return to_user_response(created)
🧱 7. Repository Should Only Handle Entities
def save(self, db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
⚠️ Important principle
Layer	Should know
API	DTO only
Service	DTO + Entity
Repository	Entity only
🧠 8. Why This Matters (Interview Gold)

You can say:

“I separate persistence models from API contracts using DTOs and mapping, ensuring that database concerns do not leak into the API layer.”

🔥 9. Optional: Remove from_attributes=True

If you map manually, you don’t even need it anymore.

👉 That’s actually cleaner and more explicit.

🧪 10. Your Exercise

Refactor your code so that:

/users
returns UserResponse
NEVER returns SQLAlchemy objects
/users POST
accepts UserCreate
returns UserResponse
🧠 Expected final flow
Route → Service → Repository → DB
            ↓
         Mapper
            ↓
         DTO
⚠️ Real-World Note

In small projects:

people skip mapping

In serious systems:

mapping is standard

