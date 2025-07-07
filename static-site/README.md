# Jimmy's Tapas Bar - Statische Website

Eine vollständig statische Website für Jimmy's Tapas Bar mit dynamischer Speisekarte über INI-Konfiguration.

## 🚀 Quick Start

### Lokale Installation und Start

1. **Repository klonen oder herunterladen**
   ```bash
   # Falls Git verfügbar
   git clone [repository-url]
   cd jimmys-tapas-static
   
   # Oder ZIP-Datei entpacken
   ```

2. **HTTP-Server starten**
   ```bash
   # Mit Node.js (empfohlen)
   npx http-server ./dist -p 8080 -o
   
   # Mit Python 3
   cd dist && python -m http.server 8080
   
   # Mit PHP
   cd dist && php -S localhost:8080
   ```

3. **Website öffnen**
   - Automatisch: Browser öffnet sich auf `http://localhost:8080`
   - Manuell: `http://localhost:8080` im Browser aufrufen

## 📁 Projektstruktur

```
static-site/
├── dist/                          # Produktions-Website
│   ├── index.html                 # Hauptseite
│   ├── css/
│   │   ├── styles.css             # Haupt-Stylesheet
│   │   └── speisekarte.css        # Speisekarte-spezifische Styles
│   ├── js/
│   │   ├── main.js                # Haupt-JavaScript
│   │   └── speisekarte.js         # Speisekarte-Funktionalität
│   ├── config/
│   │   └── menu.ini               # Speisekarte-Konfiguration
│   ├── pages/                     # Unterseiten
│   │   ├── speisekarte.html       # Speisekarte
│   │   ├── standorte.html         # Standorte (Template)
│   │   ├── ueber-uns.html         # Über uns (Template)
│   │   ├── kontakt.html           # Kontakt (Template)
│   │   ├── bewertungen.html       # Bewertungen (Template)
│   │   ├── impressum.html         # Impressum (Template)
│   │   └── datenschutz.html       # Datenschutz (Template)
│   └── assets/                    # Medien-Dateien
│       ├── images/                # Bilder
│       ├── icons/                 # Icons
│       └── fonts/                 # Lokale Schriftarten (optional)
└── README.md                      # Diese Datei
```

## 🍽️ Speisekarte bearbeiten (menu.ini)

### INI-Datei-Format

Die Speisekarte wird über die Datei `dist/config/menu.ini` konfiguriert:

```ini
# Kommentare beginnen mit #

[SETTINGS]
restaurant_name = Jimmy's Tapas Bar
currency = EUR
currency_symbol = €

[CATEGORIES]
inicio = Inicio / Vorspeisen
carnes = Carnes / Fleischgerichte
pescados = Pescados / Fischgerichte
paellas = Paellas
postres = Postres / Nachspeisen
bebidas = Bebidas / Getränke

# Gericht-Definitionen
[inicio_1]
name = Gambas al Ajillo
description = Klassische Knoblauchgarnelen in Olivenöl
detailed_description = Frische Garnelen, scharf angebraten in bestem Olivenöl mit viel Knoblauch und Petersilie
price = 12.90
category = inicio
allergens = Krustentiere
origin = Andalusien
preparation = In Knoblauchöl
ingredients = Garnelen, Knoblauch, Petersilie, Olivenöl, Chili
vegetarian = false
vegan = false
image = https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b
```

### Neues Gericht hinzufügen

1. **Eindeutige Sektion erstellen:**
   ```ini
   [kategorie_nummer]  # z.B. [inicio_5] oder [paellas_3]
   ```

2. **Pflichtfelder ausfüllen:**
   ```ini
   name = Gericht-Name
   description = Kurze Beschreibung
   price = 15.90
   category = inicio  # Muss in [CATEGORIES] definiert sein
   ```

3. **Optionale Felder:**
   ```ini
   detailed_description = Ausführliche Beschreibung für Modal
   allergens = Gluten, Eier
   origin = Region/Stadt
   preparation = Zubereitungsart
   ingredients = Zutatenliste
   vegetarian = true/false
   vegan = true/false
   image = URL zum Bild
   ```

### Kategorie hinzufügen

1. **In [CATEGORIES] Sektion:**
   ```ini
   [CATEGORIES]
   neue_kategorie = Deutscher Name der Kategorie
   ```

2. **Gerichte der Kategorie zuordnen:**
   ```ini
   [gericht_1]
   category = neue_kategorie
   ```

### Beispiel: Neues Gericht hinzufügen

```ini
[bebidas_4]
name = Agua con Gas
description = Spanisches Mineralwasser mit Kohlensäure
detailed_description = Erfrischendes Mineralwasser aus den spanischen Bergen, natürlich mit Kohlensäure versetzt
price = 2.50
category = bebidas
allergens = 
origin = Spanien
preparation = Gekühlt serviert
ingredients = Mineralwasser, natürliche Kohlensäure
vegetarian = true
vegan = true
image = https://images.unsplash.com/photo-1560472354-b33ff0c44a43
```

## 🎨 Design-Anpassungen

### Farben ändern (CSS Custom Properties)

In `dist/css/styles.css` können die Hauptfarben angepasst werden:

```css
:root {
    --warm-brown: #3D2B1F;      /* Warmes Braun */
    --dark-brown: #2D1F1A;      /* Dunkles Braun */
    --medium-brown: #4A3426;    /* Mittleres Braun */
    --warm-beige: #F5E6D3;      /* Warmes Beige */
    --light-beige: #E8DCC0;     /* Helles Beige */
}
```

### Schriftarten ändern

Google Fonts werden in den HTML-Dateien eingebunden:

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
```

Verwendung im CSS:
```css
.font-serif {
    font-family: 'Playfair Display', serif;  /* Überschriften */
}

