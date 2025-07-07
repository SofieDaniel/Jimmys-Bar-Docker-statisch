/**
 * Jimmy's Tapas Bar - Speisekarte JavaScript
 * Handles menu loading, filtering, and modal functionality
 */

let currentCategory = 'all';
let menuItems = [];

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeSpeisekarte();
});

/**
 * Initialize the Speisekarte page
 */
async function initializeSpeisekarte() {
    // Show loading screen
    if (window.JimmysApp) {
        window.JimmysApp.showLoadingScreen();
    }
    
    try {
        // Load menu data
        await loadMenuDataForSpeisekarte();
        
        // Initialize components
        initializeCategories();
        initializeMenuGrid();
        initializeModal();
        initializeFilters();
        
        // Hide loading screen
        if (window.JimmysApp) {
            window.JimmysApp.hideLoadingScreen();
        }
        
        console.log('Speisekarte initialized successfully');
    } catch (error) {
        console.error('Error initializing Speisekarte:', error);
        
        // Hide loading screen even on error
        if (window.JimmysApp) {
            window.JimmysApp.hideLoadingScreen();
        }
    }
}

/**
 * Load menu data specifically for Speisekarte
 */
async function loadMenuDataForSpeisekarte() {
    try {
        // Try to use global menu data first
        if (window.JimmysApp && window.JimmysApp.menuData && Object.keys(window.JimmysApp.menuData).length > 0) {
            processMenuData(window.JimmysApp.menuData);
            return;
        }
        
        // Load menu data directly
        const response = await fetch('../config/menu.ini');
        const iniText = await response.text();
        const menuData = parseINIForSpeisekarte(iniText);
        
        processMenuData(menuData);
        
        console.log('Menu data loaded for Speisekarte:', menuData);
    } catch (error) {
        console.error('Error loading menu data:', error);
        
        // Use fallback data
        const fallbackData = getFallbackMenuDataForSpeisekarte();
        processMenuData(fallbackData);
    }
}

/**
 * Parse INI data for Speisekarte
 */
function parseINIForSpeisekarte(iniText) {
    const result = {
        settings: {},
        categories: {},
        items: []
    };
    
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
                result.items.push({
                    id: currentSection,
                    section: currentSection
                });
            }
            continue;
        }
        
        // Key-value pairs
        const equalIndex = line.indexOf('=');
        if (equalIndex > -1) {
            const key = line.slice(0, equalIndex).trim();
            const value = line.slice(equalIndex + 1).trim();
            
            if (currentSection === 'CATEGORIES') {
                result.categories[key] = value;
            } else if (currentSection === 'SETTINGS') {
                result.settings[key] = value;
            } else if (currentSection) {
                // Add to current item
                const currentItem = result.items[result.items.length - 1];
                if (currentItem && currentItem.section === currentSection) {
                    // Convert boolean strings
                    if (value === 'true') {
                        currentItem[key] = true;
                    } else if (value === 'false') {
                        currentItem[key] = false;
                    } else {
                        currentItem[key] = value;
                    }
                }
            }
        }
    }
    
    return result;
}

/**
 * Process menu data into usable format
 */
function processMenuData(data) {
    // Store categories
    window.menuCategories = data.categories || {};
    window.menuSettings = data.settings || {};
    
    // Process menu items
    if (data.items) {
        menuItems = data.items.filter(item => item.name && item.category);
    } else {
        // Handle old format (fallback)
        menuItems = [];
        Object.keys(data).forEach(key => {
            if (key !== 'settings' && key !== 'categories' && data[key].name) {
                menuItems.push({
                    id: key,
                    ...data[key]
                });
            }
        });
    }
    
    console.log('Processed menu items:', menuItems);
}

/**
 * Get fallback menu data
 */
