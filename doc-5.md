🚀 Lesson 5 — Alembic (Database Migrations)
🎯 Goal

By the end, you will:

Understand migrations (like EF Core)
Initialize Alembic
Generate migrations from your models
Apply schema changes safely
Talk about it confidently in interviews

🧠 1. Mental Model (VERY IMPORTANT)
Concept	Alembic	ASP.NET
Migration tool	Alembic	EF Core Migrations
Create migration	revision --autogenerate	Add-Migration
Apply migration	upgrade	Update-Database
Schema evolution	versioned	versioned

👉 Right now you use:

Base.metadata.create_all()

❌ This is NOT production safe

Why?
no versioning
no rollback
no history
no diff tracking

⚙️ 2. Install Alembic
pip install alembic
⚙️ 3. Initialize Alembic

Run at project root:

alembic init alembic
This creates:
alembic/
 ├── versions/
 ├── env.py
 ├── script.py.mako
alembic.ini
⚙️ 4. Configure Database Connection
In alembic.ini

Find:

sqlalchemy.url = driver://user:pass@localhost/dbname

Replace with:

sqlalchemy.url = sqlite:///./test.db
⚙️ 5. Link Alembic to Your Models (CRITICAL)
Edit alembic/env.py

Find:

target_metadata = None

Replace with:

from app.db.base import Base
import app.db.models.user  # IMPORTANT

target_metadata = Base.metadata

👉 This tells Alembic:

“These are my models — compare them to DB”

🔥 6. Create First Migration

Run:

alembic revision --autogenerate -m "create users table"

👉 This generates a file in:

alembic/versions/

Example content:

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('users')
▶️ 7. Apply Migration
alembic upgrade head

👉 Your DB is now created via migrations ✅

⚠️ IMPORTANT — REMOVE THIS

In main.py, DELETE:

Base.metadata.create_all(bind=engine)

👉 Because now:

✔ Alembic manages schema
✔ Not your app

🧠 8. Modify Schema (Real Scenario)

Add a field:

# db/models/user.py
email = Column(String)
Then:
alembic revision --autogenerate -m "add email to users"
alembic upgrade head

👉 DB evolves safely

🔁 9. Rollback (VERY IMPORTANT)
alembic downgrade -1

👉 Rolls back last migration

💡 ASP.NET Equivalent
Add-Migration AddEmail
Update-Database

Rollback:

Update-Database PreviousMigration
🔥 10. Senior-Level Workflow

Real workflow:

Change model
Generate migration
Review migration file (!!)
Apply migration
Commit migration file
⚠️ NEVER TRUST AUTOGENERATE BLINDLY

Always check:

column types
constraints
indexes
🧠 Interview Gold

Say this:

“I use Alembic for schema versioning and evolution, similar to EF Core migrations, ensuring controlled database changes and rollback capability.”