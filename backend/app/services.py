from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import json
import re
from fastapi import HTTPException, status
import openai

from app.models import (
    UserCreate, UserResponse, UserLogin, RegistrationRequest, 
    RegistrationAction, RegistrationStatus, UserRole,
    RegistrationUpdateResponse, UserInfoResponse,
    CustomerCreate, CustomerUpdate, CustomerResponse, CustomerKitUpdate,
    CustomerListResponse, GeneKitStatus,
    GeneKitData, GeneKitCreate, GeneKitUpdate, GeneReference, GeneReferenceCreate,
    CustomerGeneAnalysis, CustomerGeneAnalysisResponse,
    SymptomsReference, SymptomsReferenceCreate, SymptomsReferenceResponse,
    SymptomsAnalysisRequest, CustomerSymptomsAnalysis, CustomerSymptomsAnalysisResponse
)
from app.database import get_supabase, get_supabase_service
from app.auth import get_password_hash, verify_password
from app.config import settings

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate) -> UserResponse:
        """Create a new user in the database with pending status"""
        try:
            # Use service role client for user creation to bypass RLS
            supabase = get_supabase_service()
            
            # Check if user already exists (by user_id or license_id)
            existing_user = supabase.table("users").select("user_id, license_id").or_(
                f"user_id.eq.{user_data.user_id},license_id.eq.{user_data.license_id}"
            ).execute()
            
            if existing_user.data:
                existing_record = existing_user.data[0]
                if existing_record.get("user_id") == user_data.user_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="User with this user ID already exists"
                    )
                if existing_record.get("license_id") == user_data.license_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="User with this license ID already exists"
                    )
            
            # Hash password
            hashed_password = get_password_hash(user_data.password)
            
            # Create user record with pending status
            user_record = {
                "user_id": user_data.user_id,
                "full_name": user_data.full_name,
                "pharmacy_road_address": user_data.pharmacy_road_address,
                "pharmacy_position_x": user_data.pharmacy_position_x,
                "pharmacy_position_y": user_data.pharmacy_position_y,
                "phone_number": user_data.phone_number,
                "license_id": user_data.license_id,
                "pharmacy_name": user_data.pharmacy_name,
                "password_hash": hashed_password,
                "created_at": datetime.utcnow().isoformat(),
                "registration_status": RegistrationStatus.PENDING.value,
                "role": UserRole.USER.value
            }
            
            response = supabase.table("users").insert(user_record).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user"
                )
            
            user_data = response.data[0]
            return UserResponse(**user_data)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    @staticmethod
    async def authenticate_user(login_data: UserLogin) -> Optional[UserResponse]:
        """Authenticate user with user_id and password - only approved users can login"""
        try:
            # Use service role client for authentication to bypass RLS
            supabase = get_supabase_service()
            
            # Get user by user_id
            response = supabase.table("users").select("*").eq("user_id", login_data.user_id).execute()
            
            if not response.data:
                return None
            
            user_data = response.data[0]
            
            # Verify password
            if not verify_password(login_data.password, user_data["password_hash"]):
                return None
            
            user = UserResponse(**user_data)
            
            # Only allow approved users to login
            if user.registration_status != RegistrationStatus.APPROVED:
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserResponse]:
        """Get user by ID"""
        try:
            supabase = get_supabase()
            response = supabase.table("users").select("*").eq("id", user_id).execute()
            
            if not response.data:
                return None
            
            user_data = response.data[0]
            return UserResponse(**user_data)
            
        except Exception as e:
            logger.error(f"Error fetching user by ID: {e}")
            return None
    
    @staticmethod
    async def get_user_by_user_id(user_id: str) -> Optional[UserResponse]:
        """Get user by user_id"""
        try:
            # Use service role client to bypass RLS for user lookup
            supabase = get_supabase_service()
            response = supabase.table("users").select("*").eq("user_id", user_id).execute()
            
            if not response.data:
                return None
            
            user_data = response.data[0]
            return UserResponse(**user_data)
            
        except Exception as e:
            logger.error(f"Error fetching user by user_id: {e}")
            return None

    @staticmethod
    async def get_database_stats() -> Dict[str, int]:
        """Get database statistics including user and customer counts"""
        try:
            # Use service role client to access all data
            supabase = get_supabase_service()
            
            # Get total users count
            users_response = supabase.table("users").select("id, registration_status").execute()
            total_users = len(users_response.data)
            
            # Count users by status
            approved_users = len([u for u in users_response.data if u["registration_status"] == "approved"])
            pending_users = len([u for u in users_response.data if u["registration_status"] == "pending"])
            
            # Get total customers count
            customers_response = supabase.table("customers").select("id").execute()
            total_customers = len(customers_response.data)
            
            return {
                "total_users": total_users,
                "approved_users": approved_users,
                "pending_users": pending_users,
                "total_customers": total_customers
            }
            
        except Exception as e:
            logger.error(f"Error fetching database stats: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching database statistics"
            )

    @staticmethod
    async def get_user_customer_count(user_id: str) -> Dict[str, Any]:
        """Get customer count for a specific user"""
        try:
            # Use service role client to access data
            supabase = get_supabase_service()
            
            # Get user info
            user_response = supabase.table("users").select("user_id, full_name").eq("id", user_id).execute()
            
            if not user_response.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            user_data = user_response.data[0]
            
            # Get customer count for this user
            customers_response = supabase.table("customers").select("id").eq("pharmacy_id", user_id).execute()
            customer_count = len(customers_response.data)
            
            return {
                "user_id": user_data["user_id"],
                "full_name": user_data["full_name"],
                "customer_count": customer_count
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching user customer count: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching user customer count"
            )

