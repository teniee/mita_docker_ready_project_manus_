from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import app.core.jwt_utils as jwt_utils
from app.api.auth.schemas import LoginIn  # noqa: E501
from app.api.auth.schemas import GoogleAuthIn, RegisterIn, TokenOut
from app.api.auth.services import authenticate_google  # noqa: E501
from app.api.auth.services import authenticate_user, register_user
from app.core.session import get_db
from app.services.auth_jwt_service import (
    blacklist_token,
    create_access_token,
    verify_token,
)

router = APIRouter(prefix="", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post(
    "/register",
    response_model=TokenOut,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterIn,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Create a new user account."""
    return register_user(payload, db)


@router.post("/login", response_model=TokenOut)
async def login(
    payload: LoginIn,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Authenticate an existing user."""
    return authenticate_user(payload, db)


@router.post("/refresh")
async def refresh_token(request: Request):
    """Issue a new access token using either token format."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token, scope="refresh_token")
    if payload:
        user_data = {k: payload[k] for k in payload}
        user_data.pop("exp", None)
        user_data.pop("scope", None)
        new_access = create_access_token(user_data)
        return {"access_token": new_access, "token_type": "bearer"}

    # Fallback for legacy tokens without `scope`
    try:
        legacy = jwt_utils.decode_token(token)
        if legacy.get("type") != "refresh":
            raise ValueError("Incorrect token type")
        user_id = str(legacy["sub"])
        access = jwt_utils.create_access_token(user_id)
        refresh = jwt_utils.create_refresh_token(user_id)
        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer",
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
async def logout(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    blacklist_token(token)
    return JSONResponse({"message": "Successfully logged out."})


@router.post("/google", response_model=TokenOut)
async def google_login(
    payload: GoogleAuthIn,
    db: Session = Depends(get_db),  # noqa: B008
):
    """Authenticate a user using a Google ID token."""
    return await authenticate_google(payload, db)
