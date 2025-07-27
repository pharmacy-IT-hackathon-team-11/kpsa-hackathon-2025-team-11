from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class RegistrationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved" 
    REJECTED = "rejected"

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class GeneKitStatus(str, Enum):
    NOT_SUBMITTED = "not_submitted"
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class UserBase(BaseModel):
    full_name: str = Field(..., description="User full name")
    pharmacy_road_address: str = Field(..., description="Pharmacy road address")
    pharmacy_position_x: float = Field(..., description="Pharmacy position X coordinate")
    pharmacy_position_y: float = Field(..., description="Pharmacy position Y coordinate")
    phone_number: str = Field(..., description="Phone number")
    license_id: str = Field(..., description="Pharmacy license ID")
    pharmacy_name: str = Field(..., description="Pharmacy name")

class UserCreate(UserBase):
    user_id: str = Field(..., description="Unique user ID for authentication")
    password: str = Field(..., min_length=8, description="User password (minimum 8 characters)")

class UserLogin(BaseModel):
    user_id: str = Field(..., description="User ID")
    password: str = Field(..., description="User password")

class UserInfoResponse(BaseModel):
    """User info response (for user display)"""
    id: str = Field(..., description="User ID")
    user_id: str = Field(..., description="Unique user ID")
    full_name: str = Field(..., description="User full name")
    pharmacy_road_address: str = Field(..., description="Pharmacy road address")
    pharmacy_position_x: float = Field(..., description="Pharmacy position X coordinate")
    pharmacy_position_y: float = Field(..., description="Pharmacy position Y coordinate")
    phone_number: str = Field(..., description="Phone number")
    license_id: str = Field(..., description="Pharmacy license ID")
    pharmacy_name: str = Field(..., description="Pharmacy name")
    registration_status: RegistrationStatus = Field(default=RegistrationStatus.PENDING, description="Registration approval status")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    created_at: datetime = Field(..., description="User creation timestamp")
    approved_at: Optional[datetime] = Field(None, description="When the registration was approved")
    approved_by: Optional[str] = Field(None, description="Admin who approved the registration")
    
    class Config:
        from_attributes = True

class UserResponse(UserBase):
    """Complete user response (for internal/admin use)"""
    id: str = Field(..., description="User ID")
    user_id: str = Field(..., description="Unique user ID for authentication")
    created_at: datetime = Field(..., description="User creation timestamp")
    registration_status: RegistrationStatus = Field(default=RegistrationStatus.PENDING, description="Registration approval status")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    approved_at: Optional[datetime] = Field(None, description="When the registration was approved")
    approved_by: Optional[str] = Field(None, description="Admin who approved the registration")
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")

class TokenData(BaseModel):
    user_id: Optional[str] = None
    internal_id: Optional[str] = None  # Database UUID

class AuthResponse(BaseModel):
    user: UserInfoResponse  # Use UserInfoResponse
    token: Token
    message: str = Field(default="Authentication successful")

class MessageResponse(BaseModel):
    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Operation success status")

class RegistrationRequest(BaseModel):
    """Model for viewing registration requests (admin use)"""
    id: int
    user_id: str
    full_name: str
    pharmacy_road_address: str
    pharmacy_position_x: float
    pharmacy_position_y: float
    phone_number: str
    license_id: str
    pharmacy_name: str
    created_at: Optional[datetime] = None
    registration_status: str = "pending"

class RegistrationAction(BaseModel):
    """Model for admin actions on registration requests"""
    action: RegistrationStatus = Field(..., description="Action to take (approved/rejected)")
    reason: Optional[str] = Field(None, description="Reason for the action")

class PendingRegistrationsResponse(BaseModel):
    """Response model for pending registrations list"""
    pending_registrations: list[RegistrationRequest] = Field(..., description="List of pending registration requests")
    total_count: int = Field(..., description="Total number of pending requests")

class RegistrationUpdateResponse(BaseModel):
    """Response model for registration status updates"""
    user_id: str = Field(..., description="User ID")
    internal_id: str = Field(..., description="Internal Database ID")
    previous_status: RegistrationStatus = Field(..., description="Previous registration status")
    new_status: RegistrationStatus = Field(..., description="New registration status")
    updated_by: str = Field(..., description="Admin who performed the update")
    message: str = Field(..., description="Status message")

class UserStatusResponse(BaseModel):
    """Simplified response model for user status endpoint"""
    user_id: str = Field(..., description="User ID")
    full_name: str = Field(..., description="User full name")
    registration_status: RegistrationStatus = Field(..., description="Registration approval status")
    role: UserRole = Field(..., description="User role")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")
    approved_at: Optional[datetime] = Field(None, description="Account approval timestamp")

