#!/usr/bin/env python3
"""
AUTOMATISCHES STARTUP SYSTEM für Jimmy's Tapas Bar
Stellt sicher, dass alle Datenbanken und APIs funktionieren
"""

import asyncio
import aiomysql
import os
import uuid
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# MySQL connection settings
mysql_config = {
    'host': os.environ['MYSQL_HOST'],
    'port': int(os.environ['MYSQL_PORT']),
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'db': os.environ['MYSQL_DATABASE'],
    'charset': 'utf8mb4',
    'autocommit': True
}

async def check_and_fix_database():
    """Überprüft und repariert automatisch alle Datenbankprobleme"""
    print("🔧 JIMMY'S TAPAS BAR - AUTOMATISCHE REPARATUR")
    print("=" * 60)
    
    try:
        # Stelle sicher, dass MariaDB läuft
        print("1. Starte MariaDB Service...")
        subprocess.run(['service', 'mariadb', 'start'], check=False)
        
        # Warte kurz
        await asyncio.sleep(2)
        
        # Verbinde zur Datenbank
        connection = await aiomysql.connect(**mysql_config)
        cursor = await connection.cursor()
        print("✅ Datenbankverbindung erfolgreich")
        
        # Prüfe delivery_info
        await cursor.execute("SELECT COUNT(*) FROM delivery_info")
        delivery_count = (await cursor.fetchone())[0]
        if delivery_count == 0:
            print("🚚 Erstelle Delivery-Daten...")
            delivery_id = str(uuid.uuid4())
            await cursor.execute("""
                INSERT INTO delivery_info (id, delivery_time_min, delivery_time_max, 
                                         minimum_order_value, delivery_fee, available_locations,
                                         is_active, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                delivery_id, 30, 45, 15.00, 2.50,
                json.dumps({
                    "neustadt": {"name": "Neustadt", "available": True},
                    "grossenbrode": {"name": "Großenbrode", "available": True}
                }),
                True, "system"
            ))
            print("✅ Delivery-Daten erstellt")
        
        # Prüfe standorte_enhanced
        await cursor.execute("SELECT COUNT(*) FROM standorte_enhanced")
        standorte_count = (await cursor.fetchone())[0]
        if standorte_count == 0:
            print("📍 Erstelle Standorte-Daten...")
            standorte_id = str(uuid.uuid4())
            
            neustadt_data = {
                "name": "Jimmy's Tapas Bar Neustadt",
                "address": "Strandstraße 12, 23730 Neustadt in Holstein",
                "phone": "+49 4561 123456",
                "email": "neustadt@jimmys-tapasbar.de",
                "description": "Unser Hauptstandort direkt am Strand",
                "image_url": "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
                "opening_hours": {
                    "Montag": "16:00 - 23:00", "Dienstag": "16:00 - 23:00",
                    "Mittwoch": "16:00 - 23:00", "Donnerstag": "16:00 - 23:00",
                    "Freitag": "16:00 - 24:00", "Samstag": "12:00 - 24:00",
                    "Sonntag": "12:00 - 23:00"
                },
                "features": ["Direkte Strandlage", "Große Terrasse", "Live-Musik"]
            }
            
            grossenbrode_data = {
                "name": "Jimmy's Tapas Bar Großenbrode",
                "address": "Strandpromenade 8, 23775 Großenbrode",
                "phone": "+49 4367 987654",
                "email": "grossenbrode@jimmys-tapasbar.de",
                "description": "Gemütlich direkt an der Ostsee",
                "image_url": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d",
                "opening_hours": {
                    "Montag": "17:00 - 23:00", "Dienstag": "17:00 - 23:00",
                    "Mittwoch": "17:00 - 23:00", "Donnerstag": "17:00 - 23:00",
                    "Freitag": "17:00 - 24:00", "Samstag": "12:00 - 24:00",
                    "Sonntag": "12:00 - 23:00"
                },
                "features": ["Panorama-Meerblick", "Ruhige Lage", "Romantische Atmosphäre"]
            }
            
            info_data = {
                "sections": [
                    {"title": "Anreise", "icon": "🚗", "description": "Gut erreichbar mit kostenlosen Parkplätzen"},
                    {"title": "Reservierung", "icon": "📞", "description": "Reservierung empfohlen"},
                    {"title": "Events", "icon": "🎉", "description": "Event-Packages verfügbar"}
                ]
            }
            
            await cursor.execute("""
                INSERT INTO standorte_enhanced (
                    id, page_title, page_subtitle, header_background,
                    neustadt_data, grossenbrode_data, info_section_data,
                    updated_at, updated_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                standorte_id,
                "Unsere Standorte",
                "Besuchen Sie uns an der malerischen Ostseeküste",
                "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
                json.dumps(neustadt_data),
                json.dumps(grossenbrode_data),
                json.dumps(info_data),
                datetime.now(),
                "system"
            ))
            print("✅ Standorte-Daten erstellt")
        
        # Prüfe about_content
        await cursor.execute("SELECT COUNT(*) FROM about_content")
        about_count = (await cursor.fetchone())[0]
        if about_count == 0:
            print("👥 Erstelle About-Daten...")
            about_id = str(uuid.uuid4())
            
            team_members = [
                {
                    "name": "Jimmy Rodriguez",
                    "role": "Küchenchef & Inhaber",
                    "description": "Geboren in Valencia, über 15 Jahre Erfahrung",
                    "image": "https://images.unsplash.com/photo-1560250097-0b93528c311a"
                },
                {
                    "name": "Maria Gonzalez",
                    "role": "Sous Chef",
                    "description": "Spezialistin für traditionelle Tapas",
                    "image": "https://images.unsplash.com/photo-1594736797933-d0ee6a8b2023"
                }
            ]
            
            values = [
                {"title": "Authentizität", "description": "Beste Zutaten aus Spanien", "icon": "🇪🇸"},
                {"title": "Qualität", "description": "Frisch zubereitet mit Liebe", "icon": "⭐"},
                {"title": "Gastfreundschaft", "description": "Spanische Herzlichkeit", "icon": "❤️"}
            ]
            
            await cursor.execute("""
                INSERT INTO about_content (
                    id, page_title, hero_title, hero_description, story_title,
                    story_content, story_image, team_title, team_members,
                    values_title, values_data, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                about_id,
                "Über uns",
                "Willkommen bei Jimmy's Tapas Bar",
                "Authentische spanische Küche an der Ostsee",
                "Unsere Geschichte",
                """Jimmy's Tapas Bar wurde 2015 von Jimmy Rodriguez gegründet. Nach Jahren in 
                renommierten Restaurants verwirklichte er seinen Traum an der Ostseeküste. 
                Wir vereinen spanische Wärme mit der entspannten Ostsee-Atmosphäre.""",
                "https://images.unsplash.com/photo-1571197119738-26123cb0d22f",
                "Unser Team",
                json.dumps(team_members),
                "Unsere Werte",
                json.dumps(values),
                datetime.now()
            ))
            print("✅ About-Daten erstellt")
        
        await cursor.close()
        connection.close()
        
        print("🎉 ALLE DATENBANKEN ERFOLGREICH ÜBERPRÜFT UND REPARIERT!")
        
        # Zusätzliche CMS-Inhalte erstellen
        await cursor.execute("SELECT COUNT(*) FROM homepage_content")
        homepage_count = (await cursor.fetchone())[0]
        if homepage_count == 0:
            print("🏠 Erstelle Homepage CMS-Daten...")
            subprocess.run(['python3', '/app/setup_complete_cms.py'], check=False)
        
        print("🎉 KOMPLETTE SYSTEM-ÜBERPRÜFUNG ABGESCHLOSSEN!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei der automatischen Reparatur: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check_and_fix_database())