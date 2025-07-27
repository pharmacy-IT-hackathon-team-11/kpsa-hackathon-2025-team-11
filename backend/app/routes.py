from datetime import timedelta
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
import logging

from app.models import (
    UserCreate, UserLogin, UserResponse, AuthResponse, 
    Token, MessageResponse, RegistrationRequest, RegistrationAction,
    PendingRegistrationsResponse, RegistrationUpdateResponse, UserInfoResponse, UserStatusResponse,
    DatabaseStatsResponse, UserCustomerCountResponse,
    CustomerCreate, CustomerUpdate, CustomerResponse, CustomerKitUpdate,
    CustomerListResponse, GeneKitCreate, GeneKitUpdate, GeneKitData,
    GeneReferenceCreate, GeneReference, CustomerGeneAnalysisResponse,
    SymptomsReference, SymptomsReferenceCreate, SymptomsReferenceResponse,
    SymptomsAnalysisRequest, CustomerSymptomsAnalysisResponse
)
from app.services import UserService, RegistrationService, CustomerService, GeneKitService, GeneReferenceService, GeneAnalysisService, SymptomsReferenceService, SymptomsAnalysisService
from app.database import get_supabase
from app.auth import (
    create_access_token, get_current_user, get_current_admin_user,
    get_current_user_allow_pending, get_current_user_full
)
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user - will be in pending status awaiting admin approval"""
    try:
        # Create user with pending status
        user = await UserService.create_user(user_data)
        
        return MessageResponse(
            message="Registration submitted successfully. Your account is pending admin approval.",
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/login", response_model=AuthResponse)
async def login(login_data: UserLogin):
    """Login with email and password - only approved users can login"""
    try:
        # Authenticate user
        user = await UserService.authenticate_user(login_data)
        
        if not user:
            # Check if user exists but is not approved
            supabase_user = await UserService.get_user_by_user_id(login_data.user_id)
            if supabase_user:
                if supabase_user.registration_status == "pending":
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Your registration is pending admin approval"
                    )
                elif supabase_user.registration_status == "rejected":
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Your registration has been rejected"
                    )
            
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
    """Get current authenticated user information (without email)"""
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

@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: UserInfoResponse = Depends(get_current_user)):
    """Logout current user (client-side token removal)"""
    return MessageResponse(
        message="Logout successful. Please remove the token from client storage.",
        success=True
    )

@router.get("/health")
async def auth_health_check():
    """Health check for authentication service"""
    return {
        "status": "healthy",
        "service": "authentication",
        "message": "Authentication service is running"
    }

@router.get("/my-customer-count", response_model=UserCustomerCountResponse)
async def get_my_customer_count(current_user: UserInfoResponse = Depends(get_current_user)):
    """Get customer count for the current authenticated user"""
    try:
        stats = await UserService.get_user_customer_count(current_user.id)
        
        return UserCustomerCountResponse(
            user_id=stats["user_id"],
            full_name=stats["full_name"],
            customer_count=stats["customer_count"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user customer count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user customer count"
        )

@router.get("/database-statistics", response_model=DatabaseStatsResponse)
async def get_database_statistics(current_user: UserInfoResponse = Depends(get_current_user)):
    """Get database statistics including total users and customers (All authenticated users)"""
    try:
        stats = await UserService.get_database_stats()
        
        return DatabaseStatsResponse(
            total_users=stats["total_users"],
            approved_users=stats["approved_users"],
            pending_users=stats["pending_users"],
            total_customers=stats["total_customers"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching database statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching database statistics"
        )

@router.get("/users/{user_id}/customer-count", response_model=UserCustomerCountResponse)
async def get_user_customer_count_by_id(
    user_id: str,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Get customer count for any specific user by their ID (All authenticated users)"""
    try:
        stats = await UserService.get_user_customer_count(user_id)
        
        return UserCustomerCountResponse(
            user_id=stats["user_id"],
            full_name=stats["full_name"],
            customer_count=stats["customer_count"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user customer count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user customer count"
        )

# Admin routes
admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("/pending-registrations", response_model=PendingRegistrationsResponse)
async def get_pending_registrations(admin_user: UserInfoResponse = Depends(get_current_admin_user)):
    """Get all pending registration requests (Admin only)"""
    try:
        pending_requests = await RegistrationService.get_pending_registrations()
        
        return PendingRegistrationsResponse(
            pending_registrations=pending_requests,
            total_count=len(pending_requests)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching pending registrations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching pending registrations"
        )

@admin_router.post("/registration/{user_id}/approve", response_model=RegistrationUpdateResponse)
async def approve_registration(
    user_id: str,
    action: RegistrationAction,
    admin_user: UserInfoResponse = Depends(get_current_admin_user)
):
    """Approve or reject a user registration (Admin only)"""
    try:
        # Get admin's full info to access the ID
        admin_full_info = await UserService.get_user_by_id(admin_user.id)
        if not admin_full_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin user not found"
            )
        
        result = await RegistrationService.update_registration_status(
            user_id=user_id,
            action=action,
            admin_user_id=admin_full_info.id
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating registration status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating registration status"
        )

