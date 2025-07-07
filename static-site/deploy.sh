#!/bin/bash

# Jimmy's Tapas Bar - Static Website Deployment Script
# This script helps with local testing and deployment preparation

echo "🌶️ Jimmy's Tapas Bar - Static Website Deployment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "dist/index.html" ]; then
    echo "❌ Error: Please run this script from the static-site directory"
    echo "   The dist/index.html file was not found."
    exit 1
fi

echo "✅ Found dist/index.html - correct directory"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to start local server
start_local_server() {
    echo ""
    echo "🚀 Starting local development server..."
    
    cd dist
    
    # Try npx http-server first (most reliable)
    if command_exists npx; then
        echo "   Using: npx http-server"
        echo "   URL: http://localhost:8080"
        echo "   Press Ctrl+C to stop"
        echo ""
        npx http-server -p 8080 -o -c-1
    # Try Python 3
    elif command_exists python3; then
        echo "   Using: Python 3 http.server"
        echo "   URL: http://localhost:8080"
        echo "   Press Ctrl+C to stop"
        echo ""
        python3 -m http.server 8080
    # Try Python 2
    elif command_exists python; then
        echo "   Using: Python 2 SimpleHTTPServer"
        echo "   URL: http://localhost:8080"
        echo "   Press Ctrl+C to stop"
        echo ""
        python -m SimpleHTTPServer 8080
    # Try PHP
    elif command_exists php; then
        echo "   Using: PHP built-in server"
        echo "   URL: http://localhost:8080"
        echo "   Press Ctrl+C to stop"
        echo ""
        php -S localhost:8080
    else
        echo "❌ No suitable HTTP server found!"
        echo "   Please install one of the following:"
        echo "   - Node.js (for npx http-server)"
        echo "   - Python (for http.server)"
        echo "   - PHP (for built-in server)"
        exit 1
    fi
}

# Function to validate menu.ini
validate_menu() {
    echo ""
    echo "🔍 Validating menu.ini file..."
    
    if [ ! -f "dist/config/menu.ini" ]; then
        echo "❌ menu.ini file not found!"
        return 1
    fi
    
    # Check for required sections
    if ! grep -q "\\[SETTINGS\\]" dist/config/menu.ini; then
        echo "❌ Missing [SETTINGS] section in menu.ini"
        return 1
    fi
    
    if ! grep -q "\\[CATEGORIES\\]" dist/config/menu.ini; then
        echo "❌ Missing [CATEGORIES] section in menu.ini"
        return 1
    fi
    
    # Count menu items
    item_count=$(grep -c "^\\[.*_[0-9]\\+\\]" dist/config/menu.ini)
    echo "✅ Found $item_count menu items"
    
    # Check for required settings
    if grep -q "restaurant_name.*=" dist/config/menu.ini; then
        echo "✅ Restaurant name configured"
    else
        echo "⚠️  Restaurant name not configured"
    fi
    
    if grep -q "currency_symbol.*=" dist/config/menu.ini; then
        echo "✅ Currency symbol configured"
    else
        echo "⚠️  Currency symbol not configured"
    fi
    
    echo "✅ menu.ini validation completed"
}

# Function to create deployment package
create_package() {
    echo ""
    echo "📦 Creating deployment package..."
    
    # Create timestamp
    timestamp=$(date +"%Y%m%d_%H%M%S")
    package_name="jimmys-tapas-static_${timestamp}.zip"
    
    # Create ZIP file
    if command_exists zip; then
        cd dist
        zip -r "../${package_name}" . -x "*.DS_Store" "*.git*" "node_modules/*"
        cd ..
        echo "✅ Created package: ${package_name}"
        echo "   Ready for upload to static hosting service"
    else
        echo "❌ ZIP command not found"
        echo "   Please install zip utility or manually copy dist/ folder"
    fi
}

# Function to show deployment instructions
show_deployment_info() {
    echo ""
    echo "🌐 Deployment Instructions"
    echo "========================="
    echo ""
    echo "Static Hosting Services:"
    echo ""
    echo "1. Netlify:"
    echo "   - Go to https://netlify.com"
    echo "   - Drag & drop the dist/ folder"
    echo "   - Get instant URL"
    echo ""
    echo "2. Vercel:"
    echo "   - Install: npm i -g vercel"
    echo "   - Run: vercel --cwd dist"
    echo ""
    echo "3. GitHub Pages:"
    echo "   - Push dist/ contents to repository"
    echo "   - Enable Pages in repository settings"
    echo ""
    echo "4. Traditional Hosting:"
    echo "   - Upload all files from dist/ via FTP"
    echo "   - Set index.html as default page"
    echo ""
    echo "📝 Configuration Files:"
    echo "   - Menu: dist/config/menu.ini"
    echo "   - Styles: dist/css/styles.css"
    echo "   - Main Logic: dist/js/main.js"
}

# Function to show menu editing help
show_menu_help() {
    echo ""
    echo "🍽️ Menu Editing Guide"
    echo "===================="
    echo ""
    echo "File: dist/config/menu.ini"
    echo ""
    echo "Add new dish:"
    echo "-------------"
    echo "[categoria_numero]"
    echo "name = Dish Name"
    echo "description = Short description"
    echo "detailed_description = Detailed description for modal"
    echo "price = 15.90"
    echo "category = inicio"
    echo "allergens = Gluten, Eggs"
    echo "origin = Valencia"
    echo "preparation = Grilled"
    echo "ingredients = Ingredient list"
    echo "vegetarian = true"
    echo "vegan = false"
    echo "image = https://images.unsplash.com/photo-..."
    echo ""
    echo "Add new category:"
    echo "----------------"
    echo "1. In [CATEGORIES] section:"
    echo "   new_category = Category Display Name"
    echo ""
    echo "2. Use in dishes:"
    echo "   category = new_category"
    echo ""
    echo "💡 Tip: Always test locally after changes!"
}

# Main menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo ""
    echo "1) Start local development server"
    echo "2) Validate menu.ini file"
    echo "3) Create deployment package"
    echo "4) Show deployment instructions"
    echo "5) Show menu editing guide"
    echo "6) Exit"
    echo ""
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            validate_menu
            start_local_server
            ;;
        2)
            validate_menu
            ;;
        3)
            validate_menu
            create_package
            ;;
        4)
            show_deployment_info
            ;;
        5)
            show_menu_help
            ;;
        6)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please try again."
            show_menu
            ;;
    esac
}

# Run main menu
show_menu