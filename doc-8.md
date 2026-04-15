Lesson 8 — Async FastAPI + Performance
Goal

By the end, you will understand:

def vs async def
what async actually does
when to use it
when not to use it
how to explain it in an interview
1. Mental model

In C#, you already know:

public async Task<IActionResult> Get()

In Python/FastAPI, the equivalent is:

@router.get("/users")
async def get_users():
    ...

So at first sight:

async def in Python ≈ async Task in C#

That part is true.

But the important part is what kind of work is being awaited.

2. def vs async def
Synchronous route
@router.get("/health")
def health_check():
    return {"status": "ok"}
Asynchronous route
@router.get("/health")
async def health_check():
    return {"status": "ok"}

Both work.

So the real question is not:

“Can I use async?”

The real question is:

“Am I doing I/O that benefits from async?”

3. What async is really for

Async is mainly useful for waiting on I/O without blocking the worker.

Typical I/O:

database call
HTTP call to another API
file access
message queue/network calls

While the code is waiting, the server can handle other requests.

4. What async is not for

Async is not for CPU-heavy work.

Examples:

large calculations
ML inference on CPU
image processing
huge loops
encryption/compression-heavy tasks

For CPU-heavy work, async does not magically make it fast.

5. Good intuition
Async helps when the app says:

“I’m waiting for something external”

Async does not help when the app says:

“I’m busy computing”

That distinction is critical.

6. Example with external HTTP call
import httpx
from fastapi import APIRouter

router = APIRouter()

@router.get("/external-data")
async def get_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://example.com")
        return response.json()

This is a good async use case because:

network call
waiting time
server can do other work during the wait
7. Example of bad async thinking
@router.get("/sum")
async def calculate():
    total = 0
    for i in range(100000000):
        total += i
    return {"total": total}

This is still CPU work.

Even if the route is async def, it is not helping much.

8. Important FastAPI rule

If your code uses synchronous libraries, keep the route synchronous.

Example:

normal SQLAlchemy session
sync repository methods
sync file operations

Then:

@router.get("/users")
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_users()

is fine.

9. Your current project: should it be async?

Right now, your stack is roughly:

FastAPI
SQLAlchemy sync session
standard repository/service pattern

So for now:

Best answer:

Use sync endpoints for this version.

Why:

your DB access is sync
your service layer is sync
simpler architecture
easier learning path

So this is fine:

@router.get("/users")
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_users()

You do not need to force async everywhere.

This is actually a senior point.

10. Common beginner mistake

A lot of people do this:

@router.get("/users")
async def get_users(service: UserService = Depends(get_user_service)):
    return service.get_users()

But if service.get_users() is synchronous and uses sync SQLAlchemy, then this is inconsistent.

It may still run, but it is not a clean async architecture.

11. Clean async architecture requires async all the way

If you want true async DB handling, usually you move to:

async SQLAlchemy engine/session
async repository methods
await DB operations
async HTTP clients
async route handlers

So the chain becomes:

Route async
→ Service async
→ Repository async
→ Async DB session

Not half-sync, half-async.

12. C# comparison

This is similar to C#:

If your whole chain is async:

controller async
service async
repository async
EF Core async methods

then great.

But if your repository is synchronous and you fake async at the controller, that is not ideal.

Same idea here.

13. Example of a proper async signature style
Sync version
class UserService:
    def get_users(self, db: Session):
        return self.repo.get_all(db)
Async version conceptually
class UserService:
    async def get_users(self, db):
        return await self.repo.get_all(db)

And then route:

@router.get("/users")
async def get_users(service: UserService = Depends(get_user_service)):
    return await service.get_users()

But only if repository and DB are async too.

14. Performance truth

FastAPI being “fast” is not because:

Python is magically faster than C#

It is because:

ASGI
efficient async handling
low overhead
good tooling around async web APIs

But raw CPU-heavy business logic in Python is often not faster than .NET.

That is important to understand.

15. When to use async in your future case

For your interview / backend discussions, a very good answer is:

Use async when:
calling external APIs
database driver is async
high-concurrency I/O workloads
microservice communication
waiting on network resources
Keep sync when:
using sync SQLAlchemy
app is simple
CPU-heavy work dominates
you want architectural simplicity first
16. Real interview answer

A strong answer would be:

“In FastAPI, I use async def when the request path is I/O-bound and the dependencies are async end-to-end, such as async database or HTTP clients. If the stack is synchronous, I keep the endpoint synchronous rather than mixing paradigms.”

That is a very good answer.

17. One subtle point: async is concurrency, not magic parallel CPU

This matters a lot.

Async means:

handle many waiting tasks efficiently

It does not mean:

Python suddenly runs CPU work in parallel

For CPU parallelism, you would think more about:

multiprocessing
distributed workers
task queues like Celery
background jobs
18. Practical recommendation for your project

For your current learning project:

Stay sync for now

Use:

def
sync SQLAlchemy
simple service/repository

Why:

less complexity
clearer architecture
more stable understanding

Then later, if needed, we can build:

async version
compare both
discuss tradeoffs

That is the best progression for you.

19. What you should remember
async def is for non-blocking I/O
not for CPU-heavy work
sync stack → keep sync endpoints
async architecture should be consistent end-to-end
async improves concurrency, not raw CPU computation

20. Tiny examples to memorize
Good async case
@router.get("/price")
async def get_price():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/price")
        return response.json()
Good sync case
@router.get("/users")
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_users()

because repository/DB are sync.

Interview-level summary

You can now say:

“FastAPI supports both sync and async handlers. I use async for I/O-bound operations when the full dependency chain is async, and I keep endpoints synchronous when using synchronous libraries like standard SQLAlchemy sessions.”

That is a strong, credible answer.