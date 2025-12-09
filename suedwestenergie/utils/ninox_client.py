"""Ninox Database Client - API wrapper for Ninox database integration"""

import asyncio
import logging
from typing import Dict, Any, Optional
from ninox import Ninox
from ..config import Config

logger = logging.getLogger(__name__)


class NinoxClient:
    """A client for interacting with Ninox database API"""
    
    def __init__(self):
        """Initialize Ninox client with environment configuration"""
        self.api_key = Config.NINOX_API_KEY
        self.database_id = Config.NINOX_DATABASE_ID
        self.table_id = Config.NINOX_TABLE_ID
        
        if not self.api_key or not self.database_id or not self.table_id:
            raise ValueError("Ninox configuration is incomplete. Please check your environment variables.")
        
        try:
            self.client = Ninox(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Ninox client: {e}")
            raise
    
    def save_contact_form_data(self, data: Dict[str, Any]) -> bool:
        """
        Save contact form data to Ninox database
        
        Args:
            data: Dictionary containing form data with keys like name, email, etc.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Prepare the record data
            record_data = {
                "fields": {
                    "Name": data.get("name", ""),
                    "Email": data.get("email", ""),
                    "Phone": data.get("phone", ""),
                    "Company": data.get("company", ""),
                    "Message": data.get("message", ""),
                    "SubmittedAt": data.get("submitted_at", "")
                }
            }
            
            # Save to the specified database and table
            result = self.client.databases[self.database_id].tables[self.table_id].records.create(**record_data)
            
            logger.info(f"Successfully saved contact form data to Ninox database. Record ID: {result.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save contact form data to Ninox: {e}")
            return False
    
    def get_record_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a record from Ninox database by ID
        
        Args:
            record_id: The ID of the record to retrieve
        
        Returns:
            Optional[Dict]: The record data or None if not found
        """
        try:
            record = self.client.databases[self.database_id].tables[self.table_id].records[record_id].get()
            return {
                "id": record.id,
                "fields": record.fields
            }
        except Exception as e:
            logger.error(f"Failed to retrieve record from Ninox: {e}")
            return None


# Global instance of Ninox client
_ninox_client = None


def get_ninox_client() -> NinoxClient:
    """
    Get or create a global instance of the Ninox client
    
    Returns:
        NinoxClient: The Ninox client instance
    """
    global _ninox_client
    if _ninox_client is None:
        _ninox_client = NinoxClient()
    return _ninox_client


def save_contact_to_ninox(data: Dict[str, Any]) -> bool:
    """
    Convenience function to save contact form data to Ninox database
    
    Args:
        data: Dictionary containing contact form data
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        client = get_ninox_client()
        return client.save_contact_form_data(data)
    except Exception as e:
        logger.error(f"Error saving contact to Ninox: {e}")
        return False