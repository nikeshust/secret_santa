from database import SessionLocal, engine
from models import Member
from database import Base

# CREATE TABLES first!
Base.metadata.create_all(bind=engine)

teamMembers = [

]

db = SessionLocal()

for name in teamMembers:
    db.add(Member(name=name, friend=None, is_assigned=False))

db.commit()
db.close()

print("Database seeded successfully!")
