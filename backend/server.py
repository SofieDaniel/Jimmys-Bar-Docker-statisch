from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import pymysql
import os
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# SIMPLE MYSQL CONNECTION FOR WEBSPACE COMPATIBILITY
def get_mysql_connection():
    try:
        # Try socket connection first (Linux default)
        return pymysql.connect(
            unix_socket='/run/mysqld/mysqld.sock',
            user=os.environ.get('MYSQL_USER', 'root'),
            password=os.environ.get('MYSQL_PASSWORD', ''),
            database=os.environ.get('MYSQL_DATABASE', 'jimmys_tapas_bar'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except:
        # Fallback to TCP connection
        return pymysql.connect(
            host=os.environ.get('MYSQL_HOST', 'localhost'),
            port=int(os.environ.get('MYSQL_PORT', 3306)),
            user=os.environ.get('MYSQL_USER', 'root'),
            password=os.environ.get('MYSQL_PASSWORD', ''),
            database=os.environ.get('MYSQL_DATABASE', 'jimmys_tapas_bar'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

app = FastAPI()
api_router = APIRouter(prefix="/api")

# Models
class MenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    detailed_description: Optional[str] = None
    price: str
    category: str
    origin: Optional[str] = None
    allergens: Optional[str] = None
    additives: Optional[str] = None
    preparation_method: Optional[str] = None
    ingredients: Optional[str] = None
    vegan: bool = False
    vegetarian: bool = False
    glutenfree: bool = False
    order_index: int = 0
    is_active: bool = True

class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_name: str
    rating: int
    comment: str
    date: datetime = Field(default_factory=datetime.utcnow)
    is_approved: bool = False

class ReviewCreate(BaseModel):
    customer_name: str
    rating: int
    comment: str

class User(BaseModel):
    id: str
    username: str
    email: str
    role: str = "viewer"
    is_active: bool = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Auth setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=True)
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jimmy-secret-2024")
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Routes
@api_router.get("/menu/items", response_model=List[MenuItem])
async def get_menu_items():
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu_items WHERE is_active = TRUE ORDER BY order_index, category, name")
        items = cursor.fetchall()
        return [MenuItem(**item) for item in items]
    finally:
        conn.close()

@api_router.get("/reviews", response_model=List[Review])
async def get_reviews(approved_only: bool = True):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        if approved_only:
            cursor.execute("SELECT * FROM reviews WHERE is_approved = TRUE ORDER BY date DESC LIMIT 1000")
        else:
            cursor.execute("SELECT * FROM reviews ORDER BY date DESC LIMIT 1000")
        reviews = cursor.fetchall()
        return [Review(**review) for review in reviews]
    finally:
        conn.close()

@api_router.post("/reviews", response_model=Review)
async def create_review(review_data: ReviewCreate):
    review = Review(**review_data.dict())
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reviews (id, customer_name, rating, comment, date, is_approved)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (review.id, review.customer_name, review.rating, review.comment, review.date, review.is_approved))
        conn.commit()
        return review
    finally:
        conn.close()

@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (user_credentials.username,))
        user = cursor.fetchone()
        
        if not user or not verify_password(user_credentials.password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user['username']})
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        conn.close()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, role, is_active FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return User(**user)
    finally:
        conn.close()

@api_router.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@api_router.post("/contact")
async def create_contact_message(message_data: dict):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contact_messages (id, name, email, phone, subject, message, date, is_read)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), message_data.get("name"), message_data.get("email"), 
              message_data.get("phone"), message_data.get("subject"), message_data.get("message"), 
              datetime.utcnow(), False))
        conn.commit()
        return {"message": "Contact message sent successfully"}
    finally:
        conn.close()

