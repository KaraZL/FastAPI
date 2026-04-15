🚀 Lesson 9 — Dockerizing Your FastAPI Service
🎯 Goal

By the end, you will:

Containerize your FastAPI app
Understand how Python apps are packaged
Run your API in Docker
Be able to explain it in interviews
🧠 1. Mental Model (ASP.NET vs Python)
Concept	FastAPI	ASP.NET
Build	no compile step	dotnet build
Run	uvicorn	dotnet run
Container	Python image	.NET runtime image

👉 Key difference:

Python is interpreted
so Docker is simpler (no build/publish step)
📦 2. Project Structure (what Docker sees)
FastAPI/
├── app/
├── alembic/
├── requirements.txt
├── Dockerfile
⚙️ 3. Create requirements.txt

If not done yet:

pip freeze > requirements.txt
🐳 4. Create Dockerfile
Dockerfile
# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
🔥 Explanation (important)
This line:
WORKDIR /app

👉 Equivalent to:

cd /app
This:
COPY . .

👉 Copies your entire project into container

This:
CMD ["uvicorn", "app.main:app", ...]

👉 Runs your API

▶️ 5. Build the image

From project root:

docker build -t fastapi-app .
▶️ 6. Run the container
docker run -p 8000:8000 fastapi-app

👉 Open:
http://localhost:8000/docs

⚠️ Important (DB + Alembic)

Right now:

SQLite file is inside container
it will be lost when container stops
For now (learning): OK

Later:

use volumes
or external DB (Postgres, Azure SQL, etc.)
🧠 7. Add .dockerignore

Create:

.dockerignore
.venv/
__pycache__/
*.pyc
*.db
.git

👉 Equivalent:

ignoring bin/obj in .NET
🔥 8. Production Improvement (very important)

Instead of:

CMD ["uvicorn", ...]

Use:

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

👉 Adds concurrency (multi-process)

🧠 9. Even better (advanced)

Use Gunicorn + Uvicorn workers

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]

👉 Equivalent to:

Kestrel + reverse proxy
⚡ 10. Interview Gold

You can say:

“I containerize FastAPI services using Docker, installing dependencies via requirements.txt and running the app with Uvicorn. For production, I use multiple workers or Gunicorn for concurrency.”