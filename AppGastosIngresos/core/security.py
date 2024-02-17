from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"],
deprecated="auto")


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def verify_token(token:str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM])
        user: str = payload.get("sub") #obtiene el usuario del token
        return user
    except jwt.ExpiredSignatureError: #token expirado
        return None
    except JWTError:   
        return None


