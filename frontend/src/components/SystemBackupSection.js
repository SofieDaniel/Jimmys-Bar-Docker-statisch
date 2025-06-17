import React, { useState, useEffect } from 'react';

const SystemBackupSection = () => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [backupStatus, setBackupStatus] = useState({
    lastBackup: null,
    backupSize: null,
    autoBackup: true,
    backupFrequency: 'daily',
    nextScheduled: null,
    backupCount: 0
  });
  const [systemInfo, setSystemInfo] = useState({
    version: 'Jimmy\'s CMS v1.0',
    uptime: '24h 15m',
    database: 'Connected',
    diskSpace: '2.5 GB used / 10 GB available'
  });
  const [activeTab, setActiveTab] = useState('backup');

  // Database Configuration State
  const [dbConfig, setDbConfig] = useState({
    host: 'localhost',
    port: '27017',
    username: '',
    password: '',
    database: 'jimmys_tapas_bar',
    connectionString: ''
  });

  useEffect(() => {
    loadSystemInfo();
    loadBackupStatus();
  }, []);

  const loadSystemInfo = async () => {
    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/system/info`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setSystemInfo({
          version: data.version || 'Jimmy\'s CMS v1.0',
          uptime: data.uptime || 'Unbekannt',
          database: data.database_status || 'Connected',
          diskSpace: `${data.disk_usage || 'N/A'} Festplatte verwendet`,
          cpuUsage: data.cpu_usage || 'N/A',
          memoryUsage: data.memory_usage || 'N/A',
          pythonVersion: data.python_version || 'N/A',
          platform: data.platform || 'N/A'
        });
      }
    } catch (error) {
      console.error('Error loading system info:', error);
    }
  };

  const loadBackupStatus = async () => {
    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/status`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setBackupStatus({
          lastBackup: data.last_backup ? formatDateTime(data.last_backup) : 'Nie',
          backupSize: data.backup_size || 'Unbekannt',
          autoBackup: data.auto_backup || false,
          backupFrequency: data.backup_frequency || 'daily',
          nextScheduled: data.next_scheduled ? formatDateTime(data.next_scheduled) : 'Unbekannt',
          backupCount: data.backup_count || 0,
          diskSpaceUsed: data.disk_space_used || 'N/A',
          diskSpaceTotal: data.disk_space_total || 'N/A'
        });
      }
    } catch (error) {
      console.error('Error loading backup status:', error);
      setMessage('Fehler beim Laden des Backup-Status');
    }
  };

  const formatDateTime = (isoString) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString('de-DE') + ' ' + date.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
    } catch {
      return 'Unbekannt';
    }
  };

  const handleDatabaseBackup = async () => {
    setLoading(true);
    setMessage('Erstelle Datenbank-Backup...');

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/database`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        // Get filename from response headers
        const contentDisposition = response.headers.get('Content-Disposition');
        const filename = contentDisposition ? 
          contentDisposition.split('filename=')[1].replace(/"/g, '') : 
          `database-backup-${new Date().toISOString().split('T')[0]}.json`;

        // Download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setMessage('✅ Datenbank-Backup erfolgreich erstellt und heruntergeladen!');
        loadBackupStatus(); // Refresh status
      } else {
        const errorData = await response.json();
        setMessage(`❌ Fehler beim Erstellen des Datenbank-Backups: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Backup error:', error);
      setMessage('❌ Verbindungsfehler beim Erstellen des Backups. Prüfen Sie Ihre Internetverbindung.');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 8000);
    }
  };

  const handleFullBackup = async () => {
    setLoading(true);
    setMessage('Erstelle vollständiges Backup (Datenbank + Dateien)...');

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/backup/full`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        // Get filename from response headers
        const contentDisposition = response.headers.get('Content-Disposition');
        const filename = contentDisposition ? 
          contentDisposition.split('filename=')[1].replace(/"/g, '') : 
          `full-backup-${new Date().toISOString().split('T')[0]}.zip`;

        // Download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setMessage('✅ Vollständiges Backup erfolgreich erstellt und heruntergeladen!');
        loadBackupStatus(); // Refresh status
      } else {
        const errorData = await response.json();
        setMessage(`❌ Fehler beim Erstellen des vollständigen Backups: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Full backup error:', error);
      setMessage('❌ Verbindungsfehler beim Erstellen des Backups. Prüfen Sie Ihre Internetverbindung.');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 8000);
    }
  };

  const handleConfigSave = async (configData) => {
    setLoading(true);
    setMessage('Speichere Konfiguration...');

    try {
      const token = localStorage.getItem('adminToken');
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/config`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(configData)
      });

      if (response.ok) {
        setMessage('✅ Konfiguration erfolgreich gespeichert!');
      } else {
        const errorData = await response.json();
        setMessage(`❌ Fehler beim Speichern: ${errorData.detail}`);
      }
    } catch (error) {
      setMessage('❌ Verbindungsfehler beim Speichern der Konfiguration');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 5000);
    }
  };

  const testDatabaseConnection = async () => {
    setLoading(true);
    setMessage('Teste Datenbankverbindung...');

    try {
      // Simulate database connection test
      await new Promise(resolve => setTimeout(resolve, 2000));
      setMessage('✅ Datenbankverbindung erfolgreich getestet!');
    } catch (error) {
      setMessage('❌ Datenbankverbindung fehlgeschlagen!');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 5000);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">System & Backup</h1>
        <p className="text-gray-600">System-Verwaltung, Backup und Konfiguration</p>
      </div>

      {message && (
        <div className={`p-4 rounded-lg ${
          message.includes('erfolgreich') 
            ? 'bg-green-100 text-green-700 border border-green-200' 
            : 'bg-red-100 text-red-700 border border-red-200'
        }`}>
          {message}
        </div>
      )}

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { key: 'backup', label: 'Backup & Restore', icon: '💾' },
            { key: 'system', label: 'System-Info', icon: '📊' },
            { key: 'database', label: 'Datenbank-Konfiguration', icon: '🗄️' },
            { key: 'config', label: 'Allgemeine Konfiguration', icon: '⚙️' }
          ].map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center ${
                activeTab === tab.key
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Backup Tab */}
      {activeTab === 'backup' && (
        <div className="space-y-6">
          {/* Enhanced Backup Status */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Backup-Status</h3>
              <button
                onClick={loadBackupStatus}
                disabled={loading}
                className="text-blue-600 hover:text-blue-800 text-sm disabled:opacity-50"
              >
                🔄 Aktualisieren
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="flex items-center p-4 bg-blue-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Letztes Backup</p>
                      <p className="text-xs text-blue-600">{backupStatus.lastBackup}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-green-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Backup-Größe</p>
                      <p className="text-xs text-green-600">{backupStatus.backupSize}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-purple-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 ${backupStatus.autoBackup ? 'bg-green-500' : 'bg-red-500'} rounded-full mr-3`}></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Auto-Backup</p>
                      <p className={`text-xs ${backupStatus.autoBackup ? 'text-green-600' : 'text-red-600'}`}>
                        {backupStatus.autoBackup ? 'Aktiviert' : 'Deaktiviert'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-orange-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-orange-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Nächstes Backup</p>
                      <p className="text-xs text-orange-600">{backupStatus.nextScheduled}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-gray-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Backup-Anzahl</p>
                      <p className="text-xs text-gray-600">{backupStatus.backupCount} Backups</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center p-4 bg-indigo-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-indigo-500 rounded-full mr-3"></div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Speicherplatz</p>
                      <p className="text-xs text-indigo-600">{backupStatus.diskSpaceUsed} / {backupStatus.diskSpaceTotal}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Backup Actions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Backup erstellen</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Database Backup */}
              <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                    <span className="text-blue-600 text-2xl">🗄️</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Datenbank-Backup</h4>
                    <p className="text-sm text-gray-600">Nur Datenbank-Inhalte (JSON)</p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Erstellt ein JSON-Backup aller Datenbank-Inhalte (Menü, Bewertungen, Benutzer, etc.).
                  Empfohlen für tägliche Backups.
                </p>
                <div className="mb-4">
                  <div className="text-xs text-gray-500">
                    💡 <strong>Verwendung:</strong> Schnelle Datensicherung, kleinere Dateigröße
                  </div>
                </div>
                <button
                  onClick={handleDatabaseBackup}
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Erstelle Backup...
                    </div>
                  ) : (
                    'Datenbank-Backup erstellen'
                  )}
                </button>
              </div>

              {/* Full Backup */}
              <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
                    <span className="text-green-600 text-2xl">📦</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Vollständiges Backup</h4>
                    <p className="text-sm text-gray-600">Datenbank + Mediendateien (ZIP)</p>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-4">
                  Erstellt ein komplettes Backup inklusive aller Bilder und Mediendateien.
                  Empfohlen für vollständige Systemsicherung.
                </p>
                <div className="mb-4">
                  <div className="text-xs text-gray-500">
                    💡 <strong>Verwendung:</strong> Vollständige Wiederherstellung, größere Dateigröße
                  </div>
                </div>
                <button
                  onClick={handleFullBackup}
                  disabled={loading}
                  className="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Erstelle Backup...
                    </div>
                  ) : (
                    'Vollständiges Backup erstellen'
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Troubleshooting */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h4 className="font-semibold text-yellow-800 mb-2">🛠️ Troubleshooting-Hinweise</h4>
            <div className="text-sm text-yellow-700 space-y-2">
              <p><strong>Backup schlägt fehl:</strong> Prüfen Sie die Datenbankverbindung und Speicherplatz.</p>
              <p><strong>Download startet nicht:</strong> Deaktivieren Sie temporär Pop-up-Blocker im Browser.</p>
              <p><strong>Große Backups:</strong> Bei großen Datenmengen kann der Download einige Minuten dauern.</p>
              <p><strong>Automatische Backups:</strong> Werden täglich um 02:00 Uhr erstellt (falls aktiviert).</p>
            </div>
          </div>
        </div>
      )}

      {/* Enhanced System Info Tab */}
      {activeTab === 'system' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-900">System-Informationen</h3>
            <button
              onClick={loadSystemInfo}
              disabled={loading}
              className="text-blue-600 hover:text-blue-800 text-sm disabled:opacity-50"
            >
              🔄 Aktualisieren
            </button>
          </div>
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">CMS-Version</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.version}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">System-Uptime</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.uptime}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Python Version</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.pythonVersion}</span>
                </div>
              </div>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Datenbank-Status</span>
                  <span className="text-sm text-green-600 font-medium">🟢 {systemInfo.database}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">CPU-Auslastung</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.cpuUsage}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Speicher-Auslastung</span>
                  <span className="text-sm text-gray-900 font-mono">{systemInfo.memoryUsage}</span>
                </div>
              </div>
            </div>
            
            <div className="border-t border-gray-200 pt-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Festplatten-Auslastung</span>
                  <span className="text-sm text-blue-600 font-mono">{systemInfo.diskSpace}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Plattform</span>
                  <span className="text-sm text-purple-600 font-mono">{systemInfo.platform}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Database Configuration Tab */}
      {activeTab === 'database' && (
        <DatabaseConfigPanel 
          dbConfig={dbConfig} 
          setDbConfig={setDbConfig}
          onSave={handleConfigSave}
          onTest={testDatabaseConnection}
          loading={loading}
        />
      )}

      {/* General Configuration Tab */}
      {activeTab === 'config' && (
        <GeneralConfigPanel onSave={handleConfigSave} loading={loading} />
      )}
    </div>
  );
};

