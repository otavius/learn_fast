from sqlalchemy.orm import Session 
from datetime import timedelta, datetime
import pytz
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from models import User as UserModel 
from schemas import  UserCreate
from passlib.context import CryptContext

SECRET_KEY = "mysecretkey"
EXPIRE_MINUTES = 60 * 24 * 90 # 90 days 
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token") # localhost:8000/token
bcrypt_context = CryptContext(schemes=["bcrypt"])

# check existing user with the same username or email 
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user:
        return db_user 
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        return db_user 
    return None 

# create token 
async def create_access_token(id: int, username: str):
    encode = {"sub": username, "id": id}
    expires = datetime.now(pytz.utc) + timedelta(minutes=EXPIRE_MINUTES)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# get current user from token 
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        # expires: datetime = payload.get("exp")
        # timestamp = expires
        # date_time_exp = datetime.fromtimestamp(timestamp)
        # if (expires > datetime.now()):
        #     return None
        if username is None or id is None:
            return None
        db_user = db.query(UserModel).filter(UserModel.id == id).first()
    except JWTError:
        return None 
    return db_user
    
# create user
async def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
        username = user.username,
        email = user.email,
        hashed_password = bcrypt_context.hash(user.password)
    )
    db.add(db_user)
    db.commit()
    return db_user

# authenticate
async def authenticate(db: Session, username: str, password: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not db_user:
        return None
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return None 
    return db_user 