class RegistrationService:
    @staticmethod
    async def get_pending_registrations() -> List[RegistrationRequest]:
        """Get all pending registration requests"""
        try:
            supabase = get_supabase()
            response = supabase.table("users").select(
                "id, user_id, full_name, pharmacy_road_address, pharmacy_position_x, pharmacy_position_y, phone_number, license_id, pharmacy_name, created_at, registration_status"
            ).eq("registration_status", RegistrationStatus.PENDING.value).execute()
            
            return [RegistrationRequest(**user) for user in response.data]
            
        except Exception as e:
            logger.error(f"Error fetching pending registrations: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching pending registrations"
            )
    
    @staticmethod
    async def update_registration_status(
        user_id: str, 
        action: RegistrationAction, 
        admin_user_id: str
    ) -> RegistrationUpdateResponse:
        """Update registration status (approve/reject)"""
        try:
            supabase = get_supabase()
            
            # Get current user data
            current_user_response = supabase.table("users").select("*").eq("id", user_id).execute()
            if not current_user_response.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            current_user = current_user_response.data[0]
            previous_status = current_user["registration_status"]
            
            # Prepare update data
            update_data = {
                "registration_status": action.action.value,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            # If approving, set approval timestamp and admin
            if action.action == RegistrationStatus.APPROVED:
                update_data.update({
                    "approved_at": datetime.utcnow().isoformat(),
                    "approved_by": admin_user_id
                })
            
            # Update the user
            response = supabase.table("users").update(update_data).eq("id", user_id).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update registration status"
                )
            
            # Get admin user info for response
            admin_response = supabase.table("users").select("user_id").eq("id", admin_user_id).execute()
            admin_user_id_str = admin_response.data[0]["user_id"] if admin_response.data else admin_user_id
            
            return RegistrationUpdateResponse(
                user_id=current_user["user_id"],
                internal_id=user_id,
                previous_status=RegistrationStatus(previous_status),
                new_status=action.action,
                updated_by=admin_user_id_str,
                message=f"Registration {action.action.value} successfully"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating registration status: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating registration status"
            )
    
    @staticmethod
    async def get_all_users_for_admin() -> List[UserResponse]:
        """Get all users for admin view"""
        try:
            supabase = get_supabase()
            response = supabase.table("users").select("*").execute()
            
            return [UserResponse(**user) for user in response.data]
            
        except Exception as e:
            logger.error(f"Error fetching all users: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching users"
            )