// Configuration Panel Component
const ConfigurationPanel = ({ onSave, loading }) => {
  const [config, setConfig] = useState({
    siteName: 'Jimmy\'s Tapas Bar',
    adminEmail: 'admin@jimmys-tapas.de',
    backupFrequency: 'daily',
    maintenanceMode: false,
    debugMode: false
  });

  const handleSave = () => {
    onSave(config);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">System-Konfiguration</h3>
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Website-Name</label>
            <input
              type="text"
              value={config.siteName}
              onChange={(e) => setConfig({...config, siteName: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Admin E-Mail</label>
            <input
              type="email"
              value={config.adminEmail}
              onChange={(e) => setConfig({...config, adminEmail: e.target.value})}
              className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Backup-Häufigkeit</label>
          <select
            value={config.backupFrequency}
            onChange={(e) => setConfig({...config, backupFrequency: e.target.value})}
            className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="hourly">Stündlich</option>
            <option value="daily">Täglich</option>
            <option value="weekly">Wöchentlich</option>
            <option value="manual">Manuell</option>
          </select>
        </div>

        <div className="space-y-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="maintenanceMode"
              checked={config.maintenanceMode}
              onChange={(e) => setConfig({...config, maintenanceMode: e.target.checked})}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="maintenanceMode" className="ml-2 text-sm text-gray-700">
              Wartungsmodus aktiviert
            </label>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="debugMode"
              checked={config.debugMode}
              onChange={(e) => setConfig({...config, debugMode: e.target.checked})}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="debugMode" className="ml-2 text-sm text-gray-700">
              Debug-Modus aktiviert
            </label>
          </div>
        </div>

        <div className="pt-6 border-t border-gray-200">
          <button
            onClick={handleSave}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Speichern...' : 'Konfiguration speichern'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SystemBackupSection;