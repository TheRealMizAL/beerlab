from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_passwd(plain, hashed):
    return pwd_context.verify(plain, hashed)


async def get_passwd_hash(passwd):
    return pwd_context.hash(passwd)
