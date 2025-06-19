from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

fake_users_db: dict[str, dict] = {}

def get_user(email: str):
    return fake_users_db.get(email)

def create_user(email: str, password: str):
    hashed = pwd_context.hash(password)
    fake_users_db[email] = {
        'email': email, 
        "hashed_password": hashed
    }
    return fake_users_db[email]

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