class CustomerService:
    @staticmethod
    async def create_customer(customer_data: CustomerCreate, pharmacy_id: str) -> CustomerResponse:
        """Create a new customer for a pharmacy"""
        try:
            supabase = get_supabase_service()  # Use service role for backend operations
            
            # Check if customer already exists for this pharmacy (same name + birth date)
            existing_customer = supabase.table("customers").select("*").eq(
                "pharmacy_id", pharmacy_id
            ).eq(
                "full_name", customer_data.full_name
            ).eq(
                "birth_date", customer_data.birth_date
            ).execute()
            
            if existing_customer.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Customer with this name and birth date already exists for your pharmacy"
                )
            
            # Create customer record
            customer_record = {
                "pharmacy_id": pharmacy_id,
                "full_name": customer_data.full_name,
                "birth_date": customer_data.birth_date,
                "phone_number": customer_data.phone_number,
                "description": customer_data.description,
                "gene_kit_identifier": customer_data.gene_kit_identifier,
                "gene_kit_status": customer_data.gene_kit_status.value,
                "kit_submission_date": customer_data.kit_submission_date.isoformat() if customer_data.kit_submission_date else None,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = supabase.table("customers").insert(customer_record).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create customer"
                )
            
            return CustomerResponse(**response.data[0])
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating customer"
            )
    
    @staticmethod
    async def get_customers_for_pharmacy(pharmacy_id: str) -> CustomerListResponse:
        """Get all customers for a specific pharmacy"""
        try:
            supabase = get_supabase_service()  # Use service role for backend operations
            
            # Get pharmacy info
            pharmacy_response = supabase.table("users").select("pharmacy_name").eq("id", pharmacy_id).execute()
            pharmacy_name = pharmacy_response.data[0]["pharmacy_name"] if pharmacy_response.data else "Unknown Pharmacy"
            
            # Get customers
            response = supabase.table("customers").select("*").eq("pharmacy_id", pharmacy_id).order("created_at", desc=False).execute()
            
            customers = [CustomerResponse(**customer) for customer in response.data]
            
            return CustomerListResponse(
                customers=customers,
                total_count=len(customers),
                pharmacy_name=pharmacy_name
            )
            
        except Exception as e:
            logger.error(f"Error fetching customers: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching customers"
            )
    
    @staticmethod
    async def get_customer_by_id(customer_id: str, pharmacy_id: str) -> CustomerResponse:
        """Get a specific customer by ID (only if belongs to the pharmacy)"""
        try:
            supabase = get_supabase_service()  # Use service role for backend operations
            
            response = supabase.table("customers").select("*").eq("id", customer_id).eq("pharmacy_id", pharmacy_id).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
            
            return CustomerResponse(**response.data[0])
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching customer: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching customer"
            )
    
    @staticmethod
    async def update_customer(customer_id: str, pharmacy_id: str, customer_data: CustomerUpdate) -> CustomerResponse:
        """Update customer information"""
        try:
            supabase = get_supabase_service()  # Use service role for backend operations
            
            # Check if customer exists and belongs to pharmacy
            existing_customer = supabase.table("customers").select("*").eq("id", customer_id).eq("pharmacy_id", pharmacy_id).execute()
            
            if not existing_customer.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
            
            # Prepare update data (only include fields that are not None)
            update_data = {}
            if customer_data.full_name is not None:
                update_data["full_name"] = customer_data.full_name
            if customer_data.birth_date is not None:
                update_data["birth_date"] = customer_data.birth_date
            if customer_data.phone_number is not None:
                update_data["phone_number"] = customer_data.phone_number
            if customer_data.description is not None:
                update_data["description"] = customer_data.description
            if customer_data.gene_kit_identifier is not None:
                update_data["gene_kit_identifier"] = customer_data.gene_kit_identifier
            if customer_data.gene_kit_status is not None:
                update_data["gene_kit_status"] = customer_data.gene_kit_status.value
            if customer_data.kit_submission_date is not None:
                update_data["kit_submission_date"] = customer_data.kit_submission_date.isoformat()
            
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            # Check for duplicate name+birth_date if these are being updated
            if customer_data.full_name or customer_data.birth_date:
                new_name = customer_data.full_name or existing_customer.data[0]["full_name"]
                new_birth_date = customer_data.birth_date or existing_customer.data[0]["birth_date"]
                
                duplicate_check = supabase.table("customers").select("id").eq(
                    "pharmacy_id", pharmacy_id
                ).eq(
                    "full_name", new_name
                ).eq(
                    "birth_date", new_birth_date
                ).neq("id", customer_id).execute()
                
                if duplicate_check.data:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Another customer with this name and birth date already exists for your pharmacy"
                    )
            
            response = supabase.table("customers").update(update_data).eq("id", customer_id).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update customer"
                )
            
            return CustomerResponse(**response.data[0])
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating customer: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating customer"
            )
    
    @staticmethod
    async def update_customer_kit_status(customer_id: str, pharmacy_id: str, kit_data: CustomerKitUpdate) -> CustomerResponse:
        """Update customer gene kit status and related information"""
        try:
            supabase = get_supabase_service()  # Use service role for backend operations
            
            # Check if customer exists and belongs to pharmacy
            existing_customer = supabase.table("customers").select("*").eq("id", customer_id).eq("pharmacy_id", pharmacy_id).execute()
            
            if not existing_customer.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
            
            update_data = {
                "gene_kit_status": kit_data.gene_kit_status.value,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            if kit_data.gene_kit_identifier is not None:
                update_data["gene_kit_identifier"] = kit_data.gene_kit_identifier
            
            if kit_data.kit_submission_date is not None:
                update_data["kit_submission_date"] = kit_data.kit_submission_date.isoformat()
            elif kit_data.gene_kit_status == GeneKitStatus.SUBMITTED and not existing_customer.data[0].get("kit_submission_date"):
                # Auto-set submission date if status is being set to submitted and no date exists
                update_data["kit_submission_date"] = datetime.utcnow().isoformat()
            
            response = supabase.table("customers").update(update_data).eq("id", customer_id).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update customer kit status"
                )
            
            return CustomerResponse(**response.data[0])
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating customer kit status: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating customer kit status"
            )
    
    @staticmethod
    async def delete_customer(customer_id: str, pharmacy_id: str) -> bool:
        """Delete a customer (only if belongs to the pharmacy)"""
        try:
            supabase = get_supabase_service()  # Use service role for backend operations
            
            # Check if customer exists and belongs to pharmacy
            existing_customer = supabase.table("customers").select("id").eq("id", customer_id).eq("pharmacy_id", pharmacy_id).execute()
            
            if not existing_customer.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
            
            response = supabase.table("customers").delete().eq("id", customer_id).execute()
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting customer: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting customer"
            )

