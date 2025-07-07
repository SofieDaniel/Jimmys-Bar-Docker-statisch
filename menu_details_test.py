#!/usr/bin/env python3
import requests
import json
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

def test_get_menu_items_detailed():
    """Test GET /api/menu/items endpoint with focus on detailed dish information"""
    print("\n🧪 Testing GET /api/menu/items endpoint for detailed dish information...")
    
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
        
        # If there are no menu items, report it
        if not data:
            print("⚠️ No menu items found in the database")
            return True
        
        # Analyze detailed fields for each menu item
        detailed_fields = [
            "detailed_description", 
            "ingredients", 
            "origin", 
            "preparation_method", 
            "allergens", 
            "additives",
            "details"
        ]
        
        # Track which fields are populated across all items
        populated_fields = {field: 0 for field in detailed_fields}
        total_items = len(data)
        
        print("\n📊 Menu Items Analysis:")
        print("=" * 80)
        
        # Print header for each item
        for i, item in enumerate(data):
            print(f"\n🍽️ Item {i+1}: {item['name']} ({item['category']})")
            print(f"  Price: {item['price']}")
            print(f"  Basic description: {item['description']}")
            
            # Check and display detailed fields
            for field in detailed_fields:
                value = item.get(field)
                if value:
                    populated_fields[field] += 1
                    print(f"  ✅ {field}: {value}")
                else:
                    print(f"  ❌ {field}: Not provided")
            
            # Check dietary information
            dietary_info = []
            if item.get('vegetarian'):
                dietary_info.append("Vegetarian")
            if item.get('vegan'):
                dietary_info.append("Vegan")
            if item.get('glutenfree'):
                dietary_info.append("Gluten-free")
                
            if dietary_info:
                print(f"  🥗 Dietary info: {', '.join(dietary_info)}")
            else:
                print(f"  ❌ No dietary information provided")
                
            print("-" * 80)
        
        # Print summary of populated fields
        print("\n📈 Summary of Detailed Information:")
        print("=" * 80)
        for field in detailed_fields:
            percentage = (populated_fields[field] / total_items) * 100 if total_items > 0 else 0
            print(f"  {field}: {populated_fields[field]}/{total_items} items ({percentage:.1f}%)")
        
        # Overall assessment
        well_described = all(populated_fields[field] == total_items for field in ["detailed_description", "ingredients"])
        partially_described = any(populated_fields[field] > 0 for field in detailed_fields)
        
        if well_described:
            print("\n✅ All menu items have comprehensive detailed descriptions and ingredients")
        elif partially_described:
            print("\n⚠️ Some menu items have detailed information, but it's not consistent across all items")
        else:
            print("\n❌ Menu items lack detailed information beyond basic descriptions")
            
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to menu/items endpoint: {e}")
        return False

def test_create_menu_item_with_details():
    """Test POST /api/menu/items endpoint with detailed information"""
    print("\n🧪 Testing POST /api/menu/items endpoint with detailed information...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Create payload with detailed information
        payload = {
            "name": "Paella de Mariscos",
            "description": "Traditionelle spanische Paella mit Meeresfrüchten",
            "detailed_description": "Eine authentische valencianische Paella, zubereitet nach traditionellem Rezept mit Safran und einer Vielzahl von frischen Meeresfrüchten aus der Ostsee und dem Mittelmeer.",
            "price": "18,90 €",
            "category": "Hauptgerichte",
            "ingredients": "Rundkornreis, Safran, Garnelen, Muscheln, Tintenfisch, Paprika, Erbsen, Olivenöl, Knoblauch, Zwiebeln, Tomaten, Fischfond",
            "origin": "Valencia, Spanien",
            "allergens": "Schalentiere, Weichtiere, kann Spuren von Gluten enthalten",
            "additives": "Keine künstlichen Zusatzstoffe",
            "preparation_method": "Traditionell in einer Paella-Pfanne über offenem Feuer zubereitet",
            "vegetarian": False,
            "vegan": False,
            "glutenfree": True,
            "order_index": 5
        }
        
        # Make POST request
        response = requests.post(f"{API_BASE_URL}/menu/items", json=payload, headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully created new menu item with detailed information")
        else:
            print(f"❌ Failed to create menu item. Status code: {response.status_code}")
            if response.status_code == 401:
                print("   Authentication failed: Invalid or expired token")
            elif response.status_code == 403:
                print("   Authorization failed: Insufficient permissions")
            return False, None
        
        # Check if response is valid JSON
        try:
            data = response.json()
            print(f"✅ Response is valid JSON")
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            return False, None
        
        # Check if response contains expected fields
        required_fields = ["id", "name", "description", "detailed_description", "price", "category", 
                          "ingredients", "origin", "allergens", "additives", "preparation_method"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if not missing_fields:
            print("✅ Response contains all required fields")
        else:
            print(f"❌ Response is missing required fields: {missing_fields}")
            return False, None
        
        # Check if detailed fields match what we sent
        detailed_fields = ["detailed_description", "ingredients", "origin", "allergens", 
                          "additives", "preparation_method"]
        
        all_match = True
        for field in detailed_fields:
            if data[field] == payload[field]:
                print(f"✅ {field} matches input")
            else:
                print(f"❌ {field} doesn't match input. Expected: {payload[field]}, Got: {data[field]}")
                all_match = False
        
        if all_match:
            print("✅ All detailed fields were saved correctly")
        else:
            print("❌ Some detailed fields were not saved correctly")
            
        return True, data["id"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to create menu item endpoint: {e}")
        return False, None

def delete_test_menu_item(item_id):
    """Delete the test menu item we created"""
    print(f"\n🧪 Cleaning up: Deleting test menu item {item_id}...")
    
    if not AUTH_TOKEN:
        print("❌ No auth token available. Login test must be run first.")
        return False
    
    try:
        # Set up headers with auth token
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"
        }
        
        # Make DELETE request
        response = requests.delete(f"{API_BASE_URL}/menu/items/{item_id}", headers=headers)
        
        # Check if response is successful
        if response.status_code == 200:
            print("✅ Successfully deleted test menu item")
            return True
        else:
            print(f"❌ Failed to delete test menu item. Status code: {response.status_code}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to delete menu item endpoint: {e}")
        return False

def run_menu_details_tests():
    """Run all menu details tests"""
    print("\n🔍 Starting Jimmy's Tapas Bar Menu Details Tests")
    print("=" * 80)
    
    # Track test results
    results = {}
    
    # Test 1: Authentication
    auth_success, token = test_auth_login()
    results["auth_login"] = auth_success
    
    # Test 2: Get menu items with detailed analysis
    results["get_menu_items_detailed"] = test_get_menu_items_detailed()
    
    # Test 3: Create menu item with detailed information
    if auth_success:
        create_success, item_id = test_create_menu_item_with_details()
        results["create_menu_item_with_details"] = create_success
        
        # Clean up by deleting the test item
        if create_success and item_id:
            results["delete_test_menu_item"] = delete_test_menu_item(item_id)
    else:
        results["create_menu_item_with_details"] = False
        print("❌ Skipping menu item creation test due to failed login")
    
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
    run_menu_details_tests()