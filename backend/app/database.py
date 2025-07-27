from supabase import create_client, Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Singleton class for Supabase client management"""
    _client: Client = None
    _service_client: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get Supabase client with anon key for user operations"""
        if cls._client is None:
            if not settings.supabase_url or not settings.supabase_key:
                raise ValueError("Supabase URL and anon key must be configured")
            
            cls._client = create_client(settings.supabase_url, settings.supabase_key)
            logger.info("Supabase client initialized")
        return cls._client
    
    @classmethod
    def get_service_client(cls) -> Client:
        """Get Supabase client with service role key for admin operations"""
        if cls._service_client is None:
            if not settings.supabase_url or not settings.supabase_service_role_key:
                raise ValueError("Supabase URL and service role key must be configured")
            
            cls._service_client = create_client(settings.supabase_url, settings.supabase_service_role_key)
            logger.info("Supabase service client initialized")
        return cls._service_client

# Convenience functions
def get_supabase() -> Client:
    """Get Supabase client instance"""
    return SupabaseClient.get_client()

def get_supabase_service() -> Client:
    """Get Supabase service client instance"""
    return SupabaseClient.get_service_client()
