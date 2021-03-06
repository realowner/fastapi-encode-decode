from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password: str) -> str:
    return pwd_context.hash(password)

def verify_pass(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)