@admin_router.get("/users", response_model=List[RegistrationRequest])
async def get_all_users(admin_user: UserInfoResponse = Depends(get_current_admin_user)):
    """Get all users with full pharmacy info (Admin only)"""
    try:
        users = await RegistrationService.get_all_users_for_admin()
        
        # Convert UserResponse to RegistrationRequest format for consistent admin view
        admin_users = []
        for user in users:
            admin_user_data = RegistrationRequest(
                id=user.id,
                user_id=user.user_id,
                full_name=user.full_name,
                pharmacy_road_address=user.pharmacy_road_address,
                pharmacy_position_x=user.pharmacy_position_x,
                pharmacy_position_y=user.pharmacy_position_y,
                phone_number=user.phone_number,
                license_id=user.license_id,
                pharmacy_name=user.pharmacy_name,
                created_at=user.created_at,
                registration_status=user.registration_status
            )
            admin_users.append(admin_user_data)
        
        return admin_users
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching users"
        )

@admin_router.get("/statistics", response_model=DatabaseStatsResponse)
async def get_database_statistics_admin(admin_user: UserInfoResponse = Depends(get_current_admin_user)):
    """Get database statistics including total users and customers (Admin endpoint for administrative dashboard)"""
    try:
        stats = await UserService.get_database_stats()
        
        return DatabaseStatsResponse(
            total_users=stats["total_users"],
            approved_users=stats["approved_users"],
            pending_users=stats["pending_users"],
            total_customers=stats["total_customers"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching database statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching database statistics"
        )

@admin_router.get("/users/{user_id}/customer-count", response_model=UserCustomerCountResponse)
async def get_user_customer_count_admin(
    user_id: str,
    admin_user: UserInfoResponse = Depends(get_current_admin_user)
):
    """Get customer count for a specific user (Admin endpoint for user management)"""
    try:
        stats = await UserService.get_user_customer_count(user_id)
        
        return UserCustomerCountResponse(
            user_id=stats["user_id"],
            full_name=stats["full_name"],
            customer_count=stats["customer_count"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user customer count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user customer count"
        )

# Include admin routes in the main router
router.include_router(admin_router)

# ============================================================================
# CUSTOMER MANAGEMENT ROUTES
# ============================================================================

customer_router = APIRouter(prefix="/customers", tags=["Customer Management"])

@customer_router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Create a new customer for the authenticated pharmacy"""
    try:
        customer = await CustomerService.create_customer(customer_data, current_user.id)
        return customer
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating customer"
        )

@customer_router.get("/", response_model=CustomerListResponse)
async def get_customers(current_user: UserInfoResponse = Depends(get_current_user)):
    """Get all customers for the authenticated pharmacy"""
    try:
        customers = await CustomerService.get_customers_for_pharmacy(current_user.id)
        return customers
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching customers"
        )

@customer_router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Get a specific customer by ID"""
    try:
        customer = await CustomerService.get_customer_by_id(customer_id, current_user.id)
        return customer
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching customer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching customer"
        )

@customer_router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    customer_data: CustomerUpdate,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Update customer information"""
    try:
        customer = await CustomerService.update_customer(customer_id, current_user.id, customer_data)
        return customer
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating customer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating customer"
        )

@customer_router.patch("/{customer_id}/kit-status", response_model=CustomerResponse)
async def update_customer_kit_status(
    customer_id: str,
    kit_data: CustomerKitUpdate,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Update customer gene kit status and related information"""
    try:
        customer = await CustomerService.update_customer_kit_status(customer_id, current_user.id, kit_data)
        return customer
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating customer kit status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating customer kit status"
        )

@customer_router.delete("/{customer_id}", response_model=MessageResponse)
async def delete_customer(
    customer_id: str,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Delete a customer"""
    try:
        await CustomerService.delete_customer(customer_id, current_user.id)
        return MessageResponse(
            message="Customer deleted successfully",
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting customer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting customer"
        )

# Include customer routes in the main router
router.include_router(customer_router)

# ============================================================================
# GENE KIT MANAGEMENT ROUTES
# ============================================================================

gene_kit_router = APIRouter(prefix="/gene-kits", tags=["Gene Kit Management"])

@gene_kit_router.post("/", response_model=GeneKitData, status_code=status.HTTP_201_CREATED)
async def create_gene_kit(
    gene_kit_data: GeneKitCreate,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Create gene kit data"""
    try:
        gene_kit = await GeneKitService.create_gene_kit(gene_kit_data)
        return gene_kit
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating gene kit: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating gene kit"
        )

