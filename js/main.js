/**
 * Jimmy's Tapas Bar - Static Website JavaScript
 * Handles dynamic menu loading, navigation, cookies, and interactions
 */

// Global variables
let menuData = {};
let cookieSettings = {
    essential: true,
    analytics: false,
    marketing: false,
    comfort: false
};

// DOM ready state
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
});

/**
 * Initialize the website
 */
function initializeWebsite() {
    // Show loading screen
    showLoadingScreen();
    
    // Initialize components
    initializeNavigation();
    initializeCookies();
    initializeScrollToTop();
    
    // Load menu data and initialize page-specific content
    loadMenuData().then(() => {
        initializeHomePage();
        initializeContactForm();
        hideLoadingScreen();
    }).catch(error => {
        console.error('Error loading menu data:', error);
        hideLoadingScreen();
    });
}

/**
 * Navigation functionality
 */
function initializeNavigation() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            
            // Animate hamburger lines
            const lines = mobileMenuBtn.querySelectorAll('.hamburger-line');
            lines.forEach((line, index) => {
                if (mobileMenu.classList.contains('active')) {
                    if (index === 0) line.style.transform = 'rotate(45deg) translate(6px, 6px)';
                    if (index === 1) line.style.opacity = '0';
                    if (index === 2) line.style.transform = 'rotate(-45deg) translate(6px, -6px)';
                } else {
                    line.style.transform = '';
                    line.style.opacity = '';
                }
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenuBtn.contains(event.target) && !mobileMenu.contains(event.target)) {
                mobileMenu.classList.remove('active');
                
                // Reset hamburger lines
                const lines = mobileMenuBtn.querySelectorAll('.hamburger-line');
                lines.forEach(line => {
                    line.style.transform = '';
                    line.style.opacity = '';
                });
            }
        });
    }
}

/**
 * Cookie management
 */
function initializeCookies() {
    const cookieBanner = document.getElementById('cookieBanner');
    const cookieAccept = document.getElementById('cookieAccept');
    const cookieReject = document.getElementById('cookieReject');
    const cookieSettings = document.getElementById('cookieSettings');
    
    // Check if cookies are already accepted
    const cookieConsent = localStorage.getItem('cookieConsent');
    
    if (!cookieConsent) {
        setTimeout(() => {
            if (cookieBanner) {
                cookieBanner.classList.add('show');
            }
        }, 2000);
    }
    
    if (cookieAccept) {
        cookieAccept.addEventListener('click', function() {
            acceptAllCookies();
        });
    }
    
    if (cookieReject) {
        cookieReject.addEventListener('click', function() {
            rejectAllCookies();
        });
    }
    
    if (cookieSettings) {
        cookieSettings.addEventListener('click', function() {
            // For now, just accept all (in a real implementation, you'd show a settings modal)
            acceptAllCookies();
        });
    }
}

function acceptAllCookies() {
    cookieSettings.essential = true;
    cookieSettings.analytics = true;
    cookieSettings.marketing = true;
    cookieSettings.comfort = true;
    
    localStorage.setItem('cookieConsent', 'accepted_all');
    localStorage.setItem('cookiePreferences', JSON.stringify(cookieSettings));
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    
    hideCookieBanner();
}

function rejectAllCookies() {
    cookieSettings.essential = true;
    cookieSettings.analytics = false;
    cookieSettings.marketing = false;
    cookieSettings.comfort = false;
    
    localStorage.setItem('cookieConsent', 'rejected');
    localStorage.setItem('cookiePreferences', JSON.stringify(cookieSettings));
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    
    hideCookieBanner();
}

function hideCookieBanner() {
    const cookieBanner = document.getElementById('cookieBanner');
    if (cookieBanner) {
        cookieBanner.classList.remove('show');
    }
}

/**
 * Scroll to top functionality
 */
function initializeScrollToTop() {
    const scrollToTop = document.getElementById('scrollToTop');
    
    if (scrollToTop) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollToTop.classList.add('visible');
            } else {
                scrollToTop.classList.remove('visible');
            }
        });
        
        // Scroll to top when clicked
        scrollToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * Load menu data from INI file
 */
