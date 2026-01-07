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
                description="Ballroom mewah untuk acara formal"
            ),
            Venue(
                name="Expo Center C",
                city="Bandung",
                address="Jl. Asia Afrika No.15",
                description="Gedung expo untuk pameran dan konser"
            ),
            Venue(
                name="Auditorium D",
                city="Depok",
                address="Jl. Margonda Raya No.45",
                description="Auditorium kapasitas 500 orang"
            ),
            Venue(
                name="Meeting Hall E",
                city="Bogor",
                address="Jl. Pajajaran No.10",
                description="Ruang meeting dan seminar"
            ),
            Venue(
                name="Grand Ballroom F",
                city="Jakarta",
                address="Jl. Gatot Subroto No.88",
                description="Ballroom premium kapasitas 800 orang"
            ),
            Venue(
                name="Outdoor Venue G",
                city="Tangerang",
                address="Jl. BSD Green Office Park",
                description="Venue outdoor untuk festival dan bazar"
            ),
            Venue(
                name="Community Hall H",
                city="Bekasi",
                address="Jl. Kalimalang No.22",
                description="Gedung serbaguna masyarakat"
            ),
            Venue(
                name="Theater I",
                city="Jakarta",
                address="Jl. Cikini Raya No.73",
                description="Teater untuk pertunjukan seni"
            ),
            Venue(
                name="Sports Hall J",
                city="Bandung",
                address="Jl. Pasteur No.30",
                description="Gedung olahraga dan event besar"
            )
        ]

        db.add_all(venues)
        db.commit()
        print("Venue seed completed")
    finally:
        db.close()

if __name__ == "__main__":
    seed()