class DatabaseStatsResponse(BaseModel):
    """Response model for database statistics"""
    total_users: int = Field(..., description="Total number of users in the database")
    approved_users: int = Field(..., description="Number of approved users")
    pending_users: int = Field(..., description="Number of pending users")
    total_customers: int = Field(..., description="Total number of customers in the database")

class UserCustomerCountResponse(BaseModel):
    """Response model for user's customer count"""
    user_id: str = Field(..., description="User ID")
    full_name: str = Field(..., description="User full name")
    customer_count: int = Field(..., description="Number of customers for this user")

# Customer Models
class CustomerBase(BaseModel):
    full_name: str = Field(..., description="Customer full name")
    birth_date: str = Field(..., description="Birth date (7 numbers format: YYMMDD + check digit)", pattern="^[0-9]{7}$")
    phone_number: str = Field(..., description="Customer phone number")
    description: Optional[str] = Field(None, description="Customer description")
    gene_kit_identifier: Optional[str] = Field(None, description="Gene kit identifier code (nullable)")
    gene_kit_status: GeneKitStatus = Field(default=GeneKitStatus.NOT_SUBMITTED, description="Gene kit process status")
    kit_submission_date: Optional[datetime] = Field(None, description="Date when kit was submitted")

class CustomerCreate(CustomerBase):
    """Model for creating a new customer"""
    pass

class CustomerUpdate(BaseModel):
    """Model for updating customer information"""
    full_name: Optional[str] = Field(None, description="Customer full name")
    birth_date: Optional[str] = Field(None, description="Birth date (7 numbers format)", pattern="^[0-9]{7}$")
    phone_number: Optional[str] = Field(None, description="Customer phone number")
    description: Optional[str] = Field(None, description="Customer description")
    gene_kit_identifier: Optional[str] = Field(None, description="Gene kit identifier code")
    gene_kit_status: Optional[GeneKitStatus] = Field(None, description="Gene kit process status")
    kit_submission_date: Optional[datetime] = Field(None, description="Date when kit was submitted")

class CustomerResponse(CustomerBase):
    """Complete customer response"""
    id: str = Field(..., description="Customer ID")
    pharmacy_id: str = Field(..., description="Associated pharmacy (user) ID") 
    created_at: datetime = Field(..., description="Customer creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True

class CustomerListResponse(BaseModel):
    """Response model for customer list"""
    customers: list[CustomerResponse] = Field(..., description="List of customers")
    total_count: int = Field(..., description="Total number of customers")
    pharmacy_name: str = Field(..., description="Name of the pharmacy")

class CustomerKitUpdate(BaseModel):
    """Model for updating customer kit information"""
    gene_kit_identifier: Optional[str] = Field(None, description="Gene kit identifier code")
    gene_kit_status: GeneKitStatus = Field(..., description="Gene kit process status")
    kit_submission_date: Optional[datetime] = Field(None, description="Date when kit was submitted")

# Gene Kit Models
class GeneKitData(BaseModel):
    """Model for gene kit data - contains gene-representation pairs"""
    gene_kit_identifier: str = Field(..., description="Unique gene kit identifier")
    gene_data: Dict[str, str] = Field(..., description="Gene-representation key-value pairs")
    processed_at: Optional[datetime] = Field(None, description="When the gene data was processed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "gene_kit_identifier": "KIT-001",
                "gene_data": {
                    "APOE": "e3/e4",
                    "MTHFR": "C677T",
                    "COMT": "Val158Met"
                },
                "processed_at": "2025-07-27T10:30:00Z"
            }
        }

class GeneKitCreate(BaseModel):
    """Model for creating gene kit data"""
    gene_kit_identifier: str = Field(..., description="Unique gene kit identifier")
    gene_data: Dict[str, str] = Field(..., description="Gene-representation key-value pairs")

class GeneKitUpdate(BaseModel):
    """Model for updating gene kit data"""
    gene_data: Optional[Dict[str, str]] = Field(None, description="Gene-representation key-value pairs")
    processed_at: Optional[datetime] = Field(None, description="When the gene data was processed")

# Gene Reference Models
class GeneReference(BaseModel):
    """Model for gene reference data"""
    id: str = Field(..., description="Reference ID")
    gene: str = Field(..., description="Gene name")
    representation: str = Field(..., description="Gene representation/variant")
    snp: str = Field(..., description="SNP identifier")
    related_nutrition: Optional[str] = Field(None, description="Recommended nutritional supplement")
    related_feature: Optional[str] = Field(None, description="Related feature/trait")
    pmid: Optional[str] = Field(None, description="PubMed ID for reference")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True