body {
    font-family: 'Inter', sans-serif;        /* Fließtext */
}
```

## 🌐 Deployment

### Statisches Hosting

Die Website kann auf jedem statischen Hosting-Service bereitgestellt werden:

#### GitHub Pages
1. Repository erstellen
2. `dist/` Ordner als Root setzen
3. GitHub Pages aktivieren

#### Netlify
1. `dist/` Ordner per Drag & Drop hochladen
2. Automatische URL erhalten

#### Vercel
```bash
npx vercel --cwd dist
```

#### Traditionelles Webhosting
1. Alle Dateien aus `dist/` per FTP hochladen
2. `index.html` als Startseite konfigurieren

### Server-Konfiguration

#### Apache (.htaccess)
```apache
# In dist/.htaccess
Options -Indexes
DirectoryIndex index.html

# Gzip Kompression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript
</IfModule>

# Cache Headers
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
</IfModule>
```

#### Nginx
```nginx
server {
    listen 80;
    server_name jimmys-tapasbar.de;
    root /var/www/jimmys-tapas;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location ~* \.(css|js)$ {
        expires 1M;
        add_header Cache-Control "public, immutable";
    }
    
    location ~* \.(jpg|jpeg|png|gif|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🔧 Technische Details

### Verwendete Technologien

- **HTML5**: Semantisches Markup
- **CSS3**: Custom Properties, Grid, Flexbox
- **Vanilla JavaScript**: ES6+, Fetch API
- **INI-Parser**: Eigene Implementierung
- **Google Fonts**: Playfair Display, Inter
- **Unsplash**: Beispielbilder

### Browser-Kompatibilität

- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

### Performance-Optimierungen

- **Kritisches CSS**: Inline für schnellere Darstellung
- **Lazy Loading**: Bilder werden bei Bedarf geladen
- **Minimierte Assets**: CSS und JS optimiert
- **Responsive Images**: Verschiedene Bildgrößen
- **Service Worker**: Offline-Funktionalität (optional)

### Accessibility (Barrierefreiheit)

- **Semantisches HTML**: Korrekte Heading-Struktur
- **ARIA-Labels**: Screen Reader Unterstützung
- **Keyboard Navigation**: Vollständig tastatursteuerbar
- **Color Contrast**: WCAG 2.1 AA konform
- **Focus Indicators**: Sichtbare Fokus-Zustände

## 🍪 Cookie & DSGVO-Konformität

### Cookie-Banner

Automatisches Cookie-Banner mit:
- **Technisch notwendige Cookies**: Immer aktiv
- **Analyse-Cookies**: Optional
- **Marketing-Cookies**: Optional
- **Komfort-Cookies**: Optional

### Datenschutz-Features

- **Local Storage**: Nur für Cookie-Einstellungen
- **Keine Tracking-Scripts**: Standardmäßig deaktiviert
- **DSGVO-konform**: Opt-in statt Opt-out
- **Cookie-Richtlinie**: Vollständige Transparenz

## 🐛 Troubleshooting

### Häufige Probleme

#### Menu.ini lädt nicht
```javascript
// Fehler in der Browser-Konsole prüfen
// Häufige Ursachen:
// 1. CORS-Policy bei file:// URLs
// 2. Syntaxfehler in der INI-Datei
// 3. Falscher Pfad zur Datei
```

**Lösung:**
- Immer HTTP-Server verwenden (nie file://)
- INI-Syntax validieren
- Browser-Konsole auf Fehler prüfen

#### Bilder werden nicht angezeigt
```ini
# Korrekte Bild-URLs verwenden
image = https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b

# Keine lokalen Pfade ohne HTTP-Server
# FALSCH: image = ../images/gericht.jpg
# RICHTIG: image = https://example.com/images/gericht.jpg
```

#### Mobile Navigation funktioniert nicht
```javascript
// JavaScript-Fehler prüfen
// Mobile Menu Button Event Listener
document.getElementById('mobileMenuBtn').addEventListener('click', ...)
```

### Debug-Modus

Entwickler-Tools öffnen (F12) für:
- **Console**: JavaScript-Fehler und Logs
- **Network**: HTTP-Requests prüfen
- **Elements**: HTML/CSS inspizieren
- **Application**: Local Storage prüfen

## 📞 Support

### Häufige Anpassungen

1. **Restaurant-Name ändern**:
   - `dist/config/menu.ini` → `[SETTINGS]` → `restaurant_name`
   - HTML-Titel in allen Dateien anpassen

2. **Kontaktdaten aktualisieren**:
   - Footer in allen HTML-Dateien
   - `dist/pages/kontakt.html`

3. **Öffnungszeiten ändern**:
   - Footer in allen HTML-Dateien
   - `dist/pages/standorte.html`

4. **Social Media Links**:
   - Footer-Bereich in HTML-Dateien

### Weitere Entwicklung

Für erweiterte Funktionen:
- **Reservierungssystem**: Backend erforderlich
- **Online-Bestellungen**: E-Commerce-Integration
- **CMS-System**: Headless CMS anbinden
- **Multi-Language**: i18n-Unterstützung

## 📄 Lizenz

© 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten.

**Design und Code**: Entwickelt für statische Website-Verwendung  
**Bilder**: Unsplash (freie Lizenz)  
**Schriftarten**: Google Fonts (Open Font License)

---

*Diese Dokumentation beschreibt eine vollständig funktionsfähige, statische Website mit dynamischer Menü-Konfiguration. Alle Designelemente wurden exakt aus der ursprünglichen React-Anwendung übernommen und für statische Verwendung optimiert.*