class GeneKitService:
    @staticmethod
    async def create_gene_kit(gene_kit_data: GeneKitCreate) -> GeneKitData:
        """Create gene kit data"""
        try:
            supabase = get_supabase()
            
            # Check if gene kit already exists
            existing_kit = supabase.table("gene_kits").select("gene_kit_identifier").eq(
                "gene_kit_identifier", gene_kit_data.gene_kit_identifier
            ).execute()
            
            if existing_kit.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Gene kit with this identifier already exists"
                )
            
            kit_record = {
                "gene_kit_identifier": gene_kit_data.gene_kit_identifier,
                "gene_data": gene_kit_data.gene_data,
                "processed_at": datetime.utcnow().isoformat(),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            response = supabase.table("gene_kits").insert(kit_record).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create gene kit data"
                )
            
            return GeneKitData(**response.data[0])
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating gene kit: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating gene kit"
            )
    
    @staticmethod
    async def get_gene_kit_by_identifier(gene_kit_identifier: str) -> GeneKitData:
        """Get gene kit data by identifier"""
        try:
            supabase = get_supabase()
            
            response = supabase.table("gene_kits").select("*").eq(
                "gene_kit_identifier", gene_kit_identifier
            ).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Gene kit not found"
                )
            
            return GeneKitData(**response.data[0])
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching gene kit: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching gene kit"
            )
    
    @staticmethod
    async def update_gene_kit(gene_kit_identifier: str, gene_kit_data: GeneKitUpdate) -> GeneKitData:
        """Update gene kit data"""
        try:
            supabase = get_supabase()
            
            # Check if gene kit exists
            existing_kit = supabase.table("gene_kits").select("*").eq(
                "gene_kit_identifier", gene_kit_identifier
            ).execute()
            
            if not existing_kit.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Gene kit not found"
                )
            
            update_data = {"updated_at": datetime.utcnow().isoformat()}
            
            if gene_kit_data.gene_data is not None:
                update_data["gene_data"] = gene_kit_data.gene_data
            
            if gene_kit_data.processed_at is not None:
                update_data["processed_at"] = gene_kit_data.processed_at.isoformat()
            
            response = supabase.table("gene_kits").update(update_data).eq(
                "gene_kit_identifier", gene_kit_identifier
            ).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update gene kit"
                )
            
            return GeneKitData(**response.data[0])
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating gene kit: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating gene kit"
            )