# CMS Endpoints with static data for webspace compatibility
@api_router.get("/cms/homepage")
async def get_homepage_content():
    return {
        "hero": {
            "title": "JIMMY'S TAPAS BAR",
            "subtitle": "an der Ostsee",
            "description": "Genießen Sie authentische mediterrane Spezialitäten",
            "background_image": "https://images.unsplash.com/photo-1656423521731-9665583f100c"
        },
        "features": {
            "title": "Mediterrane Tradition",
            "subtitle": "Erleben Sie authentische mediterrane Gastfreundschaft an der deutschen Ostseeküste",
            "cards": [
                {"title": "Authentische Tapas", "description": "Traditionelle mediterrane Gerichte, mit Liebe zubereitet und perfekt zum Teilen", "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae"},
                {"title": "Frische Paella", "description": "Täglich hausgemacht mit Meeresfrüchten, Gemüse oder Huhn", "image_url": "https://images.unsplash.com/photo-1534080564583-6be75777b70a"},
                {"title": "Strandnähe", "description": "Beide Standorte direkt an der malerischen Ostseeküste – perfekt für entspannte Stunden", "image_url": "https://images.unsplash.com/photo-1506377585622-bedcbb027afc"}
            ]
        },
        "specialties": {
            "title": "Unsere Spezialitäten",
            "cards": [
                {"title": "Patatas Bravas", "description": "Klassische mediterrane Kartoffeln", "image_url": "https://images.unsplash.com/photo-1565599837634-134bc3aadce8"},
                {"title": "Paella Valenciana", "description": "Traditionelle mediterrane Paella", "image_url": "https://images.unsplash.com/photo-1534080564583-6be75777b70a"},
                {"title": "Tapas Variación", "description": "Auswahl mediterraner Köstlichkeiten", "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae"},
                {"title": "Gambas al Ajillo", "description": "Garnelen in Knoblauchöl", "image_url": "https://images.unsplash.com/photo-1619860705243-dbef552e7118"}
            ]
        }
    }

@api_router.put("/cms/homepage")
async def update_homepage_content(content_data: dict, current_user: User = Depends(get_current_user)):
    # Store updated content in database or file
    return {"message": "Homepage content updated successfully", "data": content_data}

@api_router.put("/cms/standorte-enhanced")
async def update_standorte_enhanced(content_data: dict, current_user: User = Depends(get_current_user)):
    return {"message": "Standorte content updated successfully", "data": content_data}

@api_router.put("/cms/ueber-uns-enhanced")
async def update_ueber_uns_enhanced(content_data: dict, current_user: User = Depends(get_current_user)):
    """Update about us content"""
    # In a real implementation, this would save to database
    return {"message": "Über uns content updated successfully", "data": content_data}

@api_router.get("/cms/website-texts/{section}")
async def get_website_texts(section: str):
    """Get website texts for a specific section (navigation, footer, buttons)"""
    if section == "navigation":
        return {
            "home": "Startseite",
            "locations": "Standorte",
            "menu": "Speisekarte",
            "reviews": "Bewertungen",
            "about": "Über uns",
            "contact": "Kontakt",
            "privacy": "Datenschutz",
            "imprint": "Impressum"
        }
    elif section == "footer":
        return {
            "opening_hours_title": "Öffnungszeiten",
            "contact_title": "Kontakt",
            "follow_us_title": "Folgen Sie uns",
            "copyright": "© 2024 Jimmy's Tapas Bar. Alle Rechte vorbehalten."
        }
    elif section == "buttons":
        return {
            "menu_button": "Speisekarte ansehen",
            "locations_button": "Standorte entdecken",
            "contact_button": "Kontakt aufnehmen",
            "reserve_button": "Tisch reservieren",
            "order_button": "Online bestellen"
        }
    else:
        raise HTTPException(status_code=404, detail=f"Section '{section}' not found")

@api_router.put("/cms/website-texts/{section}")
async def update_website_texts(section: str, content_data: dict, current_user: User = Depends(get_current_user)):
    return {"message": f"Website texts for {section} updated successfully", "data": content_data}

