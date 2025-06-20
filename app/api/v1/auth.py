from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user import UserCreate, Token
from app.models.user import create_user, get_user, verify_password
from app.core.security import create_access_token, decode_token
from app.core.database import async_session
from datetime import timedelta

router = APIRouter()
oauth2_scheme = HTTPBearer()

async def get_db_session():
    async with async_session() as session:
        yield session

@router.post("/register", response_model=dict)
async def register(user: UserCreate, session: AsyncSession = Depends(get_db_session)):
    existing_user = await get_user(session, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    

    await create_user(session, user.email, user.password)
    return {"message":"User registered successfully"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session:AsyncSession = Depends(get_db_session)):
    user = await get_user(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(
        {"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": token, "token_type":'bearer'}


@router.get("/me")
async def me(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return {'token':payload['sub']}

