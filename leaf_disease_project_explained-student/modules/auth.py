# auth.py - xử lý đăng nhập và đăng ký
import bcrypt
from .db import SessionLocal, User
from sqlalchemy.exc import IntegrityError

def hash_password(password):
    # Mã hóa mật khẩu
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode()

def check_password(password, hashed):
    # So sánh mật khẩu gõ vào với mật khẩu đã mã hóa
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(username, password):
    session = SessionLocal()
    try:
        user = User(username=username, password_hash=hash_password(password))
        session.add(user)
        session.commit()
        return True, "Account created successfully!"
    except IntegrityError:
        session.rollback()
        return False, "Account already exists."
    finally:
        session.close()

def login_user(username, password):
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    if user and check_password(password, user.password_hash):
        return True
    return False