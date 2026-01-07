from ariadne import MutationType
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password, verify_password, create_token

mutation = MutationType()

@mutation.field("register")
def register(_, info, username, password, role):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            return {
                "success": False,
                "message": "Username already exists"
            }

        user = User(
            username=username,
            password_hash=hash_password(password),
            role=role
        )
        db.add(user)
        db.commit()

        return {
            "success": True,
            "message": "User registered successfully"
        }
    finally:
        db.close()



@mutation.field("login")
def login(_, info, username, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return {
                "success": False,
                "message": "Invalid username or password",
                "access_token": None,
                "role": None
            }

        if not verify_password(password, user.password_hash):
            return {
                "success": False,
                "message": "Invalid username or password",
                "access_token": None,
                "role": None
            }

        token = create_token({
            "sub": user.username,
            "role": user.role
        })

        return {
            "success": True,
            "message": "Login successful",
            "access_token": token,
            "role": user.role
        }
    finally:
        db.close()
