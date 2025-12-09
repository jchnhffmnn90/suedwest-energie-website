#!/usr/bin/env python3
"""
Test script to check environment variables and Ninox configuration
"""

import sys
import os

# Add the project path to sys.path
project_path = "/home/jchnhffmnn/Documents/suedwest-energie_website/suedwestenergie-reflex-projekt"
sys.path.insert(0, project_path)

def test_env_vars():
    """Test environment variables directly"""
    print("Testing environment variables directly...")
    
    # Check if environment variables are accessible
    api_key = os.getenv("NINOX_API_KEY")
    db_id = os.getenv("NINOX_DATABASE_ID")
    table_id = os.getenv("NINOX_TABLE_ID")
    
    print(f"NINOX_API_KEY from os.getenv: {api_key}")
    print(f"NINOX_DATABASE_ID from os.getenv: {db_id}")
    print(f"NINOX_TABLE_ID from os.getenv: {table_id}")
    
    # Now try to import and check via Config
    try:
        from suedwestenergie.config.env_config import EnvironmentConfig
        config = EnvironmentConfig()
        
        print(f"\nFrom EnvironmentConfig:")
        print(f"NINOX_API_KEY: {config.NINOX_API_KEY}")
        print(f"NINOX_DATABASE_ID: {config.NINOX_DATABASE_ID}")
        print(f"NINOX_TABLE_ID: {config.NINOX_TABLE_ID}")
        
        # Check if all values are properly set (not empty strings or placeholders)
        all_set = (
            config.NINOX_API_KEY and 
            config.NINOX_API_KEY != "your-ninox-api-key" and
            config.NINOX_DATABASE_ID and 
            config.NINOX_DATABASE_ID != "your-ninox-database-id" and
            config.NINOX_TABLE_ID and 
            config.NINOX_TABLE_ID != "your-ninox-table-id"
        )
        
        print(f"\nConfiguration complete: {all_set}")
        
        return all_set
    except Exception as e:
        print(f"Error importing config: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ninox_client():
    """Test if Ninox client can be created with current configuration"""
    try:
        from suedwestenergie.utils.ninox_client import NinoxClient
        
        try:
            client = NinoxClient()
            print("\n✅ NinoxClient created successfully!")
            return True
        except Exception as e:
            print(f"\n❌ Failed to create NinoxClient: {e}")
            return False
    except Exception as e:
        print(f"Error importing NinoxClient: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Checking current environment configuration...")
    config_ok = test_env_vars()
    client_ok = test_ninox_client()
    
    print(f"\nConfiguration OK: {config_ok}")
    print(f"Ninox Client OK: {client_ok}")
    
    if not config_ok:
        print("\n⚠️  Ninox configuration is incomplete!")
        print("You need to set the actual values for:")
        print("- NINOX_DATABASE_ID")
        print("- NINOX_TABLE_ID")
        print("\nThe NINOX_API_KEY is set correctly as: 26c696f0-ceca-11f0-8c01-8f5e51ac7afd")