class GeneReferenceService:
    @staticmethod
    async def create_gene_reference(reference_data: GeneReferenceCreate) -> GeneReference:
        """Create gene reference data"""
        try:
            supabase = get_supabase_service()  # Use service role for admin operations
            
            # Check if gene-representation pair already exists
            existing_ref = supabase.table("gene_reference").select("*").eq(
                "gene", reference_data.gene
            ).eq(
                "representation", reference_data.representation
            ).execute()
            
            if existing_ref.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Gene reference with this gene-representation pair already exists"
                )
            
            reference_record = {
                "gene": reference_data.gene,
                "representation": reference_data.representation,
                "snp": reference_data.snp,
                "related_nutrition": reference_data.related_nutrition,  # Supplement info
                "related_feature": reference_data.related_feature,
                "pmid": reference_data.pmid,
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = supabase.table("gene_reference").insert(reference_record).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create gene reference"
                )
            
            return GeneReference(**response.data[0])
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating gene reference: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating gene reference"
            )
    
    @staticmethod
    async def get_all_gene_references() -> List[GeneReference]:
        """Get all gene references"""
        try:
            supabase = get_supabase()  # Regular connection for reading
            
            response = supabase.table("gene_reference").select("*").order("gene", desc=False).execute()
            
            return [GeneReference(**ref) for ref in response.data]
            
        except Exception as e:
            logger.error(f"Error fetching gene references: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching gene references"
            )