@gene_kit_router.get("/{gene_kit_identifier}", response_model=GeneKitData)
async def get_gene_kit(
    gene_kit_identifier: str,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Get gene kit data by identifier"""
    try:
        gene_kit = await GeneKitService.get_gene_kit_by_identifier(gene_kit_identifier)
        return gene_kit
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching gene kit: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching gene kit"
        )

@gene_kit_router.put("/{gene_kit_identifier}", response_model=GeneKitData)
async def update_gene_kit(
    gene_kit_identifier: str,
    gene_kit_data: GeneKitUpdate,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Update gene kit data"""
    try:
        gene_kit = await GeneKitService.update_gene_kit(gene_kit_identifier, gene_kit_data)
        return gene_kit
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating gene kit: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating gene kit"
        )

# Include gene kit routes in the main router
router.include_router(gene_kit_router)

# ============================================================================
# GENE REFERENCE ROUTES
# ============================================================================

gene_ref_router = APIRouter(prefix="/gene-reference", tags=["Gene Reference"])

@gene_ref_router.post("/", response_model=GeneReference, status_code=status.HTTP_201_CREATED)
async def create_gene_reference(
    reference_data: GeneReferenceCreate,
    admin_user: UserInfoResponse = Depends(get_current_admin_user)
):
    """Create gene reference data (Admin only)"""
    try:
        gene_ref = await GeneReferenceService.create_gene_reference(reference_data)
        return gene_ref
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating gene reference: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating gene reference"
        )

@gene_ref_router.get("/", response_model=List[GeneReference])
async def get_gene_references(current_user: UserInfoResponse = Depends(get_current_user)):
    """Get all gene references"""
    try:
        gene_refs = await GeneReferenceService.get_all_gene_references()
        return gene_refs
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching gene references: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching gene references"
        )

# Include gene reference routes in the main router
router.include_router(gene_ref_router)

# ============================================================================
# GENE ANALYSIS ROUTES
# ============================================================================

gene_analysis_router = APIRouter(prefix="/gene-analysis", tags=["Gene Analysis"])

@gene_analysis_router.get("/customers/{customer_id}", response_model=CustomerGeneAnalysisResponse)
async def analyze_customer_genes(
    customer_id: str,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Analyze customer's genes against reference database"""
    try:
        analysis = await GeneAnalysisService.analyze_customer_genes(customer_id, current_user.id)
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing customer genes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error analyzing customer genes"
        )

# Include gene analysis routes in the main router
router.include_router(gene_analysis_router)

# ============================================================================
# SYMPTOMS REFERENCE ROUTES
# ============================================================================

symptoms_reference_router = APIRouter(prefix="/symptoms-reference", tags=["Symptoms Reference"])

@symptoms_reference_router.get("/", response_model=SymptomsReferenceResponse)
async def get_all_symptoms_references(
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Get all symptoms reference data"""
    try:
        symptoms_references = await SymptomsReferenceService.get_all_symptoms_references()
        return SymptomsReferenceResponse(
            data=symptoms_references,
            total_count=len(symptoms_references)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching symptoms references: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching symptoms references"
        )

@symptoms_reference_router.get("/symptoms/{symptom}", response_model=SymptomsReferenceResponse)
async def get_symptoms_by_condition(
    symptom: str,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Get symptoms reference data for a specific condition"""
    try:
        symptoms_references = await SymptomsReferenceService.get_symptoms_by_condition(symptom)
        return SymptomsReferenceResponse(
            data=symptoms_references,
            total_count=len(symptoms_references)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching symptoms references for {symptom}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching symptoms references for {symptom}"
        )

@symptoms_reference_router.post("/", response_model=SymptomsReference)
async def create_symptoms_reference(
    symptoms_ref: SymptomsReferenceCreate,
    current_user: UserInfoResponse = Depends(get_current_admin_user)
):
    """Create a new symptoms reference (admin only)"""
    try:
        return await SymptomsReferenceService.create_symptoms_reference(symptoms_ref)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating symptoms reference: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating symptoms reference"
        )

# Include symptoms reference routes in the main router
router.include_router(symptoms_reference_router)

# ============================================================================
# SYMPTOMS ANALYSIS ROUTES
# ============================================================================

symptoms_analysis_router = APIRouter(prefix="/symptoms-analysis", tags=["Symptoms Analysis"])

@symptoms_analysis_router.post("/customers/{customer_id}", response_model=CustomerSymptomsAnalysisResponse)
async def analyze_customer_symptoms(
    customer_id: str,
    symptoms_request: SymptomsAnalysisRequest,
    current_user: UserInfoResponse = Depends(get_current_user)
):
    """Analyze customer's symptoms against reference database"""
    try:
        analysis = await SymptomsAnalysisService.analyze_customer_symptoms(
            customer_id, symptoms_request, current_user.id
        )
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing customer symptoms: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error analyzing customer symptoms"
        )

# Include symptoms analysis routes in the main router
router.include_router(symptoms_analysis_router)