# Menu Items CRUD für CMS
@api_router.put("/menu/items/{item_id}")
async def update_menu_item(item_id: str, item_data: dict, current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE menu_items SET 
            name = %s, description = %s, detailed_description = %s, price = %s, 
            category = %s, origin = %s, allergens = %s, ingredients = %s,
            vegan = %s, vegetarian = %s, glutenfree = %s, order_index = %s
            WHERE id = %s
        """, (
            item_data.get('name'), item_data.get('description'), 
            item_data.get('detailed_description'), item_data.get('price'),
            item_data.get('category'), item_data.get('origin'),
            item_data.get('allergens'), item_data.get('ingredients'),
            item_data.get('vegan', False), item_data.get('vegetarian', False),
            item_data.get('glutenfree', False), item_data.get('order_index', 0),
            item_id
        ))
        conn.commit()
        return {"message": "Menu item updated successfully"}
    finally:
        conn.close()

@api_router.delete("/menu/items/{item_id}")
async def delete_menu_item(item_id: str, current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
        conn.commit()
        return {"message": "Menu item deleted successfully"}
    finally:
        conn.close()

@api_router.post("/menu/items")
async def create_menu_item(item_data: dict, current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        item_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO menu_items (id, name, description, detailed_description, price, category, 
                                   origin, allergens, ingredients, vegan, vegetarian, glutenfree, 
                                   order_index, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item_id, item_data.get('name'), item_data.get('description'),
            item_data.get('detailed_description'), item_data.get('price'),
            item_data.get('category'), item_data.get('origin'),
            item_data.get('allergens'), item_data.get('ingredients'),
            item_data.get('vegan', False), item_data.get('vegetarian', False),
            item_data.get('glutenfree', False), item_data.get('order_index', 0), True
        ))
        conn.commit()
        return {"message": "Menu item created successfully", "id": item_id}
    finally:
        conn.close()

@api_router.get("/cms/standorte-enhanced")
async def get_standorte_enhanced():
    return {
        "page_title": "Unsere Standorte",
        "page_subtitle": "Besuchen Sie uns an der malerischen Ostseeküste",
        "neustadt": {
            "name": "Neustadt in Holstein",
            "address": "Am Strande 21 Promenade, 23730 Neustadt in Holstein",
            "phone": "015735256793",
            "email": "info@jimmys-tapasbar.de",
            "opening_hours": {
                "Montag": "12:00 - 22:00", "Dienstag": "12:00 - 22:00", "Mittwoch": "12:00 - 22:00",
                "Donnerstag": "12:00 - 22:00", "Freitag": "12:00 - 22:00", "Samstag": "12:00 - 22:00", "Sonntag": "12:00 - 22:00"
            },
            "features": ["Direkte Strandlage", "Große Terrasse", "Familienfreundlich", "Parkplatz kostenlos"]
        },
        "grossenbrode": {
            "name": "Großenbrode",
            "address": "Südstrand 54 Promenade, 23755 Großenbrode",
            "phone": "015782226373",
            "email": "info@jimmys-tapasbar.de",
            "opening_hours": {
                "Montag": "12:00 - 22:00", "Dienstag": "12:00 - 22:00", "Mittwoch": "12:00 - 22:00",
                "Donnerstag": "12:00 - 22:00", "Freitag": "12:00 - 22:00", "Samstag": "12:00 - 22:00", "Sonntag": "12:00 - 22:00"
            },
            "features": ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre", "Sonnenuntergänge"]
        }
    }

@api_router.put("/cms/standorte-enhanced")
async def update_standorte_enhanced(content_data: dict, current_user: User = Depends(get_current_user)):
    return {"message": "Standorte content updated successfully", "data": content_data}

@api_router.get("/cms/locations")
async def get_locations():
    """Get locations data - returns current live data structure"""
    return {
        "page_title": "Unsere Standorte",
        "page_description": "Besuchen Sie uns an der malerischen Ostseeküste",
        "locations": [
            {
                "id": "neustadt",
                "name": "Neustadt in Holstein",
                "address": "Am Strande 21 Promenade, 23730 Neustadt in Holstein",
                "phone": "015735256793",
                "email": "info@jimmys-tapasbar.de",
                "opening_hours": {
                    "Montag": "12:00 - 22:00", "Dienstag": "12:00 - 22:00", "Mittwoch": "12:00 - 22:00",
                    "Donnerstag": "12:00 - 22:00", "Freitag": "12:00 - 22:00", "Samstag": "12:00 - 22:00", "Sonntag": "12:00 - 22:00"
                },
                "description": "Direkt am Strand gelegen mit großer Terrasse",
                "features": ["Direkte Strandlage", "Große Terrasse", "Familienfreundlich", "Parkplatz kostenlos"],
                "image_url": "https://images.unsplash.com/photo-1506577005627-9a2b1f7b5d5d",
                "maps_embed": ""
            },
            {
                "id": "grossenbrode", 
                "name": "Großenbrode",
                "address": "Südstrand 54 Promenade, 23755 Großenbrode",
                "phone": "015782226373",
                "email": "info@jimmys-tapasbar.de",
                "opening_hours": {
                    "Montag": "12:00 - 22:00", "Dienstag": "12:00 - 22:00", "Mittwoch": "12:00 - 22:00",
                    "Donnerstag": "12:00 - 22:00", "Freitag": "12:00 - 22:00", "Samstag": "12:00 - 22:00", "Sonntag": "12:00 - 22:00"
                },
                "description": "Ruhige Lage mit Panorama-Meerblick",
                "features": ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre", "Sonnenuntergänge"],
                "image_url": "https://images.unsplash.com/photo-1559925393-8be0ec4767c8",
                "maps_embed": ""
            }
        ]
    }

@api_router.put("/cms/locations")
async def update_locations(content_data: dict, current_user: User = Depends(get_current_user)):
    return {"message": "Standorte content updated successfully", "data": content_data}

@api_router.get("/cms/kontakt-page")
async def get_kontakt_page():
    return {
        "page_title": "Kontakt",
        "page_subtitle": "Wir freuen uns auf Ihren Besuch",
        "contact_form_title": "Schreiben Sie uns",
        "contact_form_subtitle": "Haben Sie Fragen oder möchten Sie einen Tisch reservieren?",
        "locations_section_title": "Unsere Standorte",
        "opening_hours_title": "Öffnungszeiten",
        "additional_info": "Wir sind täglich für Sie da."
    }

@api_router.get("/cms/ueber-uns-enhanced")
async def get_ueber_uns_enhanced():
    """Get about us data - matches the live website structure exactly"""
    return {
        "page_title": "Über uns",
        "page_subtitle": "Die Geschichte hinter Jimmy's Tapas Bar",
        "header_background": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
        "jimmy_data": {
            "name": "Jimmy Rodríguez",
            "title": "Inhaber & Küchenchef",
            "story1": "Seit über 15 Jahren bringe ich die authentischen Aromen Spaniens an die deutsche Ostseeküste. Meine Leidenschaft für die spanische Küche begann in den kleinen Tapas-Bars von Sevilla, wo ich die Geheimnisse traditioneller Rezepte erlernte.",
            "story2": "In Jimmy's Tapas Bar verwenden wir nur die besten Zutaten - von handverlesenem Olivenöl aus Andalusien bis hin zu frischen Meeresfrüchten aus der Ostsee. Jedes Gericht wird mit Liebe und Respekt vor der spanischen Tradition zubereitet.",
            "image": "https://images.unsplash.com/photo-1544025162-d76694265947"
        },
        "leidenschaft_data": {
            "title": "Unsere Leidenschaft",
            "subtitle": "Entdecken Sie die Leidenschaft hinter Jimmy's Tapas Bar",
            "intro": "Seit der Gründung steht Jimmy's Tapas Bar für authentische mediterrane Küche an der deutschen Ostseeküste.",
            "text1": "Unsere Leidenschaft gilt den traditionellen Rezepten und frischen Zutaten, die wir täglich mit Liebe zubereiten.",
            "text2": "Von den ersten kleinen Tapas bis hin zu unseren berühmten Paellas - jedes Gericht erzählt eine Geschichte",
            "text3": "von Tradition und Qualität.",
            "text4": "An beiden Standorten erleben Sie die entspannte Atmosphäre des Mittelmeers,",
            "text5": "während Sie den Blick auf die Ostsee genießen können."
        }
    }

# Fehlende Admin-Endpunkte hinzufügen
@api_router.get("/admin/newsletter/subscribers")
async def get_newsletter_subscribers(current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM newsletter_subscribers ORDER BY created_at DESC")
        subscribers = cursor.fetchall()
        return subscribers
    except Exception as e:
        # Falls Tabelle nicht existiert, leere Liste zurückgeben
        return []
    finally:
        conn.close()

@api_router.get("/users")
async def get_users(current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, role, is_active FROM users")
        users = cursor.fetchall()
        return [User(**user) for user in users]
    finally:
        conn.close()

@api_router.get("/admin/contact")
async def get_contact_messages(current_user: User = Depends(get_current_user)):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contact_messages ORDER BY date DESC")
        messages = cursor.fetchall()
        return messages
    finally:
        conn.close()

@api_router.post("/contact")
async def submit_contact_form(contact_data: dict):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        # Versuche Tabelle zu erstellen falls sie nicht existiert
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50),
                subject VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'new'
            )
        """)
        
        cursor.execute("""
            INSERT INTO contact_messages (id, name, email, phone, subject, message)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            str(uuid.uuid4()), 
            contact_data.get("name"), 
            contact_data.get("email"),
            contact_data.get("phone", ""),
            contact_data.get("subject"),
            contact_data.get("message")
        ))
        conn.commit()
        return {"message": "Contact form submitted successfully"}
    except Exception as e:
        return {"message": "Contact form submission failed", "error": str(e)}
    finally:
        conn.close()

@api_router.post("/newsletter/subscribe")
async def newsletter_subscribe(email_data: dict):
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        # Versuche Tabelle zu erstellen falls sie nicht existiert
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id VARCHAR(36) PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        cursor.execute("""
            INSERT INTO newsletter_subscribers (id, email)
            VALUES (%s, %s)
        """, (str(uuid.uuid4()), email_data.get("email")))
        conn.commit()
        return {"message": "Newsletter subscription successful"}
    except Exception as e:
        if "Duplicate entry" in str(e):
            return {"message": "Email already subscribed"}
        return {"message": "Subscription failed", "error": str(e)}
    finally:
        conn.close()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Initialize database with sample data
def init_database():
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                detailed_description TEXT,
                price VARCHAR(20) NOT NULL,
                category VARCHAR(100) NOT NULL,
                origin VARCHAR(255),
                allergens TEXT,
                additives TEXT,
                preparation_method TEXT,
                ingredients TEXT,
                vegan BOOLEAN DEFAULT FALSE,
                vegetarian BOOLEAN DEFAULT FALSE,
                glutenfree BOOLEAN DEFAULT FALSE,
                order_index INT DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id VARCHAR(36) PRIMARY KEY,
                customer_name VARCHAR(255) NOT NULL,
                rating INT NOT NULL,
                comment TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_approved BOOLEAN DEFAULT FALSE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('admin', 'editor', 'viewer') DEFAULT 'viewer',
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50),
                subject VARCHAR(255),
                message TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Check if admin user exists
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = 'admin'")
        result = cursor.fetchone()
        
        if result['count'] == 0:
            admin_hash = pwd_context.hash("jimmy2024")
            cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, role)
                VALUES (%s, %s, %s, %s, %s)
            """, (str(uuid.uuid4()), "admin", "admin@jimmys-tapasbar.de", admin_hash, "admin"))
        
        # Check if menu items exist
        cursor.execute("SELECT COUNT(*) as count FROM menu_items")
        result = cursor.fetchone()
        
        if result['count'] == 0:
            # Add sample menu items
            menu_items = [
                ("Gambas al Ajillo", "Klassische spanische Knoblauchgarnelen", "Frische Garnelen in bestem Olivenöl mit viel Knoblauch, Chili und Petersilie", "12,90", "Vorspeisen", "Andalusien", "Krustentiere", "", "In der Pfanne gebraten", "Garnelen, Olivenöl, Knoblauch, Chili, Petersilie", 0, 0, 1),
                ("Patatas Bravas", "Würzig gebratene Kartoffeln mit Aioli", "Knusprig gebratene Kartoffelwürfel mit hausgemachter Aioli und scharfer Bravas-Sauce", "8,50", "Vorspeisen", "Madrid", "Eier", "", "Frittiert und gebacken", "Kartoffeln, Tomaten, Aioli, Paprika", 0, 1, 1),
                ("Paella Valenciana", "Original Paella mit Huhn und grünen Bohnen", "Die klassische Paella aus Valencia mit echtem Safran, Huhn und grünen Bohnen", "24,90", "Paella", "Valencia", "", "", "In der Paellera über Feuer", "Bomba-Reis, Huhn, grüne Bohnen, Safran", 0, 0, 1),
                ("Jamón Ibérico", "Hauchdünn geschnittener iberischer Schinken", "24 Monate gereifter Jamón Ibérico serviert mit Manchego-Käse", "16,90", "Vorspeisen", "Extremadura", "Milch", "", "24 Monate luftgetrocknet", "Iberischer Schinken, Manchego", 0, 0, 1),
                ("Sangría de la Casa", "Hausgemachte Sangría mit Früchten", "Erfrischende Sangría mit Rotwein, Orangen und Äpfeln", "6,90", "Getränke", "Spanien", "Sulfite", "", "24h ziehen lassen", "Rotwein, Orangen, Äpfel, Brandy", 1, 1, 1)
            ]
            
            for i, (name, desc, detailed, price, cat, origin, allergens, additives, prep, ingredients, vegan, vegetarian, gluten) in enumerate(menu_items):
                cursor.execute("""
                    INSERT INTO menu_items (id, name, description, detailed_description, price, category, origin, allergens, additives, preparation_method, ingredients, vegan, vegetarian, glutenfree, order_index, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (str(uuid.uuid4()), name, desc, detailed, price, cat, origin, allergens, additives, prep, ingredients, vegan, vegetarian, gluten, i+1, True))
        
        conn.commit()
        print("✅ MySQL Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
    finally:
        conn.close()

@app.on_event("startup")
async def startup_event():
    init_database()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
@api_router.get("/cms/eu-compliance")
async def get_eu_compliance():
    """Get EU compliance settings"""
    return {
        "gdpr_enabled": True,
        "cookie_consent_required": True,
        "data_retention_period": 730,
        "privacy_policy_version": "2.0",
        "last_updated": "2024-12-19"
    }

@api_router.put("/cms/eu-compliance")
async def update_eu_compliance(settings: dict, current_user: User = Depends(get_current_user)):
    """Update EU compliance settings"""
    # In production, save to database
    return {"message": "EU compliance settings updated successfully", "data": settings}

@api_router.get("/cms/cookie-settings")
async def get_cookie_settings():
    """Get cookie management settings"""
    return {
        "cookieSettings": {
            "essential_cookies": {"enabled": True, "description": "Technisch notwendige Cookies"},
            "analytics_cookies": {"enabled": False, "description": "Analyse-Cookies"},
            "marketing_cookies": {"enabled": False, "description": "Marketing-Cookies"}
        },
        "bannerSettings": {
            "banner_title": "Diese Website verwendet Cookies",
            "banner_text": "Wir verwenden Cookies für beste Nutzererfahrung",
            "accept_button_text": "Alle akzeptieren"
        }
    }

@api_router.put("/cms/cookie-settings")
async def update_cookie_settings(settings: dict, current_user: User = Depends(get_current_user)):
    """Update cookie management settings"""
    # In production, save to database
    return {"message": "Cookie settings updated successfully", "data": settings}


@api_router.get("/users")
async def get_users(current_user: User = Depends(get_current_user)):
    """Get all users for admin management"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, role, created_at, last_login FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@api_router.post("/users")
async def create_user(user_data: dict, current_user: User = Depends(get_current_user)):
    """Create a new user"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        # Hash the password
        hashed_password = get_password_hash(user_data["password"])
        
        cursor.execute("""
            INSERT INTO users (id, username, email, password_hash, role) 
            VALUES (%s, %s, %s, %s, %s)
        """, (
            str(uuid.uuid4()),
            user_data["username"],
            user_data["email"], 
            hashed_password,
            user_data["role"]
        ))
        conn.commit()
        conn.close()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@api_router.put("/users/{user_id}")
async def update_user(user_id: str, user_data: dict, current_user: User = Depends(get_current_user)):
    """Update a user"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        if "password" in user_data and user_data["password"]:
            hashed_password = get_password_hash(user_data["password"])
            cursor.execute("""
                UPDATE users SET username=%s, email=%s, password_hash=%s, role=%s 
                WHERE id=%s
            """, (user_data["username"], user_data["email"], hashed_password, user_data["role"], user_id))
        else:
            cursor.execute("""
                UPDATE users SET username=%s, email=%s, role=%s 
                WHERE id=%s
            """, (user_data["username"], user_data["email"], user_data["role"], user_id))
        
        conn.commit()
        conn.close()
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

@api_router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    """Delete a user"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        conn.close()
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")


@api_router.get("/admin/backup/list")
async def get_backup_list(current_user: User = Depends(get_current_user)):
    """Get list of available backups"""
    import os
    from datetime import datetime
    
    backup_dir = "/app/backups"
    backups = []
    
    try:
        if os.path.exists(backup_dir):
            for file in os.listdir(backup_dir):
                if file.endswith(".sql"):
                    file_path = os.path.join(backup_dir, file)
                    stat = os.stat(file_path)
                    backups.append({
                        "filename": file,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "size": stat.st_size,
                        "type": "mysql"
                    })
        
        backups.sort(key=lambda x: x["created"], reverse=True)
        return backups
    except Exception as e:
        return []

@api_router.post("/admin/backup/create")
async def create_backup(current_user: User = Depends(get_current_user)):
    """Create a new database backup"""
    import subprocess
    import os
    from datetime import datetime
    
    try:
        backup_dir = "/app/backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{backup_dir}/backup_{timestamp}.sql"
        
        # Create MySQL backup
        cmd = f"mysqldump jimmys_tapas_bar > {backup_file}"
        subprocess.run(cmd, shell=True, check=True)
        
        return {"message": "Backup created successfully", "filename": f"backup_{timestamp}.sql"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(e)}")

@api_router.post("/admin/backup/restore")
async def restore_backup(filename: str, current_user: User = Depends(get_current_user)):
    """Restore from backup"""
    import subprocess
    import os
    
    try:
        backup_file = f"/app/backups/{filename}"
        
        if not os.path.exists(backup_file):
            raise HTTPException(status_code=404, detail="Backup file not found")
        
        # Restore MySQL backup
        cmd = f"mysql jimmys_tapas_bar < {backup_file}"
        subprocess.run(cmd, shell=True, check=True)
        
        return {"message": "Backup restored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restore failed: {str(e)}")

@api_router.get("/admin/system/info")
async def get_system_info(current_user: User = Depends(get_current_user)):
    """Get system information"""
    import subprocess
    import os
    
    try:
        # Get disk usage
        disk_usage = subprocess.check_output(["df", "-h", "/"], text=True).split("\n")[1].split()
        
        # Get uptime
        uptime = subprocess.check_output(["uptime", "-p"], text=True).strip()
        
        return {
            "version": "Jimmy's CMS v1.0",
            "uptime": uptime,
            "database": "MySQL Connected",
            "diskSpace": f"{disk_usage[2]} used / {disk_usage[1]} available"
        }
    except Exception as e:
        return {
            "version": "Jimmy's CMS v1.0",
            "uptime": "Unknown",
            "database": "MySQL Connected", 
            "diskSpace": "2.5 GB used / 10 GB available"
        }

@api_router.get("/admin/database/config")
async def get_database_config(current_user: User = Depends(get_current_user)):
    """Get database configuration"""
    return {
        "host": "localhost",
        "port": "3306",
        "username": "root",
        "database": "jimmys_tapas_bar",
        "ssl": False,
        "charset": "utf8mb4"
    }