class GeneAnalysisService:
    @staticmethod
    async def analyze_customer_genes(customer_id: str, pharmacy_id: str) -> CustomerGeneAnalysisResponse:
        """Analyze customer's genes against reference database"""
        try:
            supabase = get_supabase_service()  # Use service role for backend operations
            
            # Get customer info
            customer_response = supabase.table("customers").select("*").eq("id", customer_id).eq("pharmacy_id", pharmacy_id).execute()
            
            if not customer_response.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
            
            customer = customer_response.data[0]
            
            if not customer.get("gene_kit_identifier"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Customer does not have a gene kit identifier"
                )
            
            # Get gene kit data
            try:
                gene_kit = await GeneKitService.get_gene_kit_by_identifier(customer["gene_kit_identifier"])
            except HTTPException as e:
                if e.status_code == 404:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Gene kit data not found"
                    )
                raise
            
            # Get all gene references
            gene_references = await GeneReferenceService.get_all_gene_references()
            
            # Create reference lookup dictionary
            reference_lookup = {}
            for ref in gene_references:
                key = f"{ref.gene}|{ref.representation}"
                reference_lookup[key] = ref
            
            # Analyze each gene in the customer's kit
            analysis_results = []
            matches_found = 0
            
            for gene, customer_representation in gene_kit.gene_data.items():
                # Look for exact match first
                exact_match_key = f"{gene}|{customer_representation}"
                match_status = "no_match"
                reference_data = None
                
                if exact_match_key in reference_lookup:
                    reference_data = reference_lookup[exact_match_key]
                    match_status = "exact_match"
                    matches_found += 1
                else:
                    # Look for partial matches (same gene, different representation)
                    for ref_key, ref_data in reference_lookup.items():
                        ref_gene, ref_representation = ref_key.split("|", 1)
                        if ref_gene == gene:
                            reference_data = ref_data
                            match_status = "partial_match"
                            break
                
                # Create analysis result
                analysis_result = CustomerGeneAnalysis(
                    customer_id=customer_id,
                    gene_kit_identifier=gene_kit.gene_kit_identifier,
                    gene=gene,
                    customer_representation=customer_representation,
                    reference_representation=reference_data.representation if reference_data else "N/A",
                    snp=reference_data.snp if reference_data else "N/A",
                    related_nutrition=reference_data.related_nutrition if reference_data else None,
                    related_feature=reference_data.related_feature if reference_data else None,
                    pmid=reference_data.pmid if reference_data else None,
                    match_status=match_status
                )
                
                analysis_results.append(analysis_result)
            
            return CustomerGeneAnalysisResponse(
                customer_id=customer_id,
                customer_name=customer["full_name"],
                gene_kit_identifier=gene_kit.gene_kit_identifier,
                analysis_results=analysis_results,
                total_genes_analyzed=len(gene_kit.gene_data),
                matches_found=matches_found,
                analysis_date=datetime.utcnow()
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error analyzing customer genes: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error analyzing customer genes"
            )


class SymptomsReferenceService:
    @staticmethod
    async def get_all_symptoms_references() -> List[SymptomsReference]:
        """Get all symptoms reference data"""
        try:
            supabase = get_supabase_service()
            response = supabase.table("symptoms_reference").select("*").execute()
            
            return [
                SymptomsReference(
                    id=item["id"],
                    symptom=item["symptom"],
                    related_nutrition=item["related_nutrition"],
                    related_feature=item["related_feature"],
                    created_at=item["created_at"]
                )
                for item in response.data
            ]
            
        except Exception as e:
            logger.error(f"Error fetching symptoms references: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error fetching symptoms references"
            )

    @staticmethod
    async def get_symptoms_by_condition(symptom: str) -> List[SymptomsReference]:
        """Get symptoms reference data for a specific condition"""
        try:
            supabase = get_supabase_service()
            response = supabase.table("symptoms_reference").select("*").eq("symptom", symptom).execute()
            
            return [
                SymptomsReference(
                    id=item["id"],
                    symptom=item["symptom"],
                    related_nutrition=item["related_nutrition"],
                    related_feature=item["related_feature"],
                    created_at=item["created_at"]
                )
                for item in response.data
            ]
            
        except Exception as e:
            logger.error(f"Error fetching symptoms references for {symptom}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching symptoms references for {symptom}"
            )

    @staticmethod
    async def create_symptoms_reference(symptoms_ref: SymptomsReferenceCreate) -> SymptomsReference:
        """Create a new symptoms reference"""
        try:
            supabase = get_supabase_service()
            response = supabase.table("symptoms_reference").insert({
                "symptom": symptoms_ref.symptom,
                "related_nutrition": symptoms_ref.related_nutrition,
                "related_feature": symptoms_ref.related_feature
            }).execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create symptoms reference"
                )
                
            item = response.data[0]
            return SymptomsReference(
                id=item["id"],
                symptom=item["symptom"],
                related_nutrition=item["related_nutrition"],
                related_feature=item["related_feature"],
                created_at=item["created_at"]
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating symptoms reference: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating symptoms reference"
            )


