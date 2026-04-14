from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
Calls get_db()
Runs until yield → gives db to your route
After request finishes → resumes function
Executes finally → closes connection

💡 ASP.NET Equivalent

Closest mental model:

using (var db = new AppDbContext())
{
    // use db
}
'''