🚀 Lesson 1 — FastAPI + Project Structure + First Endpoint
🎯 Goal of this lesson

By the end, you will:

Understand how FastAPI works (mentally map it to ASP.NET)
Run your first API
Create a clean, production-style project structure
Expose your first endpoint

🧠 1. Mental Model (Mapped to ASP.NET)
Concept	FastAPI	ASP.NET
App entry point	main.py	Program.cs
Controller	function with decorator	Controller class
Routing	@app.get()	[HttpGet]
DI	Depends()	Constructor injection
Models	Pydantic	DTO / Model

⚙️ 2. Install Minimal Stack
pip install fastapi uvicorn

👉 Equivalent to:

FastAPI = ASP.NET Core
Uvicorn = Kestrel

▶️ 5. Run the API
uvicorn app.main:app --reload

👉 http://127.0.0.1:8000/health

🔥 6. What Just Happened (Important)
This:
@router.get("/health")

👉 is equivalent to:

[HttpGet("health")]
public IActionResult Health()
This:
def health_check():

👉 replaces:

public IActionResult Health()

⚡ 7. Why This Structure Matters (Interview Gold)

If you explain this, you sound senior:

“I separated routing from the application entry point to allow scaling into a modular architecture with independent routers, similar to splitting controllers by domain in ASP.NET.”

🧠 Key Takeaways (Memorize These)
FastAPI = function-based controllers
Decorators = routing
Return dict = JSON automatically
Router system = modular architecture
Uvicorn = runtime server