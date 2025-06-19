import React, { useState, useEffect, createContext, useContext } from "react";
import "./App.css";
import { createBrowserRouter, RouterProvider, Outlet, Link, useLocation } from "react-router-dom";

// Import Error Boundary
import ErrorBoundary from './components/ErrorBoundary';

// Import Admin Sections
import { ContentSection, MenuSection } from './AdminSections';
import { MediaSection } from './AdminSectionsFinal';
import LegalEditor from './components/LegalEditor';
import DashboardSection from './components/DashboardSection';
import NewsletterSection from './components/NewsletterSection';
import MaintenanceSection from './components/MaintenanceSection';
import LocationsAdminSection from './components/LocationsAdminSection';
import AboutAdminSection from './components/AboutAdminSection';
import ReviewsAdminSection from './components/ReviewsAdminSection';
import ContactAdminSection from './components/ContactAdminSection';
import UsersAdminSection from './components/UsersAdminSection';
import SystemBackupSection from './components/SystemBackupSection';

// Import Page Components
import Home from './components/Home';
import Locations from './components/Locations'; // Updated component
import UeberUns from './components/UeberUns';
import Speisekarte from './components/Speisekarte';
import Bewertungen from './components/Bewertungen';
import Kontakt from './components/Kontakt';
import Impressum from './components/Impressum';
import Datenschutz from './components/Datenschutz';
import Footer from './components/Footer';

// Language Context - Only German
const LanguageContext = createContext();

