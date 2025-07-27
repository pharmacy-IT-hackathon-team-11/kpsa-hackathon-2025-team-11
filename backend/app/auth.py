from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from app.config import settings
from app.models import TokenData, UserResponse, UserInfoResponse
from app.database import get_supabase, get_supabase_service

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12
)

# JWT token security
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password for storing"""
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        internal_id: str = payload.get("internal_id")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data = TokenData(user_id=user_id, internal_id=internal_id)
        return token_data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def _fetch_user_by_id(internal_id: str) -> UserResponse:
    """Helper function to fetch user by internal ID"""
    try:
        # Use service role client to bypass RLS policies
        supabase = get_supabase_service()
        response = supabase.table("users").select("*").eq("id", internal_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(**response.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user information"
        )

def _convert_to_user_info(user: UserResponse) -> UserInfoResponse:
    """Helper function to convert UserResponse to UserInfoResponse"""
    return UserInfoResponse(
        id=user.id,
        user_id=user.user_id,
        full_name=user.full_name,
        pharmacy_road_address=user.pharmacy_road_address,
        pharmacy_position_x=user.pharmacy_position_x,
        pharmacy_position_y=user.pharmacy_position_y,
        phone_number=user.phone_number,
        license_id=user.license_id,
        pharmacy_name=user.pharmacy_name,
        registration_status=user.registration_status,
        role=user.role,
        created_at=user.created_at,
        approved_at=user.approved_at,
        approved_by=user.approved_by
    )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserInfoResponse:
    """Get current authenticated user info"""
    token_data = verify_token(credentials.credentials)
    user = await _fetch_user_by_id(token_data.internal_id)
    
    # Check if user registration is approved
    if user.registration_status != "approved":
        status_messages = {
            "pending": "Your registration is pending admin approval",
            "rejected": "Your registration has been rejected"
        }
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=status_messages.get(user.registration_status, "Access denied")
        )
    
    return _convert_to_user_info(user)

async def get_current_admin_user(current_user: UserInfoResponse = Depends(get_current_user)) -> UserInfoResponse:
    """Get current authenticated admin user"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

async def get_current_user_full(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Get current authenticated user with full info (for internal use)"""
    token_data = verify_token(credentials.credentials)
    user = await _fetch_user_by_id(token_data.internal_id)
    
    # Check if user registration is approved
    if user.registration_status != "approved":
        status_messages = {
            "pending": "Your registration is pending admin approval",
            "rejected": "Your registration has been rejected"
        }
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=status_messages.get(user.registration_status, "Access denied")
        )
    
    return user

async def get_current_user_allow_pending(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserInfoResponse:
    """Get current authenticated user (allows pending status for registration info)"""
    token_data = verify_token(credentials.credentials)
    user = await _fetch_user_by_id(token_data.internal_id)
    return _convert_to_user_info(user)