function getFallbackMenuDataForSpeisekarte() {
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
            paellas: "Paellas",
            postres: "Postres / Nachspeisen",
            bebidas: "Bebidas / Getränke"
        },
        items: [
            {
                id: "inicio_1",
                name: "Gambas al Ajillo",
                description: "Klassische Knoblauchgarnelen in Olivenöl",
                detailed_description: "Frische Garnelen, scharf angebraten in bestem Olivenöl mit viel Knoblauch und Petersilie",
                price: "12.90",
                category: "inicio",
                allergens: "Krustentiere",
                origin: "Andalusien",
                image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b",
                vegetarian: false,
                preparation: "In Knoblauchöl",
                ingredients: "Garnelen, Knoblauch, Petersilie, Olivenöl, Chili"
            },
            {
                id: "inicio_2",
                name: "Patatas Bravas",
                description: "Würzige Kartoffeln mit traditioneller Bravas-Sauce",
                detailed_description: "Knusprig gebratene Kartoffelwürfel mit hausgemachter Bravas-Sauce und Aioli",
                price: "8.90",
                category: "inicio",
                allergens: "Eier (Aioli)",
                origin: "Madrid",
                image: "https://images.unsplash.com/photo-1565599837634-134bc3aadce8",
                vegetarian: true,
                preparation: "Frittiert",
                ingredients: "Kartoffeln, Tomaten, Paprika, Knoblauch, Olivenöl"
            },
            {
                id: "paellas_1",
                name: "Paella Valenciana",
                description: "Original spanische Paella mit Safran, Huhn und Gemüse",
                detailed_description: "Die klassische Paella aus Valencia mit Bomba-Reis, echtem Safran, Huhn, grünen Bohnen und Tomaten",
                price: "18.90",
                category: "paellas",
                allergens: "",
                origin: "Valencia",
                image: "https://images.unsplash.com/photo-1534080564583-6be75777b70a",
                vegetarian: false,
                preparation: "In der Paellera",
                ingredients: "Bomba-Reis, Safran, Huhn, grüne Bohnen, Tomaten, Olivenöl"
            }
        ]
    };
}

/**
 * Initialize category filter buttons
 */
function initializeCategories() {
    const categoryButtons = document.getElementById('categoryButtons');
    if (!categoryButtons) return;
    
    categoryButtons.innerHTML = '';
    
    // Add category buttons
    Object.entries(window.menuCategories || {}).forEach(([key, name]) => {
        const button = document.createElement('button');
        button.className = 'category-btn';
        button.textContent = name;
        button.dataset.category = key;
        button.onclick = () => filterByCategory(key);
        
        categoryButtons.appendChild(button);
    });
}

/**
 * Initialize menu grid
 */
function initializeMenuGrid() {
    const menuGrid = document.getElementById('menuGrid');
    if (!menuGrid) return;
    
    menuGrid.innerHTML = '';
    
    menuItems.forEach(item => {
        const menuItemElement = createMenuItemElement(item);
        menuGrid.appendChild(menuItemElement);
    });
}

/**
 * Create menu item HTML element
 */
function createMenuItemElement(item) {
    const menuItem = document.createElement('div');
    menuItem.className = 'menu-item';
    menuItem.dataset.category = item.category;
    
    const currencySymbol = window.menuSettings?.currency_symbol || '€';
    const vegetarianBadge = item.vegetarian ? '<span class="menu-item-vegetarian">🌿 Vegetarisch</span>' : '';
    const allergenInfo = item.allergens ? `<span class="menu-item-allergens">Allergene: ${item.allergens}</span>` : '';
    
    menuItem.innerHTML = `
        <img src="${item.image || 'https://images.unsplash.com/photo-1544025162-d76694265947'}" 
             alt="${item.name}" 
             class="menu-item-image">
        <div class="menu-item-content">
            <div class="menu-item-header">
                <h3 class="menu-item-title">${item.name}</h3>
                <span class="menu-item-price">${item.price}${currencySymbol}</span>
            </div>
            <p class="menu-item-description">${item.description}</p>
            <div class="menu-item-meta">
                <span class="menu-item-origin">${item.origin || ''}</span>
                ${vegetarianBadge}
                ${allergenInfo}
            </div>
        </div>
    `;
    
    // Add click handler for modal
    menuItem.onclick = () => showMenuItemModal(item);
    
    return menuItem;
}

