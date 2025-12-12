import random
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Member

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Create tables
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
# Serve HTML Page
# --------------------------
@app.get("/", response_class=HTMLResponse)
def serve(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# --------------------------
# Random non-repeating friend pick
# --------------------------
@app.get("/friend/{name}")
def get_friend(name: str, db: Session = Depends(get_db)):
    # Verify user in the team
    user = db.query(Member).filter(Member.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="This name is not on the team list!")

    # If user already got a friend → return it
    if user.friend:
        return {"friend": user.friend}

    # Get list of available people (not assigned yet)
    available = db.query(Member).filter(
        Member.is_assigned == False,
        Member.name != name  # Can't pick themselves
    ).all()

    if not available:
        raise HTTPException(status_code=400, detail="No more available friends to assign!")

    # Select random friend
    chosen = random.choice(available)

    # Save assignment
    user.friend = chosen.name
    chosen.is_assigned = True

    db.commit()

    return {"friend": user.friend}