class SymptomsAnalysisService:
    @staticmethod
    async def extract_symptoms_from_description(description: str) -> List[str]:
        """Extract disease/condition names from customer description using OpenAI"""
        try:
            if not settings.openai_api_key:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="OpenAI API key not configured"
                )
            
            # Initialize OpenAI client
            client = openai.OpenAI(api_key=settings.openai_api_key)
            
            # Get available symptoms from database
            available_symptoms = ["고혈압", "당뇨", "신부전", "부정맥"]  # These are from our CSV data
            symptoms_list = ", ".join(available_symptoms)
            
            # Create prompt for GPT
            prompt = f"""
다음 환자 설명에서 질환명을 추출해주세요. 
추출할 수 있는 질환명은 다음 중에서만 선택해주세요: {symptoms_list}

환자 설명: "{description}"

응답 형식:
- JSON 배열 형태로 응답
- 예시: ["고혈압", "당뇨"]
- 해당하는 질환이 없으면 빈 배열: []
- 질환명만 정확히 반환하고 다른 설명은 포함하지 마세요

응답:"""

            response = client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "당신은 의료 텍스트 분석 전문가입니다. 환자의 설명에서 정확한 질환명만을 추출합니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.1
            )
            
            # Extract symptoms from response
            response_text = response.choices[0].message.content.strip()
            
            try:
                # Try to parse as JSON
                extracted_symptoms = json.loads(response_text)
                if not isinstance(extracted_symptoms, list):
                    extracted_symptoms = []
            except json.JSONDecodeError:
                # Fallback: extract symptoms using regex
                extracted_symptoms = []
                for symptom in available_symptoms:
                    if symptom in response_text:
                        extracted_symptoms.append(symptom)
            
            # Filter to only include valid symptoms
            valid_symptoms = [s for s in extracted_symptoms if s in available_symptoms]
            
            return valid_symptoms
            
        except Exception as e:
            logger.error(f"Error extracting symptoms: {e}")
            # Fallback to simple keyword matching
            available_symptoms = ["고혈압", "당뇨", "신부전", "부정맥"]
            fallback_symptoms = []
            
            for symptom in available_symptoms:
                if symptom in description:
                    fallback_symptoms.append(symptom)
            
            return fallback_symptoms

    @staticmethod
    async def analyze_customer_symptoms(
        customer_id: str, 
        symptoms_request: SymptomsAnalysisRequest,
        pharmacy_id: str
    ) -> CustomerSymptomsAnalysisResponse:
        """Analyze customer's symptoms against reference database"""
        try:
            supabase = get_supabase_service()
            
            # Get customer info
            customer_response = supabase.table("customers").select("*").eq("id", customer_id).eq("pharmacy_id", pharmacy_id).execute()
            
            if not customer_response.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found"
                )
            
            customer = customer_response.data[0]
            
            # Extract symptoms from description
            extracted_symptoms = await SymptomsAnalysisService.extract_symptoms_from_description(
                symptoms_request.customer_description
            )
            
            # Get warnings for extracted symptoms
            analysis_results = []
            warnings_found = 0
            
            for symptom in extracted_symptoms:
                symptom_warnings = await SymptomsReferenceService.get_symptoms_by_condition(symptom)
                
                for warning in symptom_warnings:
                    analysis_result = CustomerSymptomsAnalysis(
                        customer_id=customer_id,
                        customer_description=symptoms_request.customer_description,
                        extracted_symptoms=extracted_symptoms,
                        symptom=warning.symptom,
                        related_nutrition=warning.related_nutrition,
                        related_feature=warning.related_feature,
                        match_confidence="high" if symptom in symptoms_request.customer_description else "medium"
                    )
                    analysis_results.append(analysis_result)
                    warnings_found += 1
            
            return CustomerSymptomsAnalysisResponse(
                customer_id=customer_id,
                customer_name=customer["full_name"],
                customer_description=symptoms_request.customer_description,
                extracted_symptoms=extracted_symptoms,
                analysis_results=analysis_results,
                total_symptoms_extracted=len(extracted_symptoms),
                warnings_found=warnings_found,
                analysis_date=datetime.utcnow()
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error analyzing customer symptoms: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error analyzing customer symptoms"
            )