class GeneReferenceCreate(BaseModel):
    """Model for creating gene reference data"""
    gene: str = Field(..., description="Gene name")
    representation: str = Field(..., description="Gene representation/variant")
    snp: str = Field(..., description="SNP identifier")
    related_nutrition: Optional[str] = Field(None, description="Recommended nutritional supplement")
    related_feature: Optional[str] = Field(None, description="Related feature/trait")
    pmid: Optional[str] = Field(None, description="PubMed ID for reference")

# Gene Analysis Models
class CustomerGeneAnalysis(BaseModel):
    """Model for customer gene analysis results"""
    customer_id: str = Field(..., description="Customer ID")
    gene_kit_identifier: str = Field(..., description="Gene kit identifier")
    gene: str = Field(..., description="Gene name")
    customer_representation: str = Field(..., description="Customer's gene representation")
    reference_representation: str = Field(..., description="Reference gene representation")
    snp: str = Field(..., description="SNP identifier")
    related_nutrition: Optional[str] = Field(None, description="Related nutrition information")
    related_feature: Optional[str] = Field(None, description="Related feature/trait")
    pmid: Optional[str] = Field(None, description="PubMed ID for reference")
    match_status: str = Field(..., description="Match status (exact_match, partial_match, no_match)")
    
class CustomerGeneAnalysisResponse(BaseModel):
    """Response model for customer gene analysis"""
    customer_id: str = Field(..., description="Customer ID")
    customer_name: str = Field(..., description="Customer name")
    gene_kit_identifier: str = Field(..., description="Gene kit identifier")
    analysis_results: List[CustomerGeneAnalysis] = Field(..., description="Gene analysis results")
    total_genes_analyzed: int = Field(..., description="Total number of genes analyzed")
    matches_found: int = Field(..., description="Number of matches found")
    analysis_date: datetime = Field(..., description="Analysis timestamp")

# Symptoms Reference Models
class SymptomsReference(BaseModel):
    """Model for symptoms reference data"""
    id: Optional[str] = Field(None, description="Unique identifier")
    symptom: str = Field(..., description="Disease/condition name")
    related_nutrition: str = Field(..., description="Supplement/ingredient to be cautious about")
    related_feature: str = Field(..., description="Warning reason/caution information")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")

class SymptomsReferenceCreate(BaseModel):
    """Model for creating symptoms reference data"""
    symptom: str = Field(..., description="Disease/condition name")
    related_nutrition: str = Field(..., description="Supplement/ingredient to be cautious about")
    related_feature: str = Field(..., description="Warning reason/caution information")

class SymptomsReferenceResponse(BaseModel):
    """Response model for symptoms reference data"""
    data: List[SymptomsReference] = Field(..., description="List of symptoms references")
    total_count: int = Field(..., description="Total number of records")

# Symptoms Analysis Models
class SymptomsAnalysisRequest(BaseModel):
    """Request model for symptoms analysis"""
    customer_description: str = Field(..., description="Customer's symptom description")

class CustomerSymptomsAnalysis(BaseModel):
    """Model for customer symptoms analysis results"""
    customer_id: str = Field(..., description="Customer ID")
    customer_description: str = Field(..., description="Customer's original description")
    extracted_symptoms: List[str] = Field(..., description="Symptoms extracted from description")
    symptom: str = Field(..., description="Disease/condition matched")
    related_nutrition: str = Field(..., description="Supplement/ingredient to be cautious about")
    related_feature: str = Field(..., description="Warning reason/caution information")
    match_confidence: Optional[str] = Field(None, description="Confidence level of the match")

class CustomerSymptomsAnalysisResponse(BaseModel):
    """Response model for customer symptoms analysis"""
    customer_id: str = Field(..., description="Customer ID")
    customer_name: str = Field(..., description="Customer name")
    customer_description: str = Field(..., description="Customer's original description")
    extracted_symptoms: List[str] = Field(..., description="Symptoms extracted from description")
    analysis_results: List[CustomerSymptomsAnalysis] = Field(..., description="Symptoms analysis results")
    total_symptoms_extracted: int = Field(..., description="Total number of symptoms extracted")
    warnings_found: int = Field(..., description="Number of warnings/cautions found")
    analysis_date: datetime = Field(..., description="Analysis timestamp")
