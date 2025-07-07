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
 * Initialize menu grid - Original Design
 */
function initializeMenuGrid() {
    const menuList = document.getElementById('menuList');
    if (!menuList) return;
    
    menuList.innerHTML = '';
    
    // Group items by category
    const categories = {};
    menuItems.forEach(item => {
        if (!categories[item.category]) {
            categories[item.category] = [];
        }
        categories[item.category].push(item);
    });
    
    // Create category sections
    Object.entries(categories).forEach(([categoryKey, items]) => {
        const categorySection = document.createElement('div');
        categorySection.className = 'menu-category-section';
        categorySection.dataset.category = categoryKey;
        
        const categoryTitle = document.createElement('h2');
        categoryTitle.className = 'menu-category-title';
        categoryTitle.textContent = getCategoryName(categoryKey);
        categorySection.appendChild(categoryTitle);
        
        items.forEach(item => {
            const menuItemElement = createMenuItemOriginal(item);
            categorySection.appendChild(menuItemElement);
        });
        
        menuList.appendChild(categorySection);
    });
}

/**
 * Create menu item HTML element - Original Design
 */
function createMenuItemOriginal(item) {
    const menuItem = document.createElement('div');
    menuItem.className = 'menu-item-original';
    menuItem.dataset.category = item.category;
    
    const currencySymbol = window.menuSettings?.currency_symbol || '€';
    const vegetarianIcon = item.vegetarian ? '🌿' : '';
    
    menuItem.innerHTML = `
        <div class="menu-item-header-original">
            <h3 class="menu-item-title-original">
                ${vegetarianIcon} ${item.name}
            </h3>
            <span class="menu-item-price-original">${item.price}${currencySymbol}</span>
        </div>
        <p class="menu-item-description-original">${item.description}</p>
        <div class="menu-item-meta-original">
            ${item.origin ? `<span class="menu-item-tag tag-origin">${item.origin}</span>` : ''}
            ${item.category ? `<span class="menu-item-tag tag-category">${getCategoryName(item.category)}</span>` : ''}
            ${item.vegetarian ? `<span class="menu-item-tag tag-vegetarian">Vegetarisch</span>` : ''}
        </div>
    `;
    
    // Add hover handler for detail panel
    menuItem.addEventListener('mouseenter', () => showMenuItemDetail(item));
    menuItem.addEventListener('mouseleave', () => hideMenuItemDetail());
    menuItem.addEventListener('click', () => {
        // Remove active from all items
        document.querySelectorAll('.menu-item-original').forEach(el => el.classList.remove('active'));
        // Add active to clicked item
        menuItem.classList.add('active');
        showMenuItemDetail(item);
    });
    
    return menuItem;
}

/**
 * Show menu item detail in right panel - Original Design
 */
function showMenuItemDetail(item) {
    const detailPanel = document.getElementById('menuDetailPanel');
    if (!detailPanel) return;
    
    const currencySymbol = window.menuSettings?.currency_symbol || '€';
    const vegetarianIcon = item.vegetarian ? '🌿' : '';
    
    detailPanel.innerHTML = `
        <div class="menu-detail-content">
            <img src="${item.image || 'https://images.unsplash.com/photo-1544025162-d76694265947'}" 
                 alt="${item.name}" 
                 class="detail-image">
            
            <h2 class="detail-title">${vegetarianIcon} ${item.name}</h2>
            <div class="detail-price">${item.price}${currencySymbol}</div>
            
            <p class="detail-description">
                ${item.detailed_description || item.description}
            </p>
            
            <div class="detail-info-section">
                <h3 class="detail-info-title">🍽️ Detaillierte Gericht-Informationen</h3>
                <div class="detail-info-grid">
                    ${item.origin ? `
                        <div class="detail-info-row">
                            <span class="detail-info-label">🌍 Herkunft:</span>
                            <span class="detail-info-value">${item.origin}</span>
                        </div>
                    ` : ''}
                    
                    ${item.preparation ? `
                        <div class="detail-info-row">
                            <span class="detail-info-label">👨‍🍳 Zubereitung:</span>
                            <span class="detail-info-value">${item.preparation}</span>
                        </div>
                    ` : ''}
                    
                    ${item.ingredients ? `
                        <div class="detail-info-row">
                            <span class="detail-info-label">🥘 Zutaten:</span>
                            <span class="detail-info-value">${item.ingredients}</span>
                        </div>
                    ` : ''}
                    
                    <div class="detail-info-row">
                        <span class="detail-info-label">🌱 Vegetarisch:</span>
                        <span class="detail-info-value">${item.vegetarian ? 'Ja' : 'Nein'}</span>
                    </div>
                </div>
            </div>
            
            ${item.allergens ? `
                <div class="detail-info-section">
                    <h3 class="detail-info-title">⚠️ Allergene & Zusatzstoffe</h3>
                    <div class="detail-info-grid">
                        <div class="detail-info-row">
                            <span class="detail-info-label">🚨 Allergene:</span>
                            <span class="detail-info-value">${item.allergens}</span>
                        </div>
                    </div>
                </div>
            ` : ''}
            
            <div class="detail-tags">
                ${item.vegetarian ? '<span class="menu-item-tag tag-vegetarian">🌿 Vegetarisch</span>' : ''}
                ${item.origin ? `<span class="menu-item-tag tag-origin">📍 ${item.origin}</span>` : ''}
                ${item.category ? `<span class="menu-item-tag tag-category">${getCategoryName(item.category)}</span>` : ''}
            </div>
        </div>
    `;
}

/**
 * Hide menu item detail panel
 */
function hideMenuItemDetail() {
    // Don't hide immediately, allow clicking
    setTimeout(() => {
        const detailPanel = document.getElementById('menuDetailPanel');
        if (detailPanel && !detailPanel.matches(':hover')) {
            detailPanel.innerHTML = `
                <div class="detail-placeholder">
                    <div class="detail-icon">🍽️</div>
                    <p>Bewegen Sie die Maus über ein Gericht<br>um detaillierte Beschreibungen,<br>Zutaten, Herkunft, Zubereitung<br>und Allergie-Informationen zu erhalten</p>
                </div>
            `;
        }
    }, 300);
}

/**
 * Filter menu items by category - Original Design
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
    
    // Filter category sections
    const categorySections = document.querySelectorAll('.menu-category-section');
    categorySections.forEach(section => {
        if (category === 'all' || section.dataset.category === category) {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });
    
    // Reset detail panel
    hideMenuItemDetail();
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