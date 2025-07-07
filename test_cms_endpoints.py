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
            print(f"✅ Response is valid JSON")
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
            print(f"✅ Response data: {json.dumps(data, indent=2)[:500]}...")  # Print first 500 chars
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["hero", "features", "specialties", "delivery"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
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
        
        # Check if features section contains expected fields
        if "features" in data:
            features_fields = ["title", "subtitle", "cards"]
            missing_features_fields = [field for field in features_fields if field not in data["features"]]
            
            if not missing_features_fields:
                print("✅ Features section contains all required fields")
                print(f"✅ Features title: {data['features']['title']}")
                print(f"✅ Features cards count: {len(data['features']['cards'])}")
            else:
                print(f"❌ Features section is missing required fields: {missing_features_fields}")
                return False
        
        # Check if specialties section contains expected fields
        if "specialties" in data:
            specialties_fields = ["title", "cards"]
            missing_specialties_fields = [field for field in specialties_fields if field not in data["specialties"]]
            
            if not missing_specialties_fields:
                print("✅ Specialties section contains all required fields")
                print(f"✅ Specialties title: {data['specialties']['title']}")
                print(f"✅ Specialties cards count: {len(data['specialties']['cards'])}")
            else:
                print(f"❌ Specialties section is missing required fields: {missing_specialties_fields}")
                return False
        
        # Check if delivery section contains expected fields
        if "delivery" in data:
            delivery_fields = ["title", "description", "button_text", "button_url"]
            missing_delivery_fields = [field for field in delivery_fields if field not in data["delivery"]]
            
            if not missing_delivery_fields:
                print("✅ Delivery section contains all required fields")
                print(f"✅ Delivery title: {data['delivery']['title']}")
            else:
                print(f"❌ Delivery section is missing required fields: {missing_delivery_fields}")
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
            print(f"✅ Response data: {json.dumps(data, indent=2)[:500]}...")  # Print first 500 chars
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_title", "page_description", "locations"]
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
            print(f"✅ Response data: {json.dumps(data, indent=2)[:500]}...")  # Print first 500 chars
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
        
        # Check if response contains expected fields
        required_fields = ["id", "page_title", "hero_title", "story_title", "story_content", "team_title", "team_members", "values_title", "values"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
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
        
        # Check if values array is present
        if "values" in data and isinstance(data["values"], list):
            print(f"✅ Values array contains {len(data['values'])} values")
        else:
            print("❌ Values array is missing or not an array")
            return False
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to cms/about endpoint: {e}")
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
                
            # Print some sample data
            print(f"📊 Sample menu items:")
            for i, item in enumerate(data[:3]):  # Show up to 3 samples
                print(f"  {i+1}. {item['name']} - {item['price']} ({item['category']})")
                
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to menu/items endpoint: {e}")
        return False

def run_cms_tests():
    """Run tests for CMS endpoints after MySQL migration"""
    print("\n🔍 Starting Jimmy's Tapas Bar CMS Endpoints Tests after MySQL Migration")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test authentication first
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    if auth_success:
        results["auth_me"] = test_auth_me()
    else:
        results["auth_me"] = False
        print("❌ Skipping auth/me test due to failed login")
    
    # Test CMS endpoints
    results["cms_homepage"] = test_cms_homepage_get()
    results["cms_locations"] = test_cms_locations_get()
    results["cms_about"] = test_cms_about_get()
    
    # Test menu items
    results["menu_items"] = test_get_menu_items()
    
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
    run_cms_tests()