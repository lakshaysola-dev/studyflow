from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.schemas.auth import Token, UserCreate, UserLogin, UserRead
from app.services.defaults import create_default_block_tags

router = APIRouter(prefix="/auth", tags=["auth"])


async def _authenticate(db: DbSession, email: str, password: str) -> User:
    result = await db.execute(select(User).where(User.email == email.lower()))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
        )
    return user


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: DbSession) -> Token:
    existing = await db.execute(select(User).where(User.email == payload.email.lower()))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=payload.email.lower(),
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        timezone=payload.timezone,
    )
    db.add(user)
    await db.flush()
    await create_default_block_tags(db, user.id)
    await db.commit()
    await db.refresh(user)
    return Token(access_token=create_access_token(user.id), user=UserRead.model_validate(user))


@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db: DbSession) -> Token:
    user = await _authenticate(db, payload.email, payload.password)
    return Token(access_token=create_access_token(user.id), user=UserRead.model_validate(user))


@router.post("/token", response_model=Token, include_in_schema=False)
async def login_form(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession) -> Token:
    """OAuth2 password flow endpoint so the Swagger UI 'Authorize' button works."""
    user = await _authenticate(db, form.username, form.password)
    return Token(access_token=create_access_token(user.id), user=UserRead.model_validate(user))


@router.get("/me", response_model=UserRead)
async def me(current_user: CurrentUser) -> User:
    return current_user
