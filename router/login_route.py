from fastapi import APIRouter, status, HTTPException
from database.database import SessionLocal
from models.schemas import Login, TokenData
from fastapi.params import Depends
from sqlalchemy.orm import Session
from models.models import Seller
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "2959f5d6c3e2a7403fd746408070a31053bb8f5cd9c46ed0d0460cfd0cf59b95"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter(tags = ["Login"])

pwd_context = CryptContext(schemes = ["bcrypt"],\
                          deprecated = "auto")
ouath2_scheme = OAuth2PasswordBearer(tokenUrl = "login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_token(data: dict):
    to_encode = data.copy()
    expire  = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    seller = db.query(Seller)\
               .filter(Seller.email == request.username)\
               .first()
    if not seller:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'Username not found/ Invalid User')
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'Inavlid password')
    access_token = generate_token(
        data = {"sub" : seller.email}
    )
    return {"access_token" : access_token, "token_type" : "bearer"}

def get_current_user(token : str = Depends(ouath2_scheme)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid auth credentials",
        headers = {'WWW-Authenticate' : "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username = username)
    except JWTError:
        raise credentials_exception