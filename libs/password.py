from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def hash_password(plain_password):
    return pwd_context.hash(plain_password)