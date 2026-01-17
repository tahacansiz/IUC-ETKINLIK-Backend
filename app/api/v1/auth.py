from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, AuthResponse
from app.schemas.user import UserOut

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login endpoint
    Frontend expects: { user, token }
    """
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya şifre hatalı"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya şifre hatalı"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Hesap aktif değil"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return AuthResponse(
        user=UserOut.model_validate(user),
        token=access_token
    )


@router.post("/register", response_model=AuthResponse)
async def register(
    register_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register endpoint
    Frontend sends: { fullName, email, password, role }
    """
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == register_data.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email adresi zaten kullanılıyor"
        )
    
    # Create new user
    hashed_pwd = hash_password(register_data.password)
    new_user = User(
        full_name=register_data.full_name,
        email=register_data.email,
        hashed_password=hashed_pwd,
        role=register_data.role
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.id})
    
    return AuthResponse(
        user=UserOut.model_validate(new_user),
        token=access_token
    )


@router.post("/logout")
async def logout():
    """
    Logout endpoint
    In a stateless JWT setup, client just discards the token
    """
    return {"detail": "Çıkış başarılı"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh token endpoint
    For simplicity, this just returns a new token
    In production, you'd validate a refresh token
    """
    # In a real implementation, you'd validate the refresh token
    # and issue a new access token
    return TokenResponse(
        token="new_token_placeholder",
        refresh_token="new_refresh_token_placeholder"
    )


@router.post("/forgot-password")
async def forgot_password(email: str, db: AsyncSession = Depends(get_db)):
    """
    Forgot password endpoint
    """
    # In production, send password reset email
    return {"detail": "Şifre sıfırlama e-postası gönderildi"}