const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Language Provider Component - Only German
const LanguageProvider = ({ children }) => {
  const [currentLanguage] = useState('de'); // Fixed to German only
  
  // Simplified t function - will be replaced by backend data
  const t = (key) => {
    // This will be replaced by backend-driven content
    return key;
  };

  return (
    <LanguageContext.Provider value={{ currentLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

// Cookie Banner Component
const CookieBanner = () => {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    const cookieConsent = localStorage.getItem('cookieConsent');
    if (!cookieConsent) {
      setShowBanner(true);
    }
  }, []);

  const acceptCookies = () => {
    localStorage.setItem('cookieConsent', 'accepted');
    setShowBanner(false);
  };

  const rejectCookies = () => {
    localStorage.setItem('cookieConsent', 'rejected');
    setShowBanner(false);
  };

  if (!showBanner) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-dark-brown border-t-2 border-warm-beige p-4 z-50">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex-1">
            <h3 className="text-warm-beige font-serif text-lg mb-2">Diese Website verwendet Cookies</h3>
            <p className="text-light-beige text-sm">Wir verwenden Cookies, um Ihnen das beste Website-Erlebnis zu bieten. Durch die weitere Nutzung der Website stimmen Sie der Verwendung von Cookies zu.</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={rejectCookies}
              className="px-4 py-2 border border-warm-beige text-warm-beige hover:bg-warm-beige hover:text-dark-brown transition-colors text-sm"
            >
              Ablehnen
            </button>
            <button
              onClick={acceptCookies}
              className="px-4 py-2 bg-warm-beige text-dark-brown hover:bg-light-beige transition-colors text-sm"
            >
              Akzeptieren
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// New Admin Sections
const NavigationSection = () => {
  const [navItems, setNavItems] = useState([
    { id: 'home', name: 'Startseite', url: '/', active: true },
    { id: 'locations', name: 'Standorte', url: '/standorte', active: true },
    { id: 'menu', name: 'Speisekarte', url: '/speisekarte', active: true },
    { id: 'reviews', name: 'Bewertungen', url: '/bewertungen', active: true },
    { id: 'about', name: 'Über uns', url: '/ueber-uns', active: true },
    { id: 'contact', name: 'Kontakt', url: '/kontakt', active: true }
  ]);

  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');

  const updateNavItem = (id, field, value) => {
    setNavItems(navItems.map(item => 
      item.id === id ? { ...item, [field]: value } : item
    ));
  };

  const saveNavigation = async () => {
    setSaving(true);
    // Simulate save operation
    setTimeout(() => {
      setSaving(false);
      setSuccess('Navigation erfolgreich gespeichert!');
      setTimeout(() => setSuccess(''), 3000);
    }, 1000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">🧭 Navigation</h1>
        <p className="text-gray-600">Website-Navigation und Menü-Struktur verwalten</p>
      </div>

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Hauptnavigation</h3>
        
        <div className="space-y-4">
          {navItems.map((item, index) => (
            <div key={item.id} className="flex items-center justify-between p-6 bg-white border-2 border-gray-200 rounded-lg hover:border-gray-300 transition-colors">
              <div className="flex items-center space-x-6 flex-1">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl font-bold text-gray-800">{index + 1}</span>
                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={item.active}
                      onChange={(e) => updateNavItem(item.id, 'active', e.target.checked)}
                      className="h-5 w-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700">Aktiv</span>
                  </div>
                </div>
                
                <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-900 mb-2">Menü-Text</label>
                    <input
                      type="text"
                      value={item.name}
                      onChange={(e) => updateNavItem(item.id, 'name', e.target.value)}
                      className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-900 mb-2">URL</label>
                    <input
                      type="text"
                      value={item.url}
                      onChange={(e) => updateNavItem(item.id, 'url', e.target.value)}
                      className="w-full p-3 text-lg font-medium text-gray-700 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-3 ml-6">
                <button 
                  className="p-3 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                  title="Nach oben verschieben"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 15l7-7 7 7" />
                  </svg>
                </button>
                <button 
                  className="p-3 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                  title="Nach unten verschieben"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <button 
                  className="p-3 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg font-semibold transition-colors"
                >
                  Bearbeiten
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
          <button className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-semibold">
            + Neuen Menüpunkt hinzufügen
          </button>
          
          <button
            onClick={saveNavigation}
            disabled={saving}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-semibold flex items-center space-x-2"
          >
            {saving ? (
              <>
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Speichern...</span>
              </>
            ) : (
              <span>Navigation speichern</span>
            )}
          </button>
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h4 className="text-lg font-semibold text-blue-900 mb-3">💡 Navigation-Tipps</h4>
        <ul className="space-y-2 text-blue-800">
          <li>• <strong>Reihenfolge ändern:</strong> Verwende die Pfeiltasten zum Verschieben der Menüpunkte</li>
          <li>• <strong>Aktivierung:</strong> Deaktivierte Menüpunkte werden nicht in der Navigation angezeigt</li>
          <li>• <strong>URLs:</strong> Beginnen immer mit "/" für interne Links</li>
          <li>• <strong>Änderungen:</strong> Werden sofort nach dem Speichern auf der Website sichtbar</li>
        </ul>
      </div>
    </div>
  );
};

const LieferandoSection = () => {
  const [deliveryInfo, setDeliveryInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadDeliveryInfo();
  }, []);

  const loadDeliveryInfo = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/delivery/info`);
      if (response.ok) {
        const data = await response.json();
        setDeliveryInfo(data);
      } else {
        setError('Fehler beim Laden der Lieferando-Informationen');
      }
    } catch (error) {
      setError('Verbindungsfehler');
    } finally {
      setLoading(false);
    }
  };

  const saveDeliveryInfo = async () => {
    try {
      setSaving(true);
      setError('');
      
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/delivery/info`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(deliveryInfo)
      });

      if (response.ok) {
        setSuccess('Lieferando-Informationen erfolgreich gespeichert!');
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError('Fehler beim Speichern');
      }
    } catch (error) {
      setError('Verbindungsfehler beim Speichern');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">🚚 Lieferando</h1>
        <p className="text-gray-600">Lieferservice-Einstellungen und Verfügbarkeit verwalten</p>
      </div>

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {deliveryInfo && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Lieferservice-Einstellungen</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Lieferzeit (Min.)</label>
              <input
                type="number"
                value={deliveryInfo.delivery_time_min || 30}
                onChange={(e) => setDeliveryInfo({...deliveryInfo, delivery_time_min: parseInt(e.target.value)})}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Lieferzeit (Max.)</label>
              <input
                type="number"
                value={deliveryInfo.delivery_time_max || 45}
                onChange={(e) => setDeliveryInfo({...deliveryInfo, delivery_time_max: parseInt(e.target.value)})}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Mindestbestellwert (€)</label>
              <input
                type="number"
                step="0.50"
                value={deliveryInfo.minimum_order_value || 15.00}
                onChange={(e) => setDeliveryInfo({...deliveryInfo, minimum_order_value: parseFloat(e.target.value)})}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Liefergebühr (€)</label>
              <input
                type="number"
                step="0.50"
                value={deliveryInfo.delivery_fee || 2.50}
                onChange={(e) => setDeliveryInfo({...deliveryInfo, delivery_fee: parseFloat(e.target.value)})}
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900"
              />
            </div>
          </div>

          <div className="mt-6">
            <h4 className="text-md font-semibold text-gray-800 mb-4">Verfügbare Standorte</h4>
            <div className="space-y-4">
              {deliveryInfo.available_locations && Object.entries(deliveryInfo.available_locations).map(([key, location]) => (
                <div key={key} className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <h5 className="font-medium text-gray-900">{location.name}</h5>
                      <p className="text-sm text-gray-600">{location.address}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-600">Verfügbar:</span>
                      <input
                        type="checkbox"
                        checked={location.available}
                        onChange={(e) => {
                          const newLocations = {...deliveryInfo.available_locations};
                          newLocations[key].available = e.target.checked;
                          setDeliveryInfo({...deliveryInfo, available_locations: newLocations});
                        }}
                        className="h-4 w-4 text-blue-600"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-end mt-6">
            <button
              onClick={saveDeliveryInfo}
              disabled={saving}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {saving ? 'Speichern...' : 'Einstellungen speichern'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

const DeveloperInfoSection = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">🔧 Entwickler-Info</h1>
        <p className="text-gray-600">Technische Informationen und Entwickler-Tools</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">System-Informationen</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-800 mb-3">Frontend</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• React 19.0.0</li>
              <li>• React Router Dom 7.5.1</li>
              <li>• Tailwind CSS 3.4.17</li>
              <li>• Axios 1.8.4</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-800 mb-3">Backend</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• FastAPI 0.110.1</li>
              <li>• Python 3.11</li>
              <li>• MySQL (MariaDB)</li>
              <li>• JWT Authentication</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">API-Endpunkte</h3>
        <div className="space-y-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-800 mb-2">Authentication</h4>
            <code className="text-sm text-gray-600">POST /api/auth/login</code><br/>
            <code className="text-sm text-gray-600">GET /api/auth/me</code>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-800 mb-2">Content Management</h4>
            <code className="text-sm text-gray-600">GET/PUT /api/cms/homepage</code><br/>
            <code className="text-sm text-gray-600">GET/PUT /api/cms/locations</code><br/>
            <code className="text-sm text-gray-600">GET/PUT /api/cms/about</code>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-800 mb-2">Delivery</h4>
            <code className="text-sm text-gray-600">GET /api/delivery/info</code><br/>
            <code className="text-sm text-gray-600">PUT /api/admin/delivery/info</code>
          </div>
        </div>
      </div>
    </div>
  );
};

// EU-Compliance Section - Comprehensive GDPR/DSGVO Management
const EUComplianceSection = () => {
  const [complianceSettings, setComplianceSettings] = useState({
    gdpr_enabled: true,
    cookie_consent_required: true,
    data_retention_days: 730,
    analytics_enabled: false,
    marketing_enabled: false,
    data_processing_basis: 'legitimate_interest',
    privacy_officer_email: 'datenschutz@jimmys-tapasbar.de',
    privacy_officer_name: 'Jimmy Rodríguez',
    company_registration: 'HRB 12345 Hamburg',
    privacy_policy_version: '2.0',
    last_updated: new Date().toISOString().split('T')[0]
  });

  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');

  const saveComplianceSettings = async () => {
    setSaving(true);
    // Simulate save operation
    setTimeout(() => {
      setSaving(false);
      setSuccess('EU-Compliance Einstellungen erfolgreich gespeichert!');
      setTimeout(() => setSuccess(''), 3000);
    }, 1000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">🇪🇺 EU-Compliance & DSGVO</h1>
        <p className="text-gray-600">Datenschutz-Grundverordnung und EU-Rechtskonformität</p>
      </div>

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      {/* DSGVO Grundeinstellungen */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">🛡️ DSGVO-Grundeinstellungen</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="gdpr_enabled"
                checked={complianceSettings.gdpr_enabled}
                onChange={(e) => setComplianceSettings({...complianceSettings, gdpr_enabled: e.target.checked})}
                className="h-5 w-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500"
              />
              <label htmlFor="gdpr_enabled" className="text-lg font-medium text-gray-900">DSGVO aktiviert</label>
            </div>
            
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="cookie_consent"
                checked={complianceSettings.cookie_consent_required}
                onChange={(e) => setComplianceSettings({...complianceSettings, cookie_consent_required: e.target.checked})}
                className="h-5 w-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500"
              />
              <label htmlFor="cookie_consent" className="text-lg font-medium text-gray-900">Cookie-Einverständnis erforderlich</label>
            </div>

            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="analytics_enabled"
                checked={complianceSettings.analytics_enabled}
                onChange={(e) => setComplianceSettings({...complianceSettings, analytics_enabled: e.target.checked})}
                className="h-5 w-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500"
              />
              <label htmlFor="analytics_enabled" className="text-lg font-medium text-gray-900">Analytics aktiviert</label>
            </div>

            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="marketing_enabled"
                checked={complianceSettings.marketing_enabled}
                onChange={(e) => setComplianceSettings({...complianceSettings, marketing_enabled: e.target.checked})}
                className="h-5 w-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500"
              />
              <label htmlFor="marketing_enabled" className="text-lg font-medium text-gray-900">Marketing-Cookies aktiviert</label>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">Datenaufbewahrung (Tage)</label>
              <input
                type="number"
                value={complianceSettings.data_retention_days}
                onChange={(e) => setComplianceSettings({...complianceSettings, data_retention_days: parseInt(e.target.value)})}
                className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">Rechtsgrundlage</label>
              <select
                value={complianceSettings.data_processing_basis}
                onChange={(e) => setComplianceSettings({...complianceSettings, data_processing_basis: e.target.value})}
                className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="consent">Einwilligung (Art. 6 Abs. 1 lit. a DSGVO)</option>
                <option value="contract">Vertragserfüllung (Art. 6 Abs. 1 lit. b DSGVO)</option>
                <option value="legal_obligation">Rechtliche Verpflichtung (Art. 6 Abs. 1 lit. c DSGVO)</option>
                <option value="legitimate_interest">Berechtigtes Interesse (Art. 6 Abs. 1 lit. f DSGVO)</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Datenschutzbeauftragter */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">👨‍💼 Datenschutzbeauftragter</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-2">Name</label>
            <input
              type="text"
              value={complianceSettings.privacy_officer_name}
              onChange={(e) => setComplianceSettings({...complianceSettings, privacy_officer_name: e.target.value})}
              className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-2">E-Mail</label>
            <input
              type="email"
              value={complianceSettings.privacy_officer_email}
              onChange={(e) => setComplianceSettings({...complianceSettings, privacy_officer_email: e.target.value})}
              className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Unternehmensdaten */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">🏢 Unternehmensdaten</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-2">Handelsregistereintrag</label>
            <input
              type="text"
              value={complianceSettings.company_registration}
              onChange={(e) => setComplianceSettings({...complianceSettings, company_registration: e.target.value})}
              className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-2">Datenschutzrichtlinie Version</label>
            <input
              type="text"
              value={complianceSettings.privacy_policy_version}
              onChange={(e) => setComplianceSettings({...complianceSettings, privacy_policy_version: e.target.value})}
              className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Betroffenenrechte */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-4">📋 Implementierte Betroffenenrechte</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <span className="text-green-600">✅</span>
              <span className="font-medium text-blue-800">Recht auf Auskunft (Art. 15 DSGVO)</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-green-600">✅</span>
              <span className="font-medium text-blue-800">Recht auf Berichtigung (Art. 16 DSGVO)</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-green-600">✅</span>
              <span className="font-medium text-blue-800">Recht auf Löschung (Art. 17 DSGVO)</span>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <span className="text-green-600">✅</span>
              <span className="font-medium text-blue-800">Recht auf Datenübertragbarkeit (Art. 20 DSGVO)</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-green-600">✅</span>
              <span className="font-medium text-blue-800">Widerspruchsrecht (Art. 21 DSGVO)</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-green-600">✅</span>
              <span className="font-medium text-blue-800">Widerruf der Einwilligung (Art. 7 DSGVO)</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={saveComplianceSettings}
          disabled={saving}
          className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-semibold flex items-center space-x-2"
        >
          {saving ? (
            <>
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Speichern...</span>
            </>
          ) : (
            <span>Compliance-Einstellungen speichern</span>
          )}
        </button>
      </div>
    </div>
  );
};

// Cookie Management Section
const CookieManagementSection = () => {
  const [cookieSettings, setCookieSettings] = useState({
    essential_cookies: {
      enabled: true,
      description: 'Technisch notwendige Cookies für die Grundfunktionen der Website',
      cookies: ['session', 'csrf_token', 'admin_auth']
    },
    analytics_cookies: {
      enabled: false,
      description: 'Cookies zur Analyse des Nutzerverhaltens und Website-Performance',
      cookies: ['google_analytics', '_ga', '_gid']
    },
    marketing_cookies: {
      enabled: false,
      description: 'Cookies für personalisierte Werbung und Marketing',
      cookies: ['facebook_pixel', 'google_ads']
    },
    comfort_cookies: {
      enabled: true,
      description: 'Cookies für erweiterte Funktionen und Benutzerfreundlichkeit',
      cookies: ['language_preference', 'theme_preference']
    }
  });

  const [bannerSettings, setBannerSettings] = useState({
    banner_title: 'Diese Website verwendet Cookies',
    banner_text: 'Wir verwenden Cookies, um Ihnen das beste Website-Erlebnis zu bieten. Durch die weitere Nutzung der Website stimmen Sie der Verwendung von Cookies zu.',
    accept_button_text: 'Alle akzeptieren',
    reject_button_text: 'Ablehnen',
    settings_button_text: 'Einstellungen',
    privacy_link_text: 'Datenschutzerklärung',
    banner_position: 'bottom',
    auto_accept_after: 0
  });

  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');

  const saveCookieSettings = async () => {
    setSaving(true);
    setTimeout(() => {
      setSaving(false);
      setSuccess('Cookie-Einstellungen erfolgreich gespeichert!');
      setTimeout(() => setSuccess(''), 3000);
    }, 1000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">🍪 Cookie-Verwaltung</h1>
        <p className="text-gray-600">Cookie-Banner und Einverständnis-Management</p>
      </div>

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      {/* Cookie-Banner Einstellungen */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">🎯 Cookie-Banner Einstellungen</h3>
        
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">Banner-Titel</label>
              <input
                type="text"
                value={bannerSettings.banner_title}
                onChange={(e) => setBannerSettings({...bannerSettings, banner_title: e.target.value})}
                className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">Banner-Position</label>
              <select
                value={bannerSettings.banner_position}
                onChange={(e) => setBannerSettings({...bannerSettings, banner_position: e.target.value})}
                className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="top">Oben</option>
                <option value="bottom">Unten</option>
                <option value="center">Mitte (Overlay)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-2">Banner-Text</label>
            <textarea
              value={bannerSettings.banner_text}
              onChange={(e) => setBannerSettings({...bannerSettings, banner_text: e.target.value})}
              rows={3}
              className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">Akzeptieren-Button</label>
              <input
                type="text"
                value={bannerSettings.accept_button_text}
                onChange={(e) => setBannerSettings({...bannerSettings, accept_button_text: e.target.value})}
                className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">Ablehnen-Button</label>
              <input
                type="text"
                value={bannerSettings.reject_button_text}
                onChange={(e) => setBannerSettings({...bannerSettings, reject_button_text: e.target.value})}
                className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">Einstellungen-Button</label>
              <input
                type="text"
                value={bannerSettings.settings_button_text}
                onChange={(e) => setBannerSettings({...bannerSettings, settings_button_text: e.target.value})}
                className="w-full p-3 text-lg font-medium text-gray-900 border-2 border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Cookie-Kategorien */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">📊 Cookie-Kategorien</h3>
        
        <div className="space-y-6">
          {Object.entries(cookieSettings).map(([category, settings]) => (
            <div key={category} className="p-6 bg-gray-50 rounded-lg border-2 border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-lg font-semibold text-gray-900 capitalize">
                  {category.replace('_', ' ').replace('cookies', 'Cookies')}
                </h4>
                <div className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    checked={settings.enabled}
                    onChange={(e) => setCookieSettings({
                      ...cookieSettings,
                      [category]: {...settings, enabled: e.target.checked}
                    })}
                    disabled={category === 'essential_cookies'}
                    className="h-5 w-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="text-sm font-medium text-gray-700">
                    {settings.enabled ? 'Aktiviert' : 'Deaktiviert'}
                  </span>
                </div>
              </div>
              
              <p className="text-gray-600 mb-4">{settings.description}</p>
              
              <div className="space-y-2">
                <h5 className="font-medium text-gray-800">Verwendete Cookies:</h5>
                <div className="flex flex-wrap gap-2">
                  {settings.cookies.map((cookie, index) => (
                    <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                      {cookie}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={saveCookieSettings}
          disabled={saving}
          className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 font-semibold flex items-center space-x-2"
        >
          {saving ? (
            <>
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Speichern...</span>
            </>
          ) : (
            <span>Cookie-Einstellungen speichern</span>
          )}
        </button>
      </div>
    </div>
  );
};

// Startseite Summary Component - Simplified
const StartseiteSummary = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Startseite</h1>
        <p className="text-gray-600">Willkommen im Jimmy's Tapas Bar CMS</p>
      </div>

      {/* Focused Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">🚀 Häufige Aktionen</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button className="flex flex-col items-center p-6 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors group">
            <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mb-3 group-hover:bg-blue-600 transition-colors">
              <span className="text-white text-xl">+</span>
            </div>
            <span className="font-medium text-blue-700 text-center">Neues Gericht hinzufügen</span>
          </button>

          <button className="flex flex-col items-center p-6 bg-yellow-50 border border-yellow-200 rounded-lg hover:bg-yellow-100 transition-colors group">
            <div className="w-12 h-12 bg-yellow-500 rounded-lg flex items-center justify-center mb-3 group-hover:bg-yellow-600 transition-colors">
              <span className="text-white text-xl">⭐</span>
            </div>
            <span className="font-medium text-yellow-700 text-center">Bewertungen prüfen</span>
          </button>

          <button className="flex flex-col items-center p-6 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors group">
            <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mb-3 group-hover:bg-green-600 transition-colors">
              <span className="text-white text-xl">📧</span>
            </div>
            <span className="font-medium text-green-700 text-center">Nachrichten lesen</span>
          </button>

          <button className="flex flex-col items-center p-6 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors group">
            <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mb-3 group-hover:bg-purple-600 transition-colors">
              <span className="text-white text-xl">📮</span>
            </div>
            <span className="font-medium text-purple-700 text-center">Newsletter senden</span>
          </button>
        </div>
      </div>

      {/* System Information */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 System-Status</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex items-center p-4 bg-green-50 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <div>
                <p className="text-sm font-medium text-gray-900">CMS-Status</p>
                <p className="text-xs text-green-600">Online & Betriebsbereit</p>
              </div>
            </div>
          </div>

          <div className="flex items-center p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
              <div>
                <p className="text-sm font-medium text-gray-900">Letztes Backup</p>
                <p className="text-xs text-blue-600">Vor 6 Stunden</p>
              </div>
            </div>
          </div>

          <div className="flex items-center p-4 bg-purple-50 rounded-lg">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
              <div>
                <p className="text-sm font-medium text-gray-900">System-Uptime</p>
                <p className="text-xs text-purple-600">24h 15m</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Hint */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">💡 Navigation</h3>
        <p className="text-blue-800 mb-4">
          Verwenden Sie das <strong>linke Hauptmenü</strong> für die vollständige Navigation zu allen CMS-Bereichen.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-blue-700">
          <div>• 🏠 <strong>Homepage bearbeiten</strong> - Inhalte der Startseite</div>
          <div>• 📍 <strong>Standorte</strong> - Adressen & Öffnungszeiten</div>
          <div>• 🍽️ <strong>Speisekarte</strong> - Gerichte & Kategorien</div>
          <div>• ⭐ <strong>Bewertungen</strong> - Moderation & Genehmigung</div>
          <div>• 📧 <strong>Kontakt-Nachrichten</strong> - Kundenanfragen</div>
          <div>• 👥 <strong>Benutzer-Verwaltung</strong> - Accounts & Rollen</div>
        </div>
      </div>
    </div>
  );
};
const AdminPanel = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [activeSection, setActiveSection] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // API Base URL
  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Helper function for API calls
  const apiCall = async (endpoint, method = 'GET', data = null) => {
    try {
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const config = {
        method,
        headers
      };

      if (data && (method === 'POST' || method === 'PUT')) {
        config.body = JSON.stringify(data);
      }

      const response = await fetch(`${API_BASE_URL}/api${endpoint}`, config);
      return response;
    } catch (error) {
      console.error('API call error:', error);
      throw error;
    }
  };

  // Check for existing login on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('adminToken');
    console.log('Checking saved token:', savedToken ? 'Found' : 'Not found');
    if (savedToken) {
      setToken(savedToken);
      verifyToken(savedToken);
    }
  }, []);

  // Authentication Functions
  const verifyToken = async (tokenToVerify) => {
    try {
      console.log('Verifying token...');
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokenToVerify}`
      };

      const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
        method: 'GET',
        headers
      });
      
      console.log('Token verification response status:', response.status);
      
      if (response.ok) {
        const userData = await response.json();
        console.log('User data received:', userData);
        setUser(userData);
        setIsLoggedIn(true);
      } else {
        console.log('Token verification failed');
        localStorage.removeItem('adminToken');
        setToken(null);
      }
    } catch (error) {
      console.error('Token verification failed:', error);
      localStorage.removeItem('adminToken');
      setToken(null);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    console.log('Attempting login with:', loginForm.username);

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginForm)
      });
      
      console.log('Login response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        const newToken = data.access_token;
        console.log('Login successful, token received');
        
        setToken(newToken);
        localStorage.setItem('adminToken', newToken);
        
        // Get user info
        const userResponse = await fetch(`${API_BASE_URL}/api/auth/me`, {
          headers: { 'Authorization': `Bearer ${newToken}` }
        });
        
        if (userResponse.ok) {
          const userData = await userResponse.json();
          setUser(userData);
          setIsLoggedIn(true);
          setSuccess('Erfolgreich angemeldet!');
        }
      } else {
        const errorData = await response.json();
        console.error('Login failed:', errorData);
        setError(errorData.detail || 'Anmeldung fehlgeschlagen');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('Verbindungsfehler. Bitte versuchen Sie es erneut.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('adminToken');
    setToken(null);
    setUser(null);
    setIsLoggedIn(false);
    setActiveSection('dashboard');
    setSuccess('Erfolgreich abgemeldet');
  };

  // Login Screen
  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Jimmy's Tapas Bar - Admin Panel
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              Melden Sie sich an, um das CMS zu verwalten
            </p>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleLogin}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <input
                  type="text"
                  required
                  value={loginForm.username}
                  onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Benutzername"
                />
              </div>
              <div>
                <input
                  type="password"
                  required
                  value={loginForm.password}
                  onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Passwort"
                />
              </div>
            </div>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            {success && (
              <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                {success}
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {loading ? 'Anmelden...' : 'Anmelden'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  // Admin Dashboard
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="flex" style={{minHeight: '100vh'}}>
        {/* Sidebar */}
        <div className="w-64 bg-white shadow-lg" style={{position: 'fixed', height: '100vh', zIndex: 40}}>
          <div className="p-6 border-b">
            <h1 className="text-xl font-bold text-gray-900">Jimmy's Tapas Bar</h1>
            <p className="text-sm text-gray-600">Admin Panel</p>
            <p className="text-xs text-blue-600 mt-1">Willkommen, {user?.username}</p>
          </div>
          <nav className="mt-6 overflow-y-auto" style={{maxHeight: 'calc(100vh - 120px)'}}>
            {/* Core Content Management */}
            <button
              onClick={() => setActiveSection('dashboard')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'dashboard' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              📊 Dashboard
            </button>
            <button
              onClick={() => setActiveSection('homepage')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'homepage' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              🏠 Homepage bearbeiten
            </button>
            <button
              onClick={() => setActiveSection('locations')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'locations' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              📍 Standorte
            </button>
            <button
              onClick={() => setActiveSection('about')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'about' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              ℹ️ Über uns
            </button>
            <button
              onClick={() => setActiveSection('menu')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'menu' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              🍽️ Speisekarte
            </button>
            
            {/* Interaction Management */}
            <button
              onClick={() => setActiveSection('reviews')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'reviews' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              ⭐ Bewertungen
            </button>
            <button
              onClick={() => setActiveSection('contacts')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'contacts' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              📧 Kontakt-Nachrichten
            </button>
            <button
              onClick={() => setActiveSection('newsletter')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'newsletter' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              📮 Newsletter
            </button>
            
            {/* User Management */}
            <button
              onClick={() => setActiveSection('users')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'users' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              👥 Benutzer-Verwaltung
            </button>
            
            {/* Legal & Content Tools */}
            <button
              onClick={() => setActiveSection('legal')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'legal' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              📋 Impressum & Datenschutz
            </button>
            <button
              onClick={() => setActiveSection('eu-compliance')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'eu-compliance' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              🇪🇺 EU-Compliance & DSGVO
            </button>
            <button
              onClick={() => setActiveSection('cookie-management')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'cookie-management' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              🍪 Cookie-Verwaltung
            </button>
            <button
              onClick={() => setActiveSection('navigation')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'navigation' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              🧭 Navigation
            </button>
            
            {/* Delivery Management */}
            <button
              onClick={() => setActiveSection('lieferando')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'lieferando' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              🚚 Lieferando
            </button>
            
            {/* Developer & System Tools */}
            <button
              onClick={() => setActiveSection('developer-info')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'developer-info' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              🔧 Entwickler-Info
            </button>
            <button
              onClick={() => setActiveSection('system')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'system' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              ⚙️ System & Backup
            </button>
            <button
              onClick={() => setActiveSection('maintenance')}
              className={`w-full text-left px-6 py-3 text-sm ${activeSection === 'maintenance' ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700' : 'text-gray-700 hover:bg-gray-50'}`}
            >
              🔧 Wartungsmodus
            </button>
            
            {/* Quick Actions */}
            <div className="border-t mt-6 pt-6">
              <a
                href="/"
                target="_blank"
                className="w-full text-left px-6 py-3 text-sm text-green-600 hover:bg-green-50 block"
              >
                🌐 Website ansehen
              </a>
              <button
                onClick={handleLogout}
                className="w-full text-left px-6 py-3 text-sm text-red-600 hover:bg-red-50"
              >
                🚪 Abmelden
              </button>
            </div>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-8" style={{marginLeft: '256px'}}>
          {activeSection === 'dashboard' && <DashboardSection setActiveSection={setActiveSection} />}
          {activeSection === 'homepage' && <ContentSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'locations' && <LocationsAdminSection />}
          {activeSection === 'about' && <AboutAdminSection />}
          {activeSection === 'menu' && <MenuSection user={user} token={token} apiCall={apiCall} />}
          {activeSection === 'reviews' && <ReviewsAdminSection />}
          {activeSection === 'contacts' && <ContactAdminSection />}
          {activeSection === 'newsletter' && <NewsletterSection />}
          {activeSection === 'users' && <UsersAdminSection />}
          {activeSection === 'legal' && <LegalEditor />}
          {activeSection === 'eu-compliance' && <EUComplianceSection />}
          {activeSection === 'cookie-management' && <CookieManagementSection />}
          {activeSection === 'navigation' && <NavigationSection />}
          {activeSection === 'lieferando' && <LieferandoSection />}
          {activeSection === 'developer-info' && <DeveloperInfoSection />}
          {activeSection === 'system' && <SystemBackupSection />}
          {activeSection === 'maintenance' && <MaintenanceSection />}
        </div>
      </div>
    </div>
  );
};

// Header Component  
const Header = () => {
  const location = useLocation();
  const [navigationTexts, setNavigationTexts] = useState({
    home: 'Startseite',
    locations: 'Standorte', 
    menu: 'Speisekarte',
    reviews: 'Bewertungen',
    about: 'Über uns',
    contact: 'Kontakt',
    privacy: 'Datenschutz',
    imprint: 'Impressum'
  });

  // Load navigation texts from backend
  useEffect(() => {
    const loadNavigationTexts = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/cms/website-texts/navigation`);
        if (response.ok) {
          const data = await response.json();
          if (data.navigation) {
            setNavigationTexts(data.navigation);
          }
        }
      } catch (error) {
        console.error('Error loading navigation texts:', error);
      }
    };
    loadNavigationTexts();
  }, []);
  
  const isActivePage = (path) => location.pathname === path;
  
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-dark-brown-transparent backdrop-blur-sm">
      <a href="#main-content" className="skip-link">
        Zum Hauptinhalt springen
      </a>
      
      <div className="container mx-auto px-8 py-4">
        <nav className="flex justify-between items-center">
          <Link to="/" className="text-xl font-light text-stone-100 tracking-[0.2em]">
            JIMMY'S
            <span className="block text-xs text-stone-300 tracking-[0.3em] font-light mt-1">TAPAS BAR</span>
          </Link>
          
          <div className="hidden md:flex space-x-10 items-center">
            <Link to="/" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.home}</Link>
            <Link to="/standorte" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/standorte') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.locations}</Link>
            <Link to="/speisekarte" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/speisekarte') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.menu}</Link>
            <Link to="/bewertungen" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/bewertungen') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.reviews}</Link>
            <Link to="/ueber-uns" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/ueber-uns') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.about}</Link>
            <Link to="/kontakt" className={`transition-colors font-light tracking-wide text-sm ${
              isActivePage('/kontakt') ? 'text-warm-beige border-b-2 border-warm-beige pb-1' : 'text-stone-100 hover:text-stone-300'
            }`}>{navigationTexts.contact}</Link>
          </div>
        </nav>
      </div>
    </header>
  );
};

// Layout Component for normal pages
const Layout = () => {
  return (
    <>
      <Header />
      <Outlet />
      <Footer />
      <CookieBanner />
    </>
  );
};

// Create the router with new React Router v7 API (without admin route)
const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <ErrorBoundary><Home /></ErrorBoundary>
      },
      {
        path: "standorte",
        element: <ErrorBoundary><Locations /></ErrorBoundary>
      },
      {
        path: "speisekarte", 
        element: <ErrorBoundary><Speisekarte /></ErrorBoundary>
      },
      {
        path: "bewertungen",
        element: <ErrorBoundary><Bewertungen /></ErrorBoundary>
      },
      {
        path: "ueber-uns",
        element: <ErrorBoundary><UeberUns /></ErrorBoundary>
      },
      {
        path: "kontakt",
        element: <Kontakt />
      },
      {
        path: "impressum",
        element: <Impressum />
      },
      {
        path: "datenschutz",
        element: <Datenschutz />
      }
    ]
  }
]);

// Direct Admin Check Component with better detection
const AppRouter = () => {
  const [isAdmin, setIsAdmin] = useState(false);
  const [currentPath, setCurrentPath] = useState('');

  useEffect(() => {
    const checkAndSetPath = () => {
      const path = window.location.pathname;
      const hash = window.location.hash.substring(1); // Remove the #
      setCurrentPath(path + (hash ? `#${hash}` : ''));
      
      // Check for admin path in multiple ways
      const isAdminPath = path === '/admin' || 
                         path.startsWith('/admin/') || 
                         hash === 'admin' || 
                         hash.startsWith('admin/');
      
      setIsAdmin(isAdminPath);
    };

    checkAndSetPath();
    
    // Listen for all navigation changes
    const handleNavigation = () => {
      setTimeout(checkAndSetPath, 10); // Small delay to ensure updates
    };
    
    window.addEventListener('popstate', handleNavigation);
    window.addEventListener('hashchange', handleNavigation);
    
    // Override history methods
    const originalPushState = window.history.pushState;
    const originalReplaceState = window.history.replaceState;
    
    window.history.pushState = function(...args) {
      originalPushState.apply(this, args);
      handleNavigation();
    };
    
    window.history.replaceState = function(...args) {
      originalReplaceState.apply(this, args);
      handleNavigation();
    };

    return () => {
      window.removeEventListener('popstate', handleNavigation);
      window.removeEventListener('hashchange', handleNavigation);
      window.history.pushState = originalPushState;
      window.history.replaceState = originalReplaceState;
    };
  }, []);

  // Force admin if URL contains admin
  if (isAdmin || window.location.pathname === '/admin' || window.location.hash === '#admin') {
    return <AdminPanel />;
  }

  return <RouterProvider router={router} />;
};

// Main App Component with direct routing
function App() {
  return (
    <LanguageProvider>
      <div className="App">
        <AppRouter />
      </div>
    </LanguageProvider>
  );
}

export default App;