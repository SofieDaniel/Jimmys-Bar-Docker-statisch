import React, { useState, useEffect } from 'react';

const Speisekarte = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('Alle Kategorien');
  const [hoveredItem, setHoveredItem] = useState(null);

  // Load menu items from backend
  useEffect(() => {
    const loadMenuItems = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/menu/items`);
        if (response.ok) {
          const data = await response.json();
          setMenuItems(data);
        }
      } catch (error) {
        console.error('Error loading menu items:', error);
      } finally {
        setLoading(false);
      }
    };
    loadMenuItems();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-brown flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-warm-beige"></div>
      </div>
    );
  }

  // Get unique categories with proper mapping
  const categoryMapping = {
    'Inicio': 'Inicio',
    'Salat': 'Salat', 
    'Kleiner Salat': 'Kleiner Salat',
    'Tapas Warme': 'Tapas Warme',
    'Tapa Paella': 'Tapa Paella',
    'Tapas Vegetar': 'Tapas Vegetar',
    'Tapas de Carne': 'Tapas de Carne',
    'Kroketten': 'Kroketten',
    'Pasta': 'Pasta',
    'Pizza': 'Pizza',
    'Snacks': 'Snacks',
    'Dessert': 'Dessert',
    'Helados': 'Helados'
  };

  const allCategories = ['Alle Kategorien', ...Object.keys(categoryMapping)];
  const filteredItems = selectedCategory === 'Alle Kategorien' 
    ? menuItems 
    : menuItems.filter(item => item.category === selectedCategory);

  // Group items by category for display
  const groupedItems = filteredItems.reduce((acc, item) => {
    const category = item.category;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(item);
    return acc;
  }, {});

  // Get allergy icons
  const getAllergyIcons = (item) => {
    const icons = [];
    if (item.vegan) icons.push('🌱');
    if (item.vegetarian && !item.vegan) icons.push('🌿');
    if (item.glutenfree) icons.push('🌾');
    return icons;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Beautiful Header Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-orange-500 via-red-500 to-yellow-500">
        <div className="absolute inset-0 bg-black bg-opacity-40"></div>
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-orange-400/20 via-transparent to-yellow-400/20"></div>
          <div className="absolute -top-10 -left-10 w-40 h-40 bg-yellow-400/30 rounded-full blur-xl"></div>
          <div className="absolute -bottom-10 -right-10 w-60 h-60 bg-orange-400/30 rounded-full blur-xl"></div>
          <div className="absolute top-1/2 left-1/4 w-32 h-32 bg-red-400/20 rounded-full blur-xl"></div>
        </div>
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4 text-center">
            <div className="max-w-4xl mx-auto">
              <h1 className="text-6xl md:text-7xl font-serif text-white mb-6 tracking-wide drop-shadow-lg">
                Speisekarte
              </h1>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                <p className="text-xl md:text-2xl text-white font-light leading-relaxed">
                  Authentische spanische Küche - Entdecken Sie unsere Gerichte
                </p>
                <div className="flex justify-center items-center gap-4 mt-4 text-white/90">
                  <span className="flex items-center gap-2 text-sm">
                    <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                    Detaillierte Allergie-Informationen
                  </span>
                  <span className="flex items-center gap-2 text-sm">
                    <span className="w-2 h-2 bg-blue-400 rounded-full"></span>
                    Hover für Details
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Category Filter Buttons */}
      <div className="container mx-auto px-4 mb-8 bg-gradient-to-r from-slate-800 to-slate-700 py-6 rounded-xl mx-4">
        <div className="flex flex-wrap justify-center gap-3 max-w-6xl mx-auto">
          {allCategories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-6 py-3 rounded-full border-2 transition-all duration-300 transform hover:scale-105 ${
                selectedCategory === category
                  ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white border-orange-500 shadow-lg'
                  : 'bg-white/10 text-gray-200 border-gray-300 hover:bg-gradient-to-r hover:from-orange-400 hover:to-red-400 hover:text-white hover:border-orange-400'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 pb-16">
        <div className="flex gap-8 max-w-7xl mx-auto">
          {/* Left Side - Menu Items List */}
          <div className="flex-1">
            {Object.entries(groupedItems).map(([category, items]) => (
              <div key={category} className="mb-8">
                {selectedCategory === 'Alle Kategorien' && (
                  <div className="flex items-center gap-4 mb-6">
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-warm-beige/50 to-transparent"></div>
                    <h2 className="text-2xl font-serif text-warm-beige px-4 bg-dark-brown">
                      {category}
                    </h2>
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-warm-beige/50 to-transparent"></div>
                  </div>
                )}
                
                <div className="space-y-2">
                  {items.map((item, index) => (
                    <div
                      key={item.id}
                      className={`group relative overflow-hidden rounded-lg transition-all duration-300 ${
                        hoveredItem?.id === item.id 
                          ? 'bg-gradient-to-r from-warm-beige/15 via-orange-500/10 to-warm-beige/15 border-l-4 border-warm-beige shadow-lg transform scale-[1.02]' 
                          : index % 2 === 0 
                            ? 'bg-gradient-to-r from-medium-brown/30 to-dark-brown/30 hover:from-warm-beige/10 hover:to-orange-500/10 border-l-4 border-transparent hover:border-warm-beige/50'
                            : 'bg-gradient-to-r from-dark-brown/30 to-medium-brown/30 hover:from-orange-500/10 hover:to-warm-beige/10 border-l-4 border-transparent hover:border-orange-500/50'
                      } cursor-pointer`}
                      onMouseEnter={() => setHoveredItem(item)}
                      onMouseLeave={() => setHoveredItem(null)}
                    >
                      <div className="p-5">
                        <div className="flex justify-between items-start">
                          <div className="flex-1 pr-4">
                            <div className="flex items-center gap-3 mb-2">
                              <h3 className="text-lg font-medium text-warm-beige group-hover:text-white transition-colors">
                                {item.name}
                              </h3>
                              <div className="flex gap-1">
                                {getAllergyIcons(item).map((icon, index) => (
                                  <span key={index} className="text-sm bg-warm-beige/20 px-1 rounded">{icon}</span>
                                ))}
                              </div>
                            </div>
                            <p className="text-light-beige text-sm leading-relaxed group-hover:text-gray-200 transition-colors">
                              {item.description.length > 85 
                                ? `${item.description.substring(0, 85)}...` 
                                : item.description}
                            </p>
                            <div className="flex items-center gap-2 mt-2">
                              <span className={`text-xs px-2 py-1 rounded-full ${
                                index % 3 === 0 ? 'bg-orange-500/20 text-orange-300'
                                : index % 3 === 1 ? 'bg-warm-beige/20 text-warm-beige'
                                : 'bg-yellow-500/20 text-yellow-300'
                              }`}>
                                {item.category}
                              </span>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className={`px-3 py-2 rounded-lg ${
                              hoveredItem?.id === item.id 
                                ? 'bg-warm-beige text-dark-brown shadow-lg'
                                : 'bg-dark-brown/50 border border-warm-beige/30'
                            } transition-all duration-300`}>
                              <span className="text-lg font-bold text-warm-beige">
                                {item.price}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      {/* Hover indicator */}
                      <div className={`absolute bottom-0 left-0 h-1 bg-gradient-to-r from-warm-beige to-orange-500 transition-all duration-300 ${
                        hoveredItem?.id === item.id ? 'w-full' : 'w-0'
                      }`}></div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Right Side - Hover Details (No Images) */}
          <div className="w-96 sticky top-24 h-fit">
            {hoveredItem ? (
              <div className="bg-gradient-to-br from-medium-brown to-dark-brown border-2 border-warm-beige/40 rounded-xl p-6 shadow-2xl">
                {/* Header with decorative elements */}
                <div className="border-b border-warm-beige/30 pb-4 mb-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-2xl font-serif text-warm-beige">
                      {hoveredItem.name}
                    </h3>
                    <div className="text-right">
                      <div className="bg-warm-beige text-dark-brown px-3 py-1 rounded-full">
                        <span className="text-xl font-bold">
                          {hoveredItem.price}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-2 flex items-center gap-2">
                    <span className="bg-orange-500/20 text-orange-300 px-2 py-1 rounded text-xs font-medium">
                      {hoveredItem.category}
                    </span>
                    <div className="flex gap-1">
                      {getAllergyIcons(hoveredItem).map((icon, index) => (
                        <span key={index} className="text-lg">{icon}</span>
                      ))}
                    </div>
                  </div>
                </div>
                
                {/* Description */}
                <div className="bg-dark-brown/50 rounded-lg p-4 mb-4 border border-warm-beige/20">
                  <p className="text-light-beige leading-relaxed">
                    {hoveredItem.description}
                  </p>
                </div>
                
                {/* Allergy Information */}
                <div className="bg-warm-beige/5 rounded-lg p-4 border border-warm-beige/20">
                  <h4 className="text-sm font-semibold text-warm-beige mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 bg-warm-beige rounded-full"></span>
                    Allergie-Informationen
                  </h4>
                  <div className="grid grid-cols-3 gap-3">
                    <div className={`text-center p-2 rounded ${hoveredItem.vegan ? 'bg-green-500/20 border border-green-500/30' : 'bg-gray-500/10 border border-gray-500/20'}`}>
                      <div className="text-lg mb-1">🌱</div>
                      <div className={`text-xs ${hoveredItem.vegan ? 'text-green-300' : 'text-gray-400'}`}>
                        Vegan
                      </div>
                    </div>
                    <div className={`text-center p-2 rounded ${hoveredItem.vegetarian ? 'bg-green-500/20 border border-green-500/30' : 'bg-gray-500/10 border border-gray-500/20'}`}>
                      <div className="text-lg mb-1">🌿</div>
                      <div className={`text-xs ${hoveredItem.vegetarian ? 'text-green-300' : 'text-gray-400'}`}>
                        Vegetarisch
                      </div>
                    </div>
                    <div className={`text-center p-2 rounded ${hoveredItem.glutenfree ? 'bg-green-500/20 border border-green-500/30' : 'bg-gray-500/10 border border-gray-500/20'}`}>
                      <div className="text-lg mb-1">🌾</div>
                      <div className={`text-xs ${hoveredItem.glutenfree ? 'text-green-300' : 'text-gray-400'}`}>
                        Glutenfrei
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-gradient-to-br from-warm-beige/10 to-orange-500/10 border-2 border-dashed border-warm-beige/30 rounded-xl p-8 text-center">
                <div className="text-warm-beige/60 mb-4">
                  <div className="w-16 h-16 mx-auto bg-warm-beige/10 rounded-full flex items-center justify-center">
                    <span className="text-2xl">🍽️</span>
                  </div>
                </div>
                <h3 className="text-warm-beige font-medium mb-2">Gericht-Details</h3>
                <p className="text-warm-beige/70 text-sm">
                  Bewegen Sie die Maus über ein Gericht<br/>
                  um Details und Allergie-Informationen zu sehen
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Allergy Legend */}
        <div className="max-w-7xl mx-auto mt-12 pt-8 border-t border-warm-beige/20">
          <h3 className="text-lg font-serif text-warm-beige mb-4 text-center">
            Allergie-Legende
          </h3>
          <div className="flex justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <span>🌱</span>
              <span className="text-light-beige">Vegan</span>
            </div>
            <div className="flex items-center gap-2">
              <span>🌿</span>
              <span className="text-light-beige">Vegetarisch</span>
            </div>
            <div className="flex items-center gap-2">
              <span>🌾</span>
              <span className="text-light-beige">Glutenfrei</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Speisekarte;
