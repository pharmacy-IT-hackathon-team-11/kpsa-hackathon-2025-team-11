from datetime import timedelta
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
import logging

from app.models import (
    UserCreate, UserLogin, UserResponse, AuthResponse, 
    Token, MessageResponse, RegistrationRequest, RegistrationAction,
    PendingRegistrationsResponse, RegistrationUpdateResponse, UserInfoResponse, UserStatusResponse,
    CountResponse, DatabaseStatsResponse
)
from app.services import UserService, RegistrationService, CustomerService, DatabaseStatsService
from app.auth import (
    create_access_token, get_current_user, get_current_admin_user,
    get_current_user_allow_pending
)
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=AuthResponse)
async def login(login_data: UserLogin):
    """Login with user_id and password - only approved users can login"""
    try:
        # Authenticate user
        user = await UserService.authenticate_user(login_data)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect user ID or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.user_id, "internal_id": user.id},
            expires_delta=access_token_expires
        )
        
        token = Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60
        )
        
        # Convert to UserInfoResponse
        user_info = UserInfoResponse(
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
        
        return AuthResponse(
            user=user_info,
            token=token,
            message="Login successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/me", response_model=UserInfoResponse)
async def get_current_user_info(current_user: UserInfoResponse = Depends(get_current_user_allow_pending)):
    """Get current authenticated user information"""
    return current_user

@router.get("/status", response_model=UserStatusResponse)
async def get_registration_status(current_user: UserInfoResponse = Depends(get_current_user_allow_pending)):
    """Get current user's registration status - simplified response"""
    return UserStatusResponse(
        user_id=current_user.user_id,
        full_name=current_user.full_name,
        registration_status=current_user.registration_status,
        role=current_user.role,
        created_at=current_user.created_at,
        approved_at=current_user.approved_at
    )

# Customer count endpoint for users
@router.get("/customers/count", response_model=CountResponse)
async def get_my_customer_count(current_user: UserInfoResponse = Depends(get_current_user)):
    """Get customer count for current user's pharmacy"""
    try:
        count = await CustomerService.get_customer_count_for_pharmacy(current_user.id)
        return CountResponse(
            count=count,
            message=f"Total customers for your pharmacy: {count}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting customer count for user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting customer count"
        )

# Admin routes
admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("/stats", response_model=DatabaseStatsResponse)
async def get_database_stats(admin_user: UserInfoResponse = Depends(get_current_admin_user)):
    """Get comprehensive database statistics (Admin only)"""
    try:
        return await DatabaseStatsService.get_database_statistics()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting database statistics"
        )

@admin_router.get("/users/count", response_model=CountResponse)
async def get_total_user_count(admin_user: UserInfoResponse = Depends(get_current_admin_user)):
    """Get total user count (Admin only)"""
    try:
        count = await UserService.get_total_user_count()
        return CountResponse(
            count=count,
            message=f"Total users in system: {count}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting user count"
        )

@admin_router.get("/customers/count", response_model=CountResponse)
async def get_total_customer_count(admin_user: UserInfoResponse = Depends(get_current_admin_user)):
    """Get total customer count (Admin only)"""
    try:
        count = await CustomerService.get_total_customer_count()
        return CountResponse(
            count=count,
            message=f"Total customers in system: {count}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting customer count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting customer count"
        )
