from app.database import SessionLocal
from app.models import Venue
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        venues = [
            Venue(
                name="Convention Hall A",
                city="Bekasi",
                address="Jl. Ahmad Yani No.1",
                description="Hall besar kapasitas 1000 orang"
            ),
            Venue(
                name="Ballroom B",
                city="Jakarta",
                address="Jl. Sudirman No.99",
                description="Ballroom mewah"
            )
        ]

        db.add_all(venues)
        db.commit()
        print("Venue seed completed")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