/**
 * Filter menu items by category
 */
function filterByCategory(category) {
    currentCategory = category;
    
    // Update active button
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.category === category || (category === 'all' && !btn.dataset.category)) {
            btn.classList.add('active');
        }
    });
    
    // Filter menu items
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        if (category === 'all' || item.dataset.category === category) {
            item.classList.remove('hidden');
            item.classList.add('show');
        } else {
            item.classList.add('hidden');
            item.classList.remove('show');
        }
    });
}

/**
 * Initialize modal functionality
 */
function initializeModal() {
    const modal = document.getElementById('menuModal');
    const modalClose = document.getElementById('modalClose');
    const modalOverlay = modal?.querySelector('.modal-overlay');
    
    // Close modal handlers
    if (modalClose) {
        modalClose.onclick = hideMenuItemModal;
    }
    
    if (modalOverlay) {
        modalOverlay.onclick = hideMenuItemModal;
    }
    
    // Close on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            hideMenuItemModal();
        }
    });
}

/**
 * Show menu item modal
 */
function showMenuItemModal(item) {
    const modal = document.getElementById('menuModal');
    const modalBody = document.getElementById('modalBody');
    
    if (!modal || !modalBody) return;
    
    const currencySymbol = window.menuSettings?.currency_symbol || '€';
    
    modalBody.innerHTML = `
        <img src="${item.image || 'https://images.unsplash.com/photo-1544025162-d76694265947'}" 
             alt="${item.name}" 
             class="modal-image">
        
        <h2 class="modal-title">${item.name}</h2>
        <div class="modal-price">${item.price}${currencySymbol}</div>
        
        <p class="modal-description">
            ${item.detailed_description || item.description}
        </p>
        
        <div class="modal-details">
            <h4>Details</h4>
            
            ${item.origin ? `
                <div class="detail-row">
                    <span class="detail-label">Herkunft:</span>
                    <span class="detail-value">${item.origin}</span>
                </div>
            ` : ''}
            
            ${item.preparation ? `
                <div class="detail-row">
                    <span class="detail-label">Zubereitung:</span>
                    <span class="detail-value">${item.preparation}</span>
                </div>
            ` : ''}
            
            ${item.ingredients ? `
                <div class="detail-row">
                    <span class="detail-label">Zutaten:</span>
                    <span class="detail-value">${item.ingredients}</span>
                </div>
            ` : ''}
            
            ${item.allergens ? `
                <div class="detail-row">
                    <span class="detail-label">Allergene:</span>
                    <span class="detail-value">${item.allergens}</span>
                </div>
            ` : ''}
            
            <div class="detail-row">
                <span class="detail-label">Vegetarisch:</span>
                <span class="detail-value">${item.vegetarian ? 'Ja 🌿' : 'Nein'}</span>
            </div>
        </div>
    `;
    
    modal.classList.add('show');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

/**
 * Hide menu item modal
 */
function hideMenuItemModal() {
    const modal = document.getElementById('menuModal');
    
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

/**
 * Initialize filter functionality
 */
function initializeFilters() {
    // Set up "All" button
    const allButton = document.querySelector('.category-btn[data-category="all"]');
    if (allButton) {
        allButton.onclick = () => filterByCategory('all');
    }
    
    // Initial filter (show all)
    filterByCategory('all');
}

/**
 * Search functionality (if needed in the future)
 */
function searchMenuItems(query) {
    const searchTerm = query.toLowerCase();
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        const title = item.querySelector('.menu-item-title').textContent.toLowerCase();
        const description = item.querySelector('.menu-item-description').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            item.classList.remove('hidden');
            item.classList.add('show');
        } else {
            item.classList.add('hidden');
            item.classList.remove('show');
        }
    });
}

// Export functions for global use
window.SpeisekarteApp = {
    filterByCategory,
    searchMenuItems,
    showMenuItemModal,
    hideMenuItemModal,
    menuItems
};

console.log('🍽️ Speisekarte JavaScript loaded successfully');