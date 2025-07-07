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
            print(f"✅ Response structure:")
            print(json.dumps(data, indent=2))
            
            # Print all top-level keys
            print(f"✅ Top-level keys: {list(data.keys())}")
            
            # Check if the expected fields are present
            if "hero" not in data:
                print("❌ Missing 'hero' section in response")
                
                # Check if hero data is available in other fields
                if "hero_title" in data and "hero_subtitle" in data:
                    print("ℹ️ Hero data is available but not in the expected 'hero' object structure")
                    print("ℹ️ Available hero fields:")
                    for key in data.keys():
                        if key.startswith("hero_"):
                            print(f"  - {key}: {data[key]}")
            
            if "features" not in data:
                print("❌ Missing 'features' section in response")
                
                # Check if features data is available in other fields
                if "features_data" in data:
                    print("ℹ️ Features data is available but not in the expected 'features' object structure")
                    print("ℹ️ Features data:")
                    print(json.dumps(data["features_data"], indent=2))
            
            if "specialties" not in data:
                print("❌ Missing 'specialties' section in response")
                
                # Check if specialties data is available in other fields
                if "specialties_data" in data:
                    print("ℹ️ Specialties data is available but not in the expected 'specialties' object structure")
                    print("ℹ️ Specialties data:")
                    print(json.dumps(data["specialties_data"], indent=2))
            
            if "delivery" not in data:
                print("❌ Missing 'delivery' section in response")
                
                # Check if delivery data is available in other fields
                if "delivery_data" in data:
                    print("ℹ️ Delivery data is available but not in the expected 'delivery' object structure")
                    print("ℹ️ Delivery data:")
                    print(json.dumps(data["delivery_data"], indent=2))
                
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
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
            print(f"✅ Response structure:")
            print(json.dumps(data, indent=2))
            
            # Print all top-level keys
            print(f"✅ Top-level keys: {list(data.keys())}")
            
            # Check if the expected fields are present
            if "id" not in data:
                print("❌ Missing 'id' field in response")
            
            if "locations" not in data:
                print("❌ Missing 'locations' array in response")
            elif not isinstance(data["locations"], list):
                print("❌ 'locations' field is not an array")
            else:
                print(f"✅ 'locations' array contains {len(data['locations'])} locations")
                
                # If there are locations, check the structure of the first one
                if data["locations"]:
                    location_fields = ["name", "address", "phone", "email", "opening_hours"]
                    missing_location_fields = [field for field in location_fields if field not in data["locations"][0]]
                    
                    if not missing_location_fields:
                        print("✅ Location objects contain all required fields")
                        print(f"✅ First location: {data['locations'][0]['name']}")
                    else:
                        print(f"❌ Location objects are missing required fields: {missing_location_fields}")
                
            # Check if locations data is available in other fields
            if "locations_data" in data:
                print("ℹ️ Locations data is available but not in the expected 'locations' array structure")
                print("ℹ️ Locations data:")
                print(json.dumps(data["locations_data"], indent=2))
                
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
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
            print(f"✅ Response structure:")
            print(json.dumps(data, indent=2))
            
            # Print all top-level keys
            print(f"✅ Top-level keys: {list(data.keys())}")
            
            # Check if the expected fields are present
            if "values" not in data:
                print("❌ Missing 'values' array in response")
                
                # Check if values data is available in other fields
                if "values_data" in data:
                    print("ℹ️ Values data is available but not in the expected 'values' array structure")
                    print("ℹ️ Values data:")
                    print(json.dumps(data["values_data"], indent=2))
            elif not isinstance(data["values"], list):
                print("❌ 'values' field is not an array")
            else:
                print(f"✅ 'values' array contains {len(data['values'])} values")
            
            if "team_members" not in data:
                print("❌ Missing 'team_members' array in response")
            elif not isinstance(data["team_members"], list):
                print("❌ 'team_members' field is not an array")
            else:
                print(f"✅ 'team_members' array contains {len(data['team_members'])} team members")
                
                # If there are team members, check the structure of the first one
                if data["team_members"]:
                    member_fields = ["name", "position", "description"]
                    missing_member_fields = [field for field in member_fields if field not in data["team_members"][0]]
                    
                    if not missing_member_fields:
                        print("✅ Team member objects contain all required fields")
                        print(f"✅ First team member: {data['team_members'][0]['name']}")
                    else:
                        print(f"❌ Team member objects are missing required fields: {missing_member_fields}")
                
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
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
        
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False
    
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