async function loadMenuData() {
    try {
        // Detect if we're in a subdirectory
        const isSubDirectory = window.location.pathname.includes('/pages/');
        const menuPath = isSubDirectory ? '../config/menu.ini' : 'config/menu.ini';
        
        const response = await fetch(menuPath);
        const iniText = await response.text();
        menuData = parseINI(iniText);
        
        console.log('Menu data loaded successfully:', menuData);
        return menuData;
    } catch (error) {
        console.error('Error loading menu.ini:', error);
        
        // Fallback data if INI file can't be loaded
        menuData = getFallbackMenuData();
        return menuData;
    }
}

/**
 * Parse INI file content
 */
function parseINI(iniText) {
    const result = {};
    const categories = {};
    let currentSection = null;
    
    const lines = iniText.split('\n');
    
    for (let line of lines) {
        line = line.trim();
        
        // Skip comments and empty lines
        if (line.startsWith('#') || line.startsWith(';') || line === '') {
            continue;
        }
        
        // Section headers
        if (line.startsWith('[') && line.endsWith(']')) {
            currentSection = line.slice(1, -1);
            if (currentSection !== 'SETTINGS' && currentSection !== 'CATEGORIES') {
                result[currentSection] = {};
            }
            continue;
        }
        
        // Key-value pairs
        const equalIndex = line.indexOf('=');
        if (equalIndex > -1) {
            const key = line.slice(0, equalIndex).trim();
            const value = line.slice(equalIndex + 1).trim();
            
            if (currentSection === 'CATEGORIES') {
                categories[key] = value;
            } else if (currentSection === 'SETTINGS') {
                result.settings = result.settings || {};
                result.settings[key] = value;
            } else if (currentSection) {
                // Convert boolean strings
                if (value === 'true') {
                    result[currentSection][key] = true;
                } else if (value === 'false') {
                    result[currentSection][key] = false;
                } else {
                    result[currentSection][key] = value;
                }
            }
        }
    }
    
    result.categories = categories;
    return result;
}

/**
 * Get fallback menu data if INI file fails to load
 */
function getFallbackMenuData() {
    return {
        settings: {
            restaurant_name: "Jimmy's Tapas Bar",
            currency: "EUR",
            currency_symbol: "€"
        },
        categories: {
            inicio: "Inicio / Vorspeisen",
            carnes: "Carnes / Fleischgerichte",
            pescados: "Pescados / Fischgerichte",
            paellas: "Paellas"
        },
        inicio_1: {
            name: "Gambas al Ajillo",
            description: "Klassische Knoblauchgarnelen in Olivenöl",
            detailed_description: "Frische Garnelen, scharf angebraten in bestem Olivenöl mit viel Knoblauch und Petersilie",
            price: "12.90",
            category: "inicio",
            allergens: "Krustentiere",
            origin: "Andalusien",
            image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b",
            vegetarian: false
        },
        inicio_2: {
            name: "Patatas Bravas",
            description: "Würzige Kartoffeln mit traditioneller Bravas-Sauce",
            detailed_description: "Knusprig gebratene Kartoffelwürfel mit hausgemachter Bravas-Sauce und Aioli",
            price: "8.90",
            category: "inicio",
            allergens: "Eier (Aioli)",
            origin: "Madrid",
            image: "https://images.unsplash.com/photo-1565599837634-134bc3aadce8",
            vegetarian: true
        },
        paellas_1: {
            name: "Paella Valenciana",
            description: "Original spanische Paella mit Safran, Huhn und Gemüse",
            detailed_description: "Die klassische Paella aus Valencia mit Bomba-Reis, echtem Safran, Huhn, grünen Bohnen und Tomaten",
            price: "18.90",
            category: "paellas",
            allergens: "",
            origin: "Valencia",
            image: "https://images.unsplash.com/photo-1534080564583-6be75777b70a",
            vegetarian: false
        },
        paellas_2: {
            name: "Paella de Mariscos",
            description: "Meeresfrüchte-Paella mit Garnelen, Muscheln und Tintenfisch",
            detailed_description: "Luxuriöse Paella mit frischen Meeresfrüchten aus der Ostsee und dem Mittelmeer",
            price: "22.90",
            category: "paellas",
            allergens: "Krustentiere, Weichtiere",
            origin: "Valencia",
            image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b",
            vegetarian: false
        }
    };
}

