from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from dpapi import config, oauth2_scheme
from dpapi.db import get_db, user_crud
from dpapi.schema import login
from dpapi.schema.login import TokenData, UserCreate, UserBase, Token, UserCheck, UserInDB

TOKEN_TYPE_BEARER = "bearer"
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
LOGIN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
EXIST_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Conflict data exist",
    headers={"WWW-Authenticate": "Bearer"},
)

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str):
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise LOGIN_EXCEPTION
    if not verify_password(password, user.hashed_password):
        raise LOGIN_EXCEPTION
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config['SECRET_KEY'], algorithm=config['ALGORITHM'])
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, config['SECRET_KEY'], algorithms=[config['ALGORITHM']])
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(email=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = user_crud.get_user_by_email(db, token_data.email)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


async def get_current_active_user(current_user: UserCheck = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise LOGIN_EXCEPTION
    access_token_expires = timedelta(minutes=config['ACCESS_TOKEN_EXPIRE_MINUTES'])
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token/test/")
async def test_me(current_user: UserBase = Depends(get_current_active_user)):
    return [{"user": current_user}]


@router.post('/users/create', response_model=login.UserBase)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, user.email)
    if db_user is None:
        db_user = user_crud.save_user(db, UserInDB(email=user.email,
                                                   full_name=user.full_name,
                                                   hashed_password=get_password_hash(user.password),
                                                   disabled=False))
        return UserBase(email=db_user.email, full_name=db_user.full_name)
    raise EXIST_EXCEPTION


@router.get("/users/me/", response_model=UserBase)
async def read_users_me(current_user: UserBase = Depends(get_current_active_user)):
    return current_user


@router.get("/login", response_model=login.Token)
async def login(email: str, password: str, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, email, password)
    access_token_expires = timedelta(minutes=config['ACCESS_TOKEN_EXPIRE_MINUTES'])
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type=TOKEN_TYPE_BEARER)
