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
print(f"API base URL: {API_BASE_URL}")

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

def test_auth_me():
    """Test GET /api/auth/me with auth token"""
    print("\n🧪 Testing GET /api/auth/me endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved user profile")
        else:
            print(f"❌ Failed to retrieve user profile. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected user fields
        required_fields = ["id", "username", "email", "role"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ User profile contains all required fields")
            print(f"✅ Username: {data['username']}, Role: {data['role']}")
        else:
            print(f"❌ User profile is missing required fields: {missing_fields}")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to auth/me endpoint: {e}")
        return False

def test_get_menu_items():
    """Test GET /api/menu/items endpoint"""
    print("\n🧪 Testing GET /api/menu/items endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/menu/items")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved menu items")
        else:
            print(f"❌ Failed to retrieve menu items. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} menu items")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are menu items, verify the structure of the first one
        if data:
            required_fields = ["id", "name", "description", "price", "category"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Menu item objects contain all required fields")
            else:
                print(f"❌ Menu item objects are missing required fields: {missing_fields}")
                return False
            
            # Count categories
            categories = set(item["category"] for item in data)
            print(f"✅ Found {len(categories)} categories: {', '.join(categories)}")
            
            # Check for expected categories
            expected_categories = [
                "INICIO", "SALAT", "KLEINER SALAT", "TAPA PAELLA", "TAPAS VEGETARIAN", 
                "TAPAS DE POLLO", "TAPAS DE CARNE", "TAPAS DE PESCADO", "KROKETTEN", 
                "PASTA", "PIZZA", "SNACKS", "DESSERT", "HELADOS"
            ]
            
            found_categories = [cat for cat in expected_categories if cat in categories]
            missing_categories = [cat for cat in expected_categories if cat not in categories]
            
            print(f"✅ Found {len(found_categories)} of {len(expected_categories)} expected categories")
            if missing_categories:
                print(f"⚠️ Missing categories: {', '.join(missing_categories)}")
            
            # Print some sample data
            print(f"📊 Sample menu items:")
            for i, item in enumerate(data[:5]):  # Show up to 5 samples
                print(f"  {i+1}. {item['name']} - {item['price']} ({item['category']})")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to menu/items endpoint: {e}")
        return False

def test_cms_homepage_get():
    """Test GET /api/cms/homepage endpoint"""
    print("\n🧪 Testing GET /api/cms/homepage endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/homepage")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved homepage content")
        else:
            print(f"❌ Failed to retrieve homepage content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["hero", "features", "specialties", "delivery"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
            for field in required_fields:
                print(f"  ✓ {field} section is present")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if hero section contains expected fields
        if "hero" in data:
            hero_fields = ["title", "subtitle", "description", "location", "background_image"]
            missing_hero_fields = [field for field in hero_fields if field not in data["hero"]]
            
            if not missing_hero_fields:
                print("✅ Hero section contains all required fields")
                print(f"✅ Hero title: {data['hero']['title']}")
            else:
                print(f"❌ Hero section is missing required fields: {missing_hero_fields}")
                return False
        
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/homepage endpoint: {e}")
        return False

def test_cms_locations_get():
    """Test GET /api/cms/locations endpoint"""
    print("\n🧪 Testing GET /api/cms/locations endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/locations")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved locations content")
        else:
            print(f"❌ Failed to retrieve locations content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["locations", "info_sections", "general_info"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if locations array is present and has items
        if "locations" in data and isinstance(data["locations"], list):
            print(f"✅ Locations array contains {len(data['locations'])} locations")
            
            # If there are locations, check the structure of the first one
            if data["locations"]:
                location_fields = ["name", "address", "phone", "email", "opening_hours"]
                missing_location_fields = [field for field in location_fields if field not in data["locations"][0]]
                
                if not missing_location_fields:
                    print("✅ Location objects contain all required fields")
                    print(f"✅ First location: {data['locations'][0]['name']}")
                    
                    # Check for Neustadt and Großenbrode locations
                    location_names = [loc["name"].lower() for loc in data["locations"]]
                    if any("neustadt" in name for name in location_names):
                        print("✅ Found Neustadt location")
                    else:
                        print("⚠️ Neustadt location not found")
                    
                    if any("großenbrode" in name or "grossenbrode" in name for name in location_names):
                        print("✅ Found Großenbrode location")
                    else:
                        print("⚠️ Großenbrode location not found")
                else:
                    print(f"❌ Location objects are missing required fields: {missing_location_fields}")
                    return False
        else:
            print("❌ Locations array is missing or not an array")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/locations endpoint: {e}")
        return False

def test_cms_about_get():
    """Test GET /api/cms/about endpoint"""
    print("\n🧪 Testing GET /api/cms/about endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/about")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved about content")
        else:
            print(f"❌ Failed to retrieve about content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["page_title", "hero_title", "story_title", "story_content", "team_title", "team_members", "values_title", "values"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if values field is present and is a list
        if "values" in data and isinstance(data["values"], list):
            print(f"✅ Values array contains {len(data['values'])} values")
        else:
            print("❌ Values array is missing or not an array")
            return False
        
        # Check if team_members array is present
        if "team_members" in data and isinstance(data["team_members"], list):
            print(f"✅ Team members array contains {len(data['team_members'])} members")
            
            # If there are team members, check the structure of the first one
            if data["team_members"]:
                member_fields = ["name", "position", "description"]
                missing_member_fields = [field for field in member_fields if field not in data["team_members"][0]]
                
                if not missing_member_fields:
                    print("✅ Team member objects contain all required fields")
                    print(f"✅ First team member: {data['team_members'][0]['name']}")
                else:
                    print(f"❌ Team member objects are missing required fields: {missing_member_fields}")
                    return False
        else:
            print("❌ Team members array is missing or not an array")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/about endpoint: {e}")
        return False

def test_cms_legal_get(page_type):
    """Test GET /api/cms/legal/{page_type} endpoint"""
    print(f"\n🧪 Testing GET /api/cms/legal/{page_type} endpoint...")
    
    try:
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/cms/legal/{page_type}")
        
        # Check if response is successful
        if response.status_code == 200:
            print(f"✅ Successfully retrieved {page_type} content")
        else:
            print(f"❌ Failed to retrieve {page_type} content. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_type", "title", "content"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
            print(f"✅ Title: {data['title']}")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if page_type matches the requested page_type
        if data["page_type"] == page_type:
            print(f"✅ Page type matches requested type: {page_type}")
        else:
            print(f"❌ Page type doesn't match requested type. Expected: {page_type}, Got: {data['page_type']}")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/legal/{page_type} endpoint: {e}")
        return False

def test_create_review():
    """Test POST /api/reviews endpoint"""
    print("\n🧪 Testing POST /api/reviews endpoint...")
    
    try:
        # Create payload
        payload = {
            "customer_name": "Elena Rodríguez",
            "rating": 5,
            "comment": "¡Excelente experiencia! La comida estaba deliciosa y el servicio fue impecable. Volveré pronto."
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
        
        # Check if date field is properly formatted as ISO date string
        try:
            datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            print("✅ Date field is properly formatted as ISO date string")
        except (ValueError, TypeError):
            print("❌ Date field is not properly formatted as ISO date string")
            return False, None
            
        # Check if review is not approved by default
        if data["is_approved"] == False:
            print("✅ Review is not approved by default as expected")
        else:
            print("❌ Review is approved by default, which is unexpected")
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create review endpoint: {e}")
        return False, None

def test_get_reviews():
    """Test GET /api/reviews endpoint"""
    print("\n🧪 Testing GET /api/reviews endpoint...")
    
    try:
        # Make GET request with approved_only=true
        response = requests.get(f"{API_BASE_URL}/reviews?approved_only=true")
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved approved reviews")
        else:
            print(f"❌ Failed to retrieve approved reviews. Status code: {response.status_code}")
            return False
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON with {len(data)} approved reviews")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response is a list
        if not isinstance(data, list):
            print("❌ Response is not a list")
            return False
        
        # If there are reviews, verify the structure of the first one
        if data:
            required_fields = ["id", "customer_name", "rating", "comment", "date", "is_approved"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Review objects contain all required fields")
            else:
                print(f"❌ Review objects are missing required fields: {missing_fields}")
                return False
            
            # Check if date field is properly formatted as ISO date string
            try:
                datetime.fromisoformat(data[0]['date'].replace('Z', '+00:00'))
                print("✅ Date field is properly formatted as ISO date string")
            except (ValueError, TypeError):
                print("❌ Date field is not properly formatted as ISO date string")
                return False
            
            # Print some sample data
            print(f"📊 Sample approved reviews:")
            for i, review in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {review['customer_name']} - {review['rating']}★ - {review['date']}")
                
            # Verify all reviews are approved
            all_approved = all(review["is_approved"] for review in data)
            if all_approved:
                print("✅ All reviews are correctly marked as approved")
            else:
                print("❌ Some reviews are marked as not approved in the approved reviews list")
                return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to reviews endpoint: {e}")
        return False

def test_admin_system_info():
    """Test GET /api/admin/system/info endpoint"""
    print("\n🧪 Testing GET /api/admin/system/info endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make GET request
        response = requests.get(f"{API_BASE_URL}/admin/system/info", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully retrieved system information")
        else:
            print(f"❌ Failed to retrieve system information. Status code: {response.status_code}")
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
        
        # Check if response contains expected sections
        required_sections = ["system", "mysql", "application"]
        missing_sections = [section for section in required_sections if section not in data]
        
        if not missing_sections:
            print("✅ Response contains all required sections")
        else:
            print(f"❌ Response is missing required sections: {missing_sections}")
            return False
        
        # Check MySQL section
        if "mysql" in data:
            mysql_info = data["mysql"]
            print(f"✅ MySQL version: {mysql_info.get('version', 'N/A')}")
            print(f"✅ MySQL connection status: {mysql_info.get('connection_status', 'N/A')}")
            
            # Check if database info is present
            if "database_info" in mysql_info:
                db_info = mysql_info["database_info"]
                print(f"✅ Database name: {db_info.get('name', 'N/A')}")
                print(f"✅ Number of tables: {db_info.get('tables_count', 'N/A')}")
            else:
                print("❌ MySQL database_info section is missing")
                return False
        else:
            print("❌ MySQL section is missing")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/system/info endpoint: {e}")
        return False

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
        
        # Check if response is a list (not a dictionary with a 'backups' key)
        if not isinstance(data, list):
            print(f"❌ Response is not a list. Got: {type(data)}")
            print(f"Response content: {data}")
            return False
        
        print(f"✅ Response is a list with {len(data)} backups")
        
        # If there are backups, verify the structure of the first one
        if data:
            required_fields = ["id", "filename", "type", "created_at", "created_by", "size_human"]
            missing_fields = [field for field in required_fields if field not in data[0]]
            
            if not missing_fields:
                print("✅ Backup objects contain all required fields")
            else:
                print(f"❌ Backup objects are missing required fields: {missing_fields}")
                return False
                
            # Print some sample data
            print(f"📊 Sample backups:")
            for i, backup in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {backup['filename']} - Type: {backup['type']}, Size: {backup['size_human']}, Created: {backup['created_at']}")
                
            # Check if created_at is properly formatted as ISO date string
            try:
                datetime.fromisoformat(data[0]['created_at'].replace('Z', '+00:00'))
                print("✅ created_at is properly formatted as ISO date string")
            except (ValueError, TypeError):
                print("❌ created_at is not properly formatted as ISO date string")
                return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/backup/list endpoint: {e}")
        return False

def test_create_database_backup():
    """Test POST /api/admin/backup/database endpoint"""
    print("\n🧪 Testing POST /api/admin/backup/database endpoint...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False, None
    
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
            
            # Check if response is SQL content
            if "Content-Disposition" in response.headers and "attachment" in response.headers["Content-Disposition"]:
                print("✅ Response contains downloadable SQL file")
                
                # Check if backup ID is in headers
                if "X-Backup-ID" in response.headers:
                    backup_id = response.headers["X-Backup-ID"]
                    print(f"✅ Backup ID: {backup_id}")
                    return True, backup_id
                else:
                    print("❌ Backup ID not found in response headers")
                    return False, None
            else:
                # If not a downloadable file, check if it's valid JSON
                try:
                    data = response.json()
                    print(f"✅ Response is valid JSON: {data}")
                    
                    # Check if response contains expected fields
                    if "id" in data:
                        print(f"✅ Backup ID: {data['id']}")
                        return True, data["id"]
                    else:
                        print("❌ Backup ID not found in response")
                        return False, None
                except json.JSONDecodeError:
                    print("❌ Response is not valid JSON or downloadable SQL file")
                    return False, None
        else:
            print(f"❌ Failed to create database backup. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False, None
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/backup/database endpoint: {e}")
        return False, None

def test_backup_download(backup_id):
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
            print("✅ Successfully retrieved backup download information")
        else:
            print(f"❌ Failed to retrieve backup download information. Status code: {response.status_code}")
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
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["message", "backup_info"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False
        
        # Check if backup_info contains expected fields
        backup_info = data["backup_info"]
        required_info_fields = ["id", "filename", "type", "created_at", "size_human"]
        missing_info_fields = [field for field in required_info_fields if field not in backup_info]
        
        if not missing_info_fields:
            print("✅ Backup info contains all required fields")
        else:
            print(f"❌ Backup info is missing required fields: {missing_info_fields}")
            return False
        
        # Check if backup ID matches
        if backup_info["id"] == backup_id:
            print(f"✅ Backup ID matches: {backup_id}")
        else:
            print(f"❌ Backup ID doesn't match requested ID. Expected: {backup_id}, Got: {backup_info['id']}")
            return False
            
        # Check if created_at is properly formatted as ISO date string
        try:
            datetime.fromisoformat(backup_info['created_at'].replace('Z', '+00:00'))
            print("✅ created_at is properly formatted as ISO date string")
        except (ValueError, TypeError):
            print("❌ created_at is not properly formatted as ISO date string")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/backup/download/{backup_id} endpoint: {e}")
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
            print(f"✅ Response is valid JSON: {data}")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains success message
        if "message" in data and "deleted" in data["message"].lower():
            print(f"✅ Response contains success message: {data['message']}")
        else:
            print("❌ Response does not contain expected success message")
            return False
            
        # Verify deletion by trying to download the backup
        verify_response = requests.get(f"{API_BASE_URL}/admin/backup/download/{backup_id}", headers=headers)
        if verify_response.status_code == 404:
            print("✅ Backup was successfully deleted (404 Not Found when trying to download)")
        else:
            print(f"❌ Backup may not have been deleted. Got status code {verify_response.status_code} when trying to download")
            return False
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to admin/backup/{backup_id} endpoint: {e}")
        return False

def run_mysql_migration_validation():
    """Run comprehensive validation tests for MySQL migration"""
    print("\n🔍 Starting Jimmy's Tapas Bar MySQL Migration Validation Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: MySQL Backend Authentication
    auth_success, token = test_auth_login()
    results["mysql_auth_login"] = auth_success
    
    if auth_success:
        results["mysql_auth_me"] = test_auth_me()
    else:
        results["mysql_auth_me"] = False
        print("❌ Skipping auth/me test due to failed login")
    
    # Test 2: Complete Menu System
    results["mysql_menu_items"] = test_get_menu_items()
    
    # Test 3: MySQL CMS Data Structure
    results["mysql_cms_homepage"] = test_cms_homepage_get()
    results["mysql_cms_locations"] = test_cms_locations_get()
    results["mysql_cms_about"] = test_cms_about_get()
    
    # Test 4: Legal pages
    for page_type in ["imprint", "privacy"]:
        results[f"mysql_cms_legal_{page_type}"] = test_cms_legal_get(page_type)
    
    # Test 5: MySQL Review System with Datetime Serialization
    review_success, review_id = test_create_review()
    results["mysql_review_create"] = review_success
    results["mysql_reviews_get"] = test_get_reviews()
    
    # Test 6: MySQL System Info
    if auth_success:
        results["mysql_system_info"] = test_admin_system_info()
    else:
        results["mysql_system_info"] = False
        print("❌ Skipping system info test due to failed login")
    
    # Test 7: MySQL Enhanced Backup System
    if auth_success:
        results["mysql_backup_list"] = test_backup_list()
        
        # Create database backup
        db_backup_success, db_backup_id = test_create_database_backup()
        results["mysql_database_backup"] = db_backup_success
        
        # Test backup download if database backup was created
        if db_backup_success and db_backup_id:
            results["mysql_backup_download"] = test_backup_download(db_backup_id)
            
            # Test backup deletion if database backup was created
            results["mysql_backup_delete"] = test_delete_backup(db_backup_id)
        else:
            results["mysql_backup_download"] = False
            results["mysql_backup_delete"] = False
            print("❌ Skipping backup download and delete tests due to failed database backup creation")
    else:
        results["mysql_backup_list"] = False
        results["mysql_database_backup"] = False
        results["mysql_backup_download"] = False
        results["mysql_backup_delete"] = False
        print("❌ Skipping backup system tests due to failed login")
    
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
    run_mysql_migration_validation()