/**
 * Initialize homepage content
 */
function initializeHomePage() {
    // Only run on homepage
    if (!document.getElementById('specialtiesGrid')) {
        return;
    }
    
    populateSpecialties();
}

/**
 * Populate specialties section with menu data
 */
function populateSpecialties() {
    const specialtiesGrid = document.getElementById('specialtiesGrid');
    if (!specialtiesGrid) return;
    
    // Get featured items from menu data
    const featuredItems = getFeaturedMenuItems();
    
    specialtiesGrid.innerHTML = '';
    
    featuredItems.forEach(item => {
        const card = createSpecialtyCard(item);
        specialtiesGrid.appendChild(card);
    });
}

/**
 * Get featured menu items for homepage
 */
function getFeaturedMenuItems() {
    const featured = [];
    
    // Get menu items (excluding settings and categories)
    Object.keys(menuData).forEach(key => {
        if (key !== 'settings' && key !== 'categories' && menuData[key].name) {
            featured.push(menuData[key]);
        }
    });
    
    // Return first 4 items for homepage display
    return featured.slice(0, 4);
}

/**
 * Create specialty card HTML element
 */
function createSpecialtyCard(item) {
    const card = document.createElement('div');
    card.className = 'specialty-card';
    card.onclick = () => {
        // Navigate to menu page (in a real implementation)
        window.location.href = 'pages/speisekarte.html';
    };
    
    const currencySymbol = menuData.settings?.currency_symbol || '€';
    
    card.innerHTML = `
        <img src="${item.image || 'https://images.unsplash.com/photo-1544025162-d76694265947'}" 
             alt="${item.name}" 
             class="specialty-image">
        <div class="specialty-content">
            <h3 class="specialty-title">${item.name}</h3>
            <p class="specialty-description">${item.description}</p>
            <p class="specialty-price">${item.price}${currencySymbol}</p>
        </div>
    `;
    
    return card;
}

/**
 * Loading screen functions
 */
function showLoadingScreen() {
    const loadingScreen = document.getElementById('loadingScreen');
    if (loadingScreen) {
        loadingScreen.style.display = 'flex';
    }
}

function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loadingScreen');
    if (loadingScreen) {
        loadingScreen.style.display = 'none';
    }
}

/**
 * Utility functions
 */

// Format price with currency
function formatPrice(price) {
    const currencySymbol = menuData.settings?.currency_symbol || '€';
    return `${price}${currencySymbol}`;
}

// Get category display name
function getCategoryName(categoryKey) {
    return menuData.categories?.[categoryKey] || categoryKey;
}

// Filter menu items by category
function getMenuItemsByCategory(category) {
    const items = [];
    
    Object.keys(menuData).forEach(key => {
        if (key !== 'settings' && key !== 'categories' && menuData[key].category === category) {
            items.push({
                key: key,
                ...menuData[key]
            });
        }
    });
    
    return items;
}

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Export functions for use in other pages
window.JimmysApp = {
    menuData,
    cookieSettings,
    loadMenuData,
    parseINI,
    formatPrice,
    getCategoryName,
    getMenuItemsByCategory,
    scrollToElement,
    showLoadingScreen,
    hideLoadingScreen
};

// Console welcome message
console.log(`
🌶️ Jimmy's Tapas Bar - Static Website
🚀 Website loaded successfully
📄 Menu data: ${Object.keys(menuData).length} items loaded
🍪 Cookie consent: ${localStorage.getItem('cookieConsent') || 'not set'}
`);