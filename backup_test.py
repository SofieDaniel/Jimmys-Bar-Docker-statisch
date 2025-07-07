#!/usr/bin/env python3
import requests
import json
import time
import sys
from datetime import datetime

# Get the backend URL from the frontend .env file
import os
from dotenv import load_dotenv

# Load the frontend .env file
load_dotenv("/app/frontend/.env")
BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://aef4033e-b196-49c4-b0b0-48e6da1eef23.preview.emergentagent.com")
API_BASE_URL = f"{BACKEND_URL}/api"

print(f"Using backend URL: {BACKEND_URL}")

# Global variable to store auth token
AUTH_TOKEN = None

def test_auth_login():
    """Test POST /api/auth/login with admin credentials"""
    print("\n🧪 Testing POST /api/auth/login endpoint...")
    global AUTH_TOKEN
    
    try:
        # Create payload with admin credentials
        payload = {
            "username": "admin",
            "password": "jimmy2024"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/auth/login", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully authenticated with admin credentials")
        else:
            print(f"❌ Failed to authenticate. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Incorrect username or password")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains token
        if "access_token" in data and "token_type" in data:
            print("✅ Response contains access token and token type")
            AUTH_TOKEN = data["access_token"]
            print(f"✅ Token type: {data['token_type']}")
        else:
            print("❌ Response does not contain expected token fields")
            return False, None
            
        return True, data["access_token"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to login endpoint: {e}")
        return False, None

def test_backup_list():
    """Test GET /api/admin/backup/list endpoint"""
    print("\n🧪 Testing GET /api/admin/backup/list endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/backup/list", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved backup list")
        else:
            print(f"❌ Failed to retrieve backup list. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains backups field
        if "backups" in data and isinstance(data["backups"], list):
            print(f"✅ Response contains backups list with {len(data['backups'])} backups")
            
            # If there are backups, check the structure of the first one
            if data["backups"]:
                backup = data["backups"][0]
                required_fields = ["id", "filename", "type", "created_at", "created_by", "size_human"]
                missing_fields = [field for field in required_fields if field not in backup]
                
                if not missing_fields:
                    print("✅ Backup objects contain all required fields")
                    print(f"✅ First backup: {backup['filename']} ({backup['type']}) - {backup['size_human']}")
                    
                    # Check if created_at is in ISO format
                    try:
                        datetime.fromisoformat(backup['created_at'])
                        print("✅ created_at is in valid ISO format")
                    except (ValueError, TypeError):
                        print("❌ created_at is not in valid ISO format")
                        return False
                else:
                    print(f"❌ Backup objects are missing required fields: {missing_fields}")
                    return False
        else:
            print("❌ Response does not contain expected 'backups' list")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to backup list endpoint: {e}")
        return False

def test_create_database_backup():
    """Test POST /api/admin/backup/database endpoint"""
    print("\n🧪 Testing POST /api/admin/backup/database endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/admin/backup/database", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created database backup")
        else:
            print(f"❌ Failed to create database backup. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False, None
        
        # Check if response contains backup file
        if "Content-Disposition" in response.headers and "attachment" in response.headers["Content-Disposition"]:
            print("✅ Response contains downloadable backup file")
            
            # Check if backup ID is in headers
            if "X-Backup-ID" in response.headers:
                backup_id = response.headers["X-Backup-ID"]
                print(f"✅ Backup ID: {backup_id}")
            else:
                print("❌ Response does not contain X-Backup-ID header")
                return False, None
            
            # Check if backup size is in headers
            if "X-Backup-Size" in response.headers:
                backup_size = response.headers["X-Backup-Size"]
                print(f"✅ Backup size: {backup_size} bytes")
            else:
                print("❌ Response does not contain X-Backup-Size header")
                return False, None
            
            # Check if response content is valid JSON
            try:
                backup_data = json.loads(response.content)
                print("✅ Backup content is valid JSON")
                
                # Check if backup data contains expected fields
                if "backup_info" in backup_data and "data" in backup_data:
                    print("✅ Backup data contains backup_info and data sections")
                    
                    # Check if backup_info contains expected fields
                    required_info_fields = ["created_at", "created_by", "version", "type", "collections_count", "total_documents"]
                    missing_info_fields = [field for field in required_info_fields if field not in backup_data["backup_info"]]
                    
                    if not missing_info_fields:
                        print("✅ backup_info contains all required fields")
                        print(f"✅ Backup created at: {backup_data['backup_info']['created_at']}")
                        print(f"✅ Backup created by: {backup_data['backup_info']['created_by']}")
                        print(f"✅ Backup type: {backup_data['backup_info']['type']}")
                        print(f"✅ Collections count: {backup_data['backup_info']['collections_count']}")
                        print(f"✅ Total documents: {backup_data['backup_info']['total_documents']}")
                    else:
                        print(f"❌ backup_info is missing required fields: {missing_info_fields}")
                        return False, None
                else:
                    print("❌ Backup data does not contain expected sections")
                    return False, None
            except json.JSONDecodeError:
                print("❌ Backup content is not valid JSON")
                return False, None
        else:
            print("❌ Response does not contain downloadable backup file")
            return False, None
            
        return True, backup_id
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create database backup endpoint: {e}")
        return False, None

def test_create_full_backup():
    """Test POST /api/admin/backup/full endpoint"""
    print("\n🧪 Testing POST /api/admin/backup/full endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/admin/backup/full", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created full backup")
        else:
            print(f"❌ Failed to create full backup. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False, None
        
        # Check if response contains backup file
        if "Content-Disposition" in response.headers and "attachment" in response.headers["Content-Disposition"]:
            print("✅ Response contains downloadable backup file")
            
            # Check if backup ID is in headers
            if "X-Backup-ID" in response.headers:
                backup_id = response.headers["X-Backup-ID"]
                print(f"✅ Backup ID: {backup_id}")
            else:
                print("❌ Response does not contain X-Backup-ID header")
                return False, None
            
            # Check if backup size is in headers
            if "X-Backup-Size" in response.headers:
                backup_size = response.headers["X-Backup-Size"]
                print(f"✅ Backup size: {backup_size} bytes")
            else:
                print("❌ Response does not contain X-Backup-Size header")
                return False, None
            
            # Check if response content is a ZIP file (starts with PK)
            if response.content[:2] == b'PK':
                print("✅ Backup content is a valid ZIP file")
            else:
                print("❌ Backup content is not a valid ZIP file")
                return False, None
        else:
            print("❌ Response does not contain downloadable backup file")
            return False, None
            
        return True, backup_id
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create full backup endpoint: {e}")
        return False, None

def test_download_backup(backup_id):
    """Test GET /api/admin/backup/download/{backup_id} endpoint"""
    print(f"\n🧪 Testing GET /api/admin/backup/download/{backup_id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/backup/download/{backup_id}", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully downloaded backup")
        else:
            print(f"❌ Failed to download backup. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 404:
                print("   Backup not found")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        if "message" in data and "backup_info" in data:
            print(f"✅ Response contains message and backup_info")
            print(f"✅ Message: {data['message']}")
            
            # Check if backup_info contains expected fields
            required_fields = ["id", "filename", "type", "size_human", "created_at"]
            missing_fields = [field for field in required_fields if field not in data["backup_info"]]
            
            if not missing_fields:
                print("✅ backup_info contains all required fields")
                print(f"✅ Backup ID: {data['backup_info']['id']}")
                print(f"✅ Filename: {data['backup_info']['filename']}")
                print(f"✅ Type: {data['backup_info']['type']}")
                print(f"✅ Size: {data['backup_info']['size_human']}")
                print(f"✅ Created at: {data['backup_info']['created_at']}")
                
                # Check if created_at is in ISO format
                try:
                    datetime.fromisoformat(data['backup_info']['created_at'])
                    print("✅ created_at is in valid ISO format")
                except (ValueError, TypeError):
                    print("❌ created_at is not in valid ISO format")
                    return False
            else:
                print(f"❌ backup_info is missing required fields: {missing_fields}")
                return False
        else:
            print("❌ Response does not contain expected fields")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to download backup endpoint: {e}")
        return False

def test_delete_backup(backup_id):
    """Test DELETE /api/admin/backup/{backup_id} endpoint"""
    print(f"\n🧪 Testing DELETE /api/admin/backup/{backup_id} endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make DELETE request
        response = requests.delete(f"{API_BASE_URL}/admin/backup/{backup_id}", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully deleted backup")
        else:
            print(f"❌ Failed to delete backup. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            elif response.status_code == 404:
                print("   Backup not found")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        if "message" in data and "deleted_backup" in data:
            print(f"✅ Response contains message and deleted_backup")
            print(f"✅ Message: {data['message']}")
            
            # Check if deleted_backup contains expected fields
            required_fields = ["id", "filename"]
            missing_fields = [field for field in required_fields if field not in data["deleted_backup"]]
            
            if not missing_fields:
                print("✅ deleted_backup contains all required fields")
                print(f"✅ Deleted backup ID: {data['deleted_backup']['id']}")
                print(f"✅ Deleted backup filename: {data['deleted_backup']['filename']}")
            else:
                print(f"❌ deleted_backup is missing required fields: {missing_fields}")
                return False
        else:
            print("❌ Response does not contain expected fields")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to delete backup endpoint: {e}")
        return False

def test_create_review():
    """Test POST /api/reviews endpoint with datetime serialization"""
    print("\n🧪 Testing POST /api/reviews endpoint with datetime serialization...")
    
    try:
        # Create payload
        payload = {
            "customer_name": "Maria García",
            "rating": 5,
            "comment": "¡Excelente comida! Las tapas son auténticas y el ambiente es muy acogedor. Volveré pronto."
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/reviews", json=payload)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created new review")
        else:
            print(f"❌ Failed to create review. Status code: {response.status_code}")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains expected fields
        required_fields = ["id", "customer_name", "rating", "comment", "date", "is_approved"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if fields match what we sent
        if (data["customer_name"] == payload["customer_name"] and 
            data["rating"] == payload["rating"] and
            data["comment"] == payload["comment"]):
            print("✅ Returned review data matches input")
        else:
            print(f"❌ Returned review data doesn't match input")
            return False, None
            
        # Check if review is not approved by default
        if data["is_approved"] == False:
            print("✅ Review is not approved by default as expected")
        else:
            print("❌ Review is approved by default, which is unexpected")
        
        # Check if date is in ISO format
        try:
            datetime.fromisoformat(data['date'])
            print("✅ date is in valid ISO format")
        except (ValueError, TypeError):
            print("❌ date is not in valid ISO format")
            return False, None
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create review endpoint: {e}")
        return False, None

def run_backup_tests():
    """Run all backup-related tests"""
    print("\n🔍 Starting Jimmy's Tapas Bar CMS Backup System Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Authentication login
    auth_success, token = test_auth_login()
    results["admin_login"] = auth_success
    
    if not auth_success:
        print("❌ Authentication failed. Cannot proceed with backup tests.")
        return False
    
    # Test 2: Backup list endpoint
    results["backup_list"] = test_backup_list()
    
    # Test 3: Create database backup
    db_backup_success, db_backup_id = test_create_database_backup()
    results["create_database_backup"] = db_backup_success
    
    # Test 4: Create full backup
    full_backup_success, full_backup_id = test_create_full_backup()
    results["create_full_backup"] = full_backup_success
    
    # Test 5: Download database backup
    if db_backup_success and db_backup_id:
        results["download_database_backup"] = test_download_backup(db_backup_id)
    else:
        results["download_database_backup"] = False
        print("❌ Skipping database backup download test due to failed creation")
    
    # Test 6: Download full backup
    if full_backup_success and full_backup_id:
        results["download_full_backup"] = test_download_backup(full_backup_id)
    else:
        results["download_full_backup"] = False
        print("❌ Skipping full backup download test due to failed creation")
    
    # Test 7: Delete database backup
    if db_backup_success and db_backup_id:
        results["delete_database_backup"] = test_delete_backup(db_backup_id)
    else:
        results["delete_database_backup"] = False
        print("❌ Skipping database backup deletion test due to failed creation")
    
    # Test 8: Delete full backup
    if full_backup_success and full_backup_id:
        results["delete_full_backup"] = test_delete_backup(full_backup_id)
    else:
        results["delete_full_backup"] = False
        print("❌ Skipping full backup deletion test due to failed creation")
    
    # Test 9: Review creation with datetime serialization
    review_success, review_id = test_create_review()
    results["create_review"] = review_success
    
    # Print summary
    print("\n📋 Test Summary")
    print("=" * 80)
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    # Overall result
    all_passed = all(results.values())
    print("\n🏁 Overall Result:", "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED")
    
    return all_passed

if __name__ == "__main__":
    run_backup_tests()