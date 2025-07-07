#!/usr/bin/env python3
import pymysql
import uuid
import os

def get_mysql_connection():
    try:
        return pymysql.connect(
            unix_socket='/run/mysqld/mysqld.sock',
            user='root',
            password='',
            database='jimmys_tapas_bar',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except:
        return pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='jimmys_tapas_bar',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

def import_complete_final_menu():
    """Importiert die vollständige Speisekarte mit allen Details"""
    
    # Vollständige Speisekarte mit detailed_description
    menu_items = [
        # 1. Inicio / Vorspeisen
        ("Aioli", "Knoblauchsauce mit Öl", "Hausgemachte Aioli mit frischem Knoblauch und bestem Olivenöl", "3,50", "Inicio / Vorspeisen", "Spanien", "Eier", "", "Traditionell gemixt", "Knoblauch, Olivenöl, Eigelb, Zitrone", 0, 1, 1, 1),
        ("Oliven", "Marinierte spanische Oliven", "Auswahl an grünen und schwarzen Oliven, traditionell mariniert", "3,90", "Inicio / Vorspeisen", "Spanien", "", "", "Traditionell mariniert", "Oliven, Olivenöl, Kräuter", 1, 1, 1, 2),
        ("Extra Brot", "Frisches Brot", "Hausgebackenes spanisches Brot, warm serviert", "1,90", "Inicio / Vorspeisen", "Spanien", "Gluten", "", "Frisch gebacken", "Mehl, Hefe, Salz, Olivenöl", 1, 1, 0, 3),
        ("Hummus", "Kichererbsen Cream", "Cremiger Hummus mit Tahini und Gewürzen", "3,90", "Inicio / Vorspeisen", "Mittelmeer", "Sesam", "", "Traditionell gemacht", "Kichererbsen, Tahini, Olivenöl, Knoblauch", 1, 1, 1, 4),
        ("Guacamole", "Avocado Cream", "Frische Avocado-Creme mit Limette und Koriander", "3,90", "Inicio / Vorspeisen", "Mexiko", "", "", "Frisch zubereitet", "Avocado, Limette, Koriander, Zwiebeln", 1, 1, 1, 5),
        ("Spanischer Käseteller", "Manchego", "Auswahl an spanischen Käsesorten mit Manchego", "8,90", "Inicio / Vorspeisen", "Spanien", "Milch", "", "Traditionell gereift", "Manchego, spanische Käse", 0, 1, 1, 6),
        ("Schinken-Käse-Wurst Teller", "Spanische Auswahl", "Auswahl spanischer Schinken, Käse und Würste", "11,90", "Inicio / Vorspeisen", "Spanien", "Milch", "", "Traditionell hergestellt", "Schinken, Käse, Chorizo", 0, 0, 1, 7),
        ("Jamón Serrano Teller", "Spanischer Schinken", "Hauchdünn geschnittener Jamón Serrano", "9,90", "Inicio / Vorspeisen", "Spanien", "", "", "Luftgetrocknet", "Jamón Serrano", 0, 0, 1, 8),
        ("Boquerones en Vinagre", "Mit Essig und Öl", "Eingelegte weiße Anchovis mit Essig und Olivenöl", "8,90", "Inicio / Vorspeisen", "Andalusien", "Fisch", "", "In Essig eingelegt", "Anchovis, Essig, Olivenöl", 0, 0, 1, 9),
        ("Pata Negra", "Spanischer Ibérico Schinken", "Edelster spanischer Ibérico-Schinken von Bellota-Schweinen", "8,90", "Inicio / Vorspeisen", "Extremadura", "", "", "36 Monate gereift", "Ibérico-Schinken", 0, 0, 1, 10),
        ("Tres", "Hummus, Avocado Cream, Aioli mit Brot", "Trio aus Hummus, Guacamole und Aioli mit frischem Brot", "10,90", "Inicio / Vorspeisen", "Spanien", "Eier, Sesam, Gluten", "", "Frisch zubereitet", "Hummus, Avocado, Aioli, Brot", 0, 1, 0, 11),

        # 2. Salate
        ("Ensalada Mixta", "Bunter Salat mit Essig und Öl", "Frischer gemischter Salat mit spanischem Dressing", "8,90", "Salate", "Spanien", "", "", "Frisch zubereitet", "Blattsalate, Tomaten, Gurken, Zwiebeln", 1, 1, 1, 12),
        ("Ensalada Tonno", "Bunter Salat mit Thunfisch", "Gemischter Salat mit hochwertigem Thunfisch", "14,90", "Salate", "Spanien", "Fisch", "", "Frisch zubereitet", "Salat, Thunfisch, Oliven, Ei", 0, 0, 1, 13),
        ("Ensalada Pollo", "Bunter Salat mit Hähnchenstreifen", "Frischer Salat mit gegrillten Hähnchenstreifen", "14,90", "Salate", "Spanien", "", "", "Frisch gegrillt", "Salat, Hähnchenbrust, Gemüse", 0, 0, 1, 14),
        ("Ensalada Garnelen", "Bunter Salat mit Garnelen", "Gemischter Salat mit frischen Garnelen", "15,90", "Salate", "Spanien", "Krustentiere", "", "Frisch zubereitet", "Salat, Garnelen, Avocado", 0, 0, 1, 15),
        ("Tomaten/Gurken Salat", "Mit Zwiebeln", "Einfacher Salat als Beilage", "6,90", "Salate", "Spanien", "", "", "Frisch geschnitten", "Tomaten, Gurken, Zwiebeln", 1, 1, 1, 16),
        ("Rote Beete Salat", "Mit Ziegenkäse", "Rote Beete mit Ziegenkäse und Walnüssen", "7,90", "Salate", "Spanien", "Milch, Nüsse", "", "Frisch zubereitet", "Rote Beete, Ziegenkäse, Walnüsse", 0, 1, 1, 17),
        ("Kichererbsen Salat", "Mit Feta", "Warmer Kichererbsensalat mit Fetakäse", "7,90", "Salate", "Mittelmeer", "Milch", "", "Warm serviert", "Kichererbsen, Feta, Kräuter", 0, 1, 1, 18),

        # 3. Tapa Paella
        ("Paella", "Mit Hähnchen und Meeresfrüchten", "Klassische Paella Mixta in Tapa-Größe", "8,90", "Tapa Paella", "Valencia", "Krustentiere, Weichtiere", "", "In der Paellera", "Bomba-Reis, Hähnchen, Garnelen, Safran", 0, 0, 1, 19),
        ("Paella Vegetarisch", "Ohne Fleisch und Fisch", "Vegetarische Paella mit saisonalem Gemüse", "7,90", "Tapa Paella", "Valencia", "", "", "In der Paellera", "Bomba-Reis, Gemüse, Safran, Olivenöl", 1, 1, 1, 20),

        # 4. Tapas Vegetarian
        ("Gebratenes Gemüse der Saison", "Vegan", "Saisonales Gemüse mediterran gebraten", "6,90", "Tapas Vegetarian", "Mittelmeer", "", "", "In der Pfanne gebraten", "Saisongemüse, Olivenöl, Kräuter", 1, 1, 1, 21),
        ("Papas Bravas", "Vegan", "Knusprige Kartoffeln mit pikanter Sauce", "6,90", "Tapas Vegetarian", "Madrid", "", "", "Frittiert", "Kartoffeln, Tomaten, Paprika", 1, 1, 1, 22),
        ("Tortilla de Patata", "Con Aioli", "Klassische spanische Tortilla mit Aioli", "6,90", "Tapas Vegetarian", "Spanien", "Eier", "", "Langsam gebraten", "Kartoffeln, Eier, Zwiebeln", 0, 1, 1, 23),
        ("Pimientos de Padrón", "Vegan", "Kleine grüne Paprika aus Galicien", "6,90", "Tapas Vegetarian", "Galicien", "", "", "Kurz gebraten", "Pimientos de Padrón, Meersalz", 1, 1, 1, 24),
        ("Kanarische Kartoffeln", "Im Salzmantel / Vegan", "Papas Arrugadas mit Mojo-Sauce", "6,90", "Tapas Vegetarian", "Kanarische Inseln", "", "", "Im Salzmantel gekocht", "Kartoffeln, Meersalz, Mojo", 1, 1, 1, 25),
        ("Fetakäse Häppchen", "Griechischer Feta", "Warme Fetakäse-Häppchen mit Honig", "6,90", "Tapas Vegetarian", "Griechenland", "Milch", "", "Im Ofen gebacken", "Feta, Honig, Kräuter", 0, 1, 1, 26),
        ("Rosmarin Ziegenkäse", "Mit frischem Rosmarin", "Ziegenkäse mit Rosmarin überbacken", "6,90", "Tapas Vegetarian", "Spanien", "Milch", "", "Überbacken", "Ziegenkäse, Rosmarin, Honig", 0, 1, 1, 27),
        ("Falafel", "Orientalische Kichererbsenbällchen", "Hausgemachte Falafel mit Tahini", "6,90", "Tapas Vegetarian", "Orient", "Sesam", "", "Frittiert", "Kichererbsen, Kräuter, Tahini", 1, 1, 1, 28),
        ("Feta Käse überbacken", "Cherry", "Überbackener Feta mit Kirschtomaten", "6,90", "Tapas Vegetarian", "Griechenland", "Milch", "", "Überbacken", "Feta, Kirschtomaten, Olivenöl", 0, 1, 1, 29),
        ("Überbackene Champignons", "Mit Käse gratiniert", "Champignons mit Käse überbacken", "6,90", "Tapas Vegetarian", "Spanien", "Milch", "", "Überbacken", "Champignons, Käse, Kräuter", 0, 1, 1, 30),
        ("Überbackene Tomaten", "Mit Käse", "Tomaten mit mediterranen Kräutern", "6,90", "Tapas Vegetarian", "Italien", "Milch", "", "Überbacken", "Tomaten, Mozzarella, Basilikum", 0, 1, 1, 31),
        ("Frittierte Auberginen", "Mit Honig", "Auberginen frittiert mit Honig", "6,90", "Tapas Vegetarian", "Andalusien", "", "", "Frittiert", "Auberginen, Honig, Meersalz", 1, 1, 1, 32),
        ("Champignons al Ajillo", "Vegan", "Champignons in Knoblauchöl", "6,90", "Tapas Vegetarian", "Spanien", "", "", "In Knoblauchöl", "Champignons, Knoblauch, Petersilie", 1, 1, 1, 33),
        ("Teigröllchen mit Spinat", "Gefüllte Teigtaschen", "Knusprige Röllchen mit Spinatfüllung", "6,90", "Tapas Vegetarian", "Spanien", "Gluten, Milch", "", "Frittiert", "Teig, Spinat, Ricotta", 0, 1, 0, 34),
        ("Feta Feigen", "Süße Feigen mit Feta", "Feta mit frischen Feigen und Honig", "6,90", "Tapas Vegetarian", "Mittelmeer", "Milch", "", "Frisch serviert", "Feta, Feigen, Honig", 0, 1, 1, 35),
        ("Ziegenkäse überbacken", "Gratinierter Ziegenkäse", "Überbackener Ziegenkäse mit Kräutern", "6,90", "Tapas Vegetarian", "Spanien", "Milch", "", "Überbacken", "Ziegenkäse, Kräuter, Olivenöl", 0, 1, 1, 36),
        ("Gebratener Spinat", "Mit Cherry Tomaten / Vegan", "Frischer Spinat mit Kirschtomaten", "6,90", "Tapas Vegetarian", "Spanien", "", "", "In der Pfanne", "Spinat, Kirschtomaten, Knoblauch", 1, 1, 1, 37),

        # 5. Tapas de Pollo
        ("Hähnchen Filet", "Mit Limetten Sauce", "Gegrillte Hähnchenbrust mit frischer Limettensauce", "7,20", "Tapas de Pollo", "Spanien", "", "", "Gegrillt", "Hähnchenbrust, Limette, Kräuter", 0, 0, 1, 38),
        ("Knusprige Hähnchen Tapas", "Mit Honig-Senf Sauce", "Panierte Hähnchenstücke mit Honig-Senf", "7,20", "Tapas de Pollo", "Spanien", "Gluten, Senf", "", "Knusprig gebraten", "Hähnchen, Honig, Senf", 0, 0, 0, 39),
        ("Hähnchen Spieß", "Mit scharfer Sauce", "Gegrillter Hähnchenspieß mit Chilisauce", "7,20", "Tapas de Pollo", "Spanien", "", "", "Gegrillt", "Hähnchen, Chili, Gewürze", 0, 0, 1, 40),
        ("Hähnchen Filet Curry", "Mit Curry Sauce", "Hähnchenbrust mit cremiger Currysauce", "7,20", "Tapas de Pollo", "Spanien", "Milch", "", "Gegrillt", "Hähnchen, Curry, Sahne", 0, 0, 1, 41),
        ("Hähnchen Filet Mandel", "Mit Mandel Sauce", "Hähnchenbrust mit traditioneller Mandelsauce", "7,20", "Tapas de Pollo", "Andalusien", "Nüsse", "", "Gegrillt", "Hähnchen, Mandeln, Kräuter", 0, 0, 1, 42),
        ("Hähnchen-Chorizo-Spieß", "Gegrillt", "Spieß aus Hähnchen und Chorizo", "7,20", "Tapas de Pollo", "Spanien", "", "", "Gegrillt", "Hähnchen, Chorizo, Paprika", 0, 0, 1, 43),
        ("Hähnchen Filet Brandy", "Mit Brandy Sauce", "Hähnchenbrust mit spanischer Brandy-Sauce", "7,20", "Tapas de Pollo", "Spanien", "", "", "Gegrillt", "Hähnchen, Brandy, Sahne", 0, 0, 1, 44),

        # 6. Tapas de Carne
        ("Dátiles con Bacon", "Datteln im Speckmantel", "Süße Datteln umhüllt von knusprigem Speck", "6,90", "Tapas de Carne", "Spanien", "", "", "Im Ofen gebacken", "Datteln, Speck", 0, 0, 1, 45),
        ("Albondigas a la Casera", "Hackbällchen mit Tomatensauce", "Hausgemachte Fleischbällchen in Tomatensauce", "6,90", "Tapas de Carne", "Spanien", "", "", "Geschmort", "Hackfleisch, Tomaten, Kräuter", 0, 0, 1, 46),
        ("Pincho de Cerdo", "Schweinespieß scharf", "Würziger Schweinefleischspieß mit Chili", "7,90", "Tapas de Carne", "Spanien", "", "", "Gegrillt", "Schweinefleisch, Chili, Gewürze", 0, 0, 1, 47),
        ("Pincho de Cordero", "Lammspieß scharf", "Zarter Lammspieß mit scharfen Gewürzen", "8,90", "Tapas de Carne", "Spanien", "", "", "Gegrillt", "Lammfleisch, Gewürze, Kräuter", 0, 0, 1, 48),
        ("Chuletas de Cordero", "2 Lammkoteletts", "Zwei zarte Lammkoteletts rosa gebraten", "9,90", "Tapas de Carne", "Kastilien", "", "", "Gegrillt", "Lammkoteletts, Rosmarin, Knoblauch", 0, 0, 1, 49),
        ("Rollitos de Serrano", "Feigen/Serrano, Frischkäse", "Serrano-Röllchen mit Feigen und Frischkäse", "9,90", "Tapas de Carne", "Spanien", "Milch", "", "Frisch gerollt", "Serrano, Feigen, Frischkäse", 0, 0, 1, 50),
        ("Queso de Cabra con Bacon", "Ziegenkäse/Speck", "Ziegenkäse umhüllt mit knusprigem Speck", "7,90", "Tapas de Carne", "Spanien", "Milch", "", "Überbacken", "Ziegenkäse, Speck", 0, 0, 1, 51),
        ("Chorizo al Diablo", "In Rotweinsauce", "Chorizo in feuriger Rotweinsauce", "7,90", "Tapas de Carne", "Spanien", "Sulfite", "", "Geschmort", "Chorizo, Rotwein, Chili", 0, 0, 1, 52),
        ("Medallions de Carne", "Rinderfilet, Pilz-Ragout", "Rinderfiletmedaillons mit Pilzragout", "9,90", "Tapas de Carne", "Spanien", "", "", "Rosa gebraten", "Rinderfilet, Champignons, Sahne", 0, 0, 1, 53),
        ("Champignons mit Käse", "Bacon, Kräuter", "Champignons gefüllt mit Käse und Speck", "8,90", "Tapas de Carne", "Spanien", "Milch", "", "Überbacken", "Champignons, Käse, Speck", 0, 0, 1, 54),
        ("Schweinefilet Cherry", "Mit Cherry Tomaten, Mango-Honig", "Schweinefilet mit Mango-Honig-Glasur", "9,50", "Tapas de Carne", "Spanien", "", "", "Gegrillt", "Schweinefilet, Mango, Honig", 0, 0, 1, 55),
        ("Schweinefilet Spinat", "Spinat, Pilze, Cremefraiche", "Schweinefilet mit Spinat-Pilz-Sauce", "9,50", "Tapas de Carne", "Spanien", "Milch", "", "Gegrillt", "Schweinefilet, Spinat, Pilze", 0, 0, 1, 56),
        ("Chorizo a la Plancha", "Gegrillt", "Gegrillte Chorizo-Scheiben", "7,90", "Tapas de Carne", "Spanien", "", "", "Gegrillt", "Chorizo, Olivenöl", 0, 0, 1, 57),
        ("Lammfilet", "Mit Pfeffersauce", "Zartes Lammfilet mit grüner Pfeffersauce", "9,90", "Tapas de Carne", "Spanien", "Milch", "", "Rosa gebraten", "Lammfilet, grüner Pfeffer, Sahne", 0, 0, 1, 58),
        ("Spareribs", "Mit BBQ-Sauce", "Zarte Spareribs mit BBQ-Glasur", "9,90", "Tapas de Carne", "USA", "", "", "Langsam gegrillt", "Schweinerippen, BBQ-Sauce", 0, 0, 1, 59),
        ("Chicken Wings", "Mit süßer Chillisauce", "Knusprige Chicken Wings mit süß-scharfer Sauce", "9,90", "Tapas de Carne", "USA", "", "", "Frittiert", "Hähnchenflügel, Sweet Chili", 0, 0, 1, 60),

        # 7. Tapas de Pescado
        ("Boquerones Fritos", "Frittierte Sardellen", "Knusprig frittierte kleine Sardellen", "7,50", "Tapas de Pescado", "Andalusien", "Fisch", "", "Frittiert", "Sardellen, Mehl, Olivenöl", 0, 0, 1, 61),
        ("Calamares a la Plancha", "Gegrillt", "Gegrillte Tintenfischringe mit Knoblauch", "8,90", "Tapas de Pescado", "Spanien", "Weichtiere", "", "Gegrillt", "Tintenfisch, Knoblauch, Petersilie", 0, 0, 1, 62),
        ("Calamares a la Romana", "Frittiert mit Aioli", "Panierte Tintenfischringe mit Aioli", "7,50", "Tapas de Pescado", "Spanien", "Weichtiere, Eier", "", "Frittiert", "Tintenfisch, Mehl, Aioli", 0, 0, 1, 63),
        ("Salmon con Espinaca", "Lachsfilet auf Spinat", "Gegrillter Lachs auf Spinatbett", "9,90", "Tapas de Pescado", "Norwegen", "Fisch", "", "Gegrillt", "Lachs, Spinat, Knoblauch", 0, 0, 1, 64),
        ("Gambas a la Plancha", "Gegrillte Tiger-Garnelen, Gemüse", "Große Garnelen mit Gemüse gegrillt", "9,90", "Tapas de Pescado", "Spanien", "Krustentiere", "", "Gegrillt", "Tiger-Garnelen, Paprika, Zwiebeln", 0, 0, 1, 65),
        ("Garnelen-Dattel-Spieß", "Speckmantel, Honig-Senf", "Garnelen und Datteln im Speckmantel", "9,90", "Tapas de Pescado", "Spanien", "Krustentiere, Senf", "", "Gegrillt", "Garnelen, Datteln, Speck", 0, 0, 1, 66),
        ("Gambas al Ajillo", "Knoblauch-Olivenöl", "Klassische Knoblauchgarnelen", "9,90", "Tapas de Pescado", "Andalusien", "Krustentiere", "", "In Knoblauchöl", "Garnelen, Knoblauch, Petersilie", 0, 0, 1, 67),
        ("Muslitos de Mar", "Krebsfleischbällchen", "Hausgemachte Krebsfleischbällchen", "6,90", "Tapas de Pescado", "Spanien", "Krustentiere, Eier", "", "Frittiert", "Krebsfleisch, Ei, Zwiebeln", 0, 0, 1, 68),
        ("Gegrillter Oktopus", "Kichererbsen, Gemüse", "Oktopus mit Kichererbsen und Gemüse", "9,90", "Tapas de Pescado", "Galicien", "Weichtiere", "", "Gegrillt", "Oktopus, Kichererbsen, Paprika", 0, 0, 1, 69),
        ("Jacobsmuscheln", "Spinat, Cherry Tomaten", "Gebratene Jakobsmuscheln auf Spinat", "9,90", "Tapas de Pescado", "Galicien", "Weichtiere", "", "Gebraten", "Jakobsmuscheln, Spinat, Tomaten", 0, 0, 1, 70),
        ("Gambas PIL PIL", "Scharfe Tomatensauce", "Garnelen in pikanter Tomatensauce", "9,90", "Tapas de Pescado", "Baskenland", "Krustentiere", "", "Geschmort", "Garnelen, Tomaten, Chili", 0, 0, 1, 71),
        ("Empanadas", "Thunfisch, gefüllter Teig", "Gefüllte Teigtaschen mit Thunfisch", "6,90", "Tapas de Pescado", "Galicien", "Fisch, Gluten, Eier", "", "Gebacken", "Teig, Thunfisch, Zwiebeln", 0, 0, 0, 72),
        ("Pfahlmuscheln", "Nach spanischer Art", "Pfahlmuscheln in Weißweinsud", "8,90", "Tapas de Pescado", "Galicien", "Weichtiere, Sulfite", "", "Gedämpft", "Pfahlmuscheln, Weißwein, Knoblauch", 0, 0, 1, 73),
        ("Pulpo al Ajillo", "Oktopus, Knoblauch", "Oktopus in Knoblauchöl mit Paprika", "9,90", "Tapas de Pescado", "Galicien", "Weichtiere", "", "In Knoblauchöl", "Oktopus, Knoblauch, Paprikapulver", 0, 0, 1, 74),
        ("Zander Filet", "Bacon, Knoblauch-Sahnesauce", "Zanderfilet mit Speck und Knoblauchsauce", "9,90", "Tapas de Pescado", "Deutschland", "Fisch, Milch", "", "Gebraten", "Zander, Speck, Sahne", 0, 0, 1, 75),
        ("Tiger Garnelen", "Tomaten, Paprika, Knoblauch, Oliven", "Große Garnelen mit mediterranem Gemüse", "9,90", "Tapas de Pescado", "Spanien", "Krustentiere", "", "Geschmort", "Garnelen, Tomaten, Paprika", 0, 0, 1, 76),
        ("Brocheta de Gambas", "Gambas Spieß", "Garnelenspieß mit Kräutern", "8,90", "Tapas de Pescado", "Spanien", "Krustentiere", "", "Gegrillt", "Garnelen, Kräuter, Olivenöl", 0, 0, 1, 77),
        ("Boqueron en Tempura", "Panierte Sardellen", "Sardellen im Tempurateig", "7,50", "Tapas de Pescado", "Japan/Spanien", "Fisch, Gluten", "", "Frittiert", "Sardellen, Tempurateig", 0, 0, 0, 78),
        ("Chipirones Fritos", "Con Aioli", "Kleine Tintenfische frittiert mit Aioli", "8,90", "Tapas de Pescado", "Spanien", "Weichtiere, Eier", "", "Frittiert", "Baby-Tintenfisch, Aioli", 0, 0, 1, 79),

        # 8. Kroketten
        ("Croquetas de Bacalao", "Stockfisch", "Kroketten mit Stockfisch-Füllung", "5,90", "Kroketten", "Spanien", "Fisch, Gluten, Milch", "", "Frittiert", "Stockfisch, Bechamel, Paniermehl", 0, 0, 0, 80),
        ("Croquetas de Queso", "Fetakäse", "Käsekroketten mit cremiger Füllung", "5,90", "Kroketten", "Spanien", "Milch, Gluten", "", "Frittiert", "Feta, Bechamel, Paniermehl", 0, 1, 0, 81),
        ("Croquetas de Almendras", "Mandeln", "Kroketten mit Mandelfüllung", "6,50", "Kroketten", "Spanien", "Nüsse, Gluten, Milch", "", "Frittiert", "Mandeln, Bechamel, Paniermehl", 0, 1, 0, 82),
        ("Croquetas de Jamón", "Serrano Schinken", "Klassische Schinkenkroketten", "5,90", "Kroketten", "Spanien", "Gluten, Milch", "", "Frittiert", "Serrano, Bechamel, Paniermehl", 0, 0, 0, 83),
        ("Croquetas de Patata", "Kartoffel", "Vegetarische Kartoffelkroketten", "5,50", "Kroketten", "Spanien", "Gluten, Milch", "", "Frittiert", "Kartoffeln, Bechamel, Paniermehl", 0, 1, 0, 84),

        # 9. Pasta
        ("Spaghetti Aglio e Olio", "Mit Knoblauch und Olivenöl", "Klassische italienische Pasta", "12,90", "Pasta", "Italien", "Gluten", "", "Al dente gekocht", "Spaghetti, Knoblauch, Olivenöl", 1, 1, 0, 85),
        ("Spaghetti Bolognese", "Mit Fleischsauce", "Traditionelle Bolognese-Sauce", "14,90", "Pasta", "Italien", "Gluten", "", "Langsam geschmort", "Spaghetti, Hackfleisch, Tomaten", 0, 0, 0, 86),
        ("Pasta Brokkoli Gorgonzola", "Mit Käsesauce", "Pasta mit Brokkoli und Gorgonzola", "14,90", "Pasta", "Italien", "Gluten, Milch", "", "Cremig geschmort", "Pasta, Brokkoli, Gorgonzola", 0, 1, 0, 87),
        ("Pasta Verdura", "Mit Gemüse", "Pasta mit saisonalem Gemüse", "14,90", "Pasta", "Italien", "Gluten", "", "Frisch gebraten", "Pasta, Saisongemüse, Kräuter", 1, 1, 0, 88),
        ("Pasta Garnelen", "Mit Garnelen", "Pasta mit frischen Garnelen", "16,90", "Pasta", "Italien", "Gluten, Krustentiere", "", "Al dente", "Pasta, Garnelen, Knoblauch", 0, 0, 0, 89),

        # 10. Pizza
        ("Pizza Margharita", "Klassische Pizza", "Mit Tomaten, Mozzarella und Basilikum", "9,90", "Pizza", "Italien", "Gluten, Milch", "", "Im Steinofen", "Teig, Tomaten, Mozzarella", 0, 1, 0, 90),
        ("Pizza Schinken", "Mit Schinken", "Margharita mit Schinken", "12,90", "Pizza", "Italien", "Gluten, Milch", "", "Im Steinofen", "Teig, Tomaten, Mozzarella, Schinken", 0, 0, 0, 91),
        ("Pizza Funghi", "Mit Champignons", "Margharita mit frischen Champignons", "12,90", "Pizza", "Italien", "Gluten, Milch", "", "Im Steinofen", "Teig, Mozzarella, Champignons", 0, 1, 0, 92),
        ("Pizza Tonno", "Mit Thunfisch", "Pizza mit Thunfisch und Zwiebeln", "13,90", "Pizza", "Italien", "Gluten, Milch, Fisch", "", "Im Steinofen", "Teig, Mozzarella, Thunfisch", 0, 0, 0, 93),
        ("Pizza Hawaii", "Mit Ananas und Schinken", "Umstrittene aber beliebte Kombination", "13,90", "Pizza", "Italien", "Gluten, Milch", "", "Im Steinofen", "Teig, Schinken, Ananas", 0, 0, 0, 94),
        ("Pizza Verdura", "Mit Gemüse", "Vegetarische Pizza mit Gemüse", "13,90", "Pizza", "Italien", "Gluten, Milch", "", "Im Steinofen", "Teig, Gemüse, Mozzarella", 0, 1, 0, 95),
        ("Pizza Salami", "Mit Salami", "Klassische Salami-Pizza", "12,90", "Pizza", "Italien", "Gluten, Milch", "", "Im Steinofen", "Teig, Salami, Mozzarella", 0, 0, 0, 96),
        ("Pizza Garnelen", "Mit Garnelen", "Pizza mit frischen Garnelen", "15,90", "Pizza", "Italien", "Gluten, Milch, Krustentiere", "", "Im Steinofen", "Teig, Garnelen, Knoblauch", 0, 0, 0, 97),
        ("Pizza Bolognese", "Mit Fleischsauce", "Pizza mit Bolognese-Sauce", "13,90", "Pizza", "Italien", "Gluten, Milch", "", "Im Steinofen", "Teig, Bolognese, Mozzarella", 0, 0, 0, 98),
        ("Jimmy's Special Pizza", "Hausspezialität", "Pizza nach Art des Hauses", "13,90", "Pizza", "Jimmy's", "Gluten, Milch", "", "Im Steinofen", "Teig, Spezialmischung", 0, 0, 0, 99),

        # 11. Für den kleinen und großen Hunger
        ("Pommes Frites", "Mit Ketchup/Mayonnaise", "Knusprige Pommes mit Sauces", "5,50", "Für den kleinen und großen Hunger", "Belgien", "", "", "Frittiert", "Kartoffeln, Sonnenblumenöl", 1, 1, 1, 100),
        ("Chicken Nuggets", "5 Stück, Pommes", "Knusprige Chicken Nuggets mit Pommes", "8,90", "Für den kleinen und großen Hunger", "USA", "Gluten", "", "Frittiert", "Hähnchenbrustfleisch, Panade", 0, 0, 0, 101),
        ("Chicken Wings", "5 Stück, Pommes", "Chicken Wings mit Pommes", "9,90", "Für den kleinen und großen Hunger", "USA", "", "", "Frittiert", "Hähnchenflügel, Gewürze", 0, 0, 1, 102),
        ("Currywurst", "Mit Pommes", "Currywurst mit Pommes", "10,90", "Für den kleinen und großen Hunger", "Deutschland", "Gluten", "", "Gebraten", "Bratwurst, Currysauce, Pommes", 0, 0, 0, 103),

        # 12. Dessert & Eis
        ("Crema Catalana", "Spanische Crème brûlée", "Traditionelles katalanisches Dessert", "5,50", "Dessert & Eis", "Katalonien", "Milch, Eier", "", "Gebrannt", "Milch, Eigelb, Zucker, Zimt", 0, 1, 1, 104),
        ("Tarte de Santiago", "Mandelkuchen aus Galicien", "Traditioneller galizischer Mandelkuchen", "7,50", "Dessert & Eis", "Galicien", "Nüsse, Eier", "", "Gebacken", "Mandeln, Eier, Zucker", 0, 1, 1, 105),
        ("Gemischtes Eis", "3 Kugeln, Sahne", "Auswahl an Eissorten mit Sahne", "6,90", "Dessert & Eis", "Italien", "Milch", "", "Gekühlt serviert", "Milch, Sahne, verschiedene Sorten", 0, 1, 1, 106),
        ("Churros", "Mit Schokolade", "Spanische Spritzgebäck mit Schokolade", "6,90", "Dessert & Eis", "Spanien", "Gluten, Milch", "", "Frittiert", "Mehl, Schokolade, Zucker", 0, 1, 0, 107),
        ("Schoko Soufflé", "Eis, Sahne", "Warmes Schokoladensoufflé mit Eis", "7,50", "Dessert & Eis", "Frankreich", "Milch, Eier", "", "Im Ofen gebacken", "Schokolade, Eier, Sahne", 0, 1, 1, 108),
        ("Kokos-Eis", "In Fruchtschale", "Kokoseis in echter Kokosnuss", "6,90", "Dessert & Eis", "Tropen", "Milch", "", "Gekühlt", "Kokosmilch, Sahne", 0, 1, 1, 109),
        ("Zitronen-Eis", "In Fruchtschale", "Zitroneneis in ausgehöhlter Zitrone", "6,90", "Dessert & Eis", "Italien", "Milch", "", "Gekühlt", "Zitronen, Milch, Zucker", 0, 1, 1, 110),
        ("Orangen-Eis", "In Fruchtschale", "Orangeneis in ausgehöhlter Orange", "6,90", "Dessert & Eis", "Spanien", "Milch", "", "Gekühlt", "Orangen, Milch, Zucker", 0, 1, 1, 111),
        ("Nuss-Eis", "In Fruchtschale", "Nusseis in dekorativer Fruchtschale", "6,90", "Dessert & Eis", "Italien", "Milch, Nüsse", "", "Gekühlt", "Nüsse, Milch, Sahne", 0, 1, 1, 112),

        # Getränke folgen...
        # 13. Heißgetränke & Tee
        ("Café Crema", "Milder Kaffee", "Klassischer Café Crema", "3,60", "Heißgetränke & Tee", "Deutschland", "", "", "Frisch gebrüht", "Kaffeebohnen", 1, 1, 1, 150),
        ("Cappuccino", "Espresso mit Milchschaum", "Italienischer Cappuccino", "3,60", "Heißgetränke & Tee", "Italien", "Milch", "", "Frisch zubereitet", "Espresso, Milch", 0, 1, 1, 151),
        ("Espresso", "Starker italienischer Kaffee", "Klassischer Espresso", "2,80", "Heißgetränke & Tee", "Italien", "", "", "Unter Druck", "Kaffeebohnen", 1, 1, 1, 152),
        ("Latte Macchiato", "Geschichteter Milchkaffee", "Italienischer Latte Macchiato", "3,90", "Heißgetränke & Tee", "Italien", "Milch", "", "Geschichtet", "Espresso, Milch", 0, 1, 1, 153),
        ("Heiße Schokolade", "Mit Sahne", "Heiße Schokolade mit Sahnehaube", "3,90", "Heißgetränke & Tee", "Spanien", "Milch", "", "Heiß gerührt", "Schokolade, Milch, Sahne", 0, 1, 1, 154),

        # 14. Softdrinks
        ("Coca Cola", "0,3 l", "Erfrischende Cola", "3,90", "Softdrinks", "USA", "", "", "Gekühlt", "Cola", 1, 1, 1, 200),
        ("Coca Cola Zero", "0,3 l", "Zuckerfreie Cola", "3,90", "Softdrinks", "USA", "", "", "Gekühlt", "Cola", 1, 1, 1, 201),
        ("Wasser Magnus", "Kohlensäure 0,25 l", "Sprudelwasser", "2,90", "Softdrinks", "Deutschland", "", "", "Gekühlt", "Mineralwasser", 1, 1, 1, 202),
        ("Wasser Magnus still", "0,25 l", "Stilles Wasser", "2,90", "Softdrinks", "Deutschland", "", "", "Gekühlt", "Mineralwasser", 1, 1, 1, 203),
        ("Apfelsaft", "0,3 l", "Naturtrüber Apfelsaft", "3,90", "Softdrinks", "Deutschland", "", "", "Gekühlt", "Äpfel", 1, 1, 1, 204),

        # 15. Spanische Getränke
        ("Sangria Tinto", "Rotwein-Sangria", "Spanische Sangria mit Rotwein und Früchten", "5,50", "Spanische Getränke", "Spanien", "Sulfite", "", "Traditionell", "Rotwein, Früchte", 1, 1, 1, 250),
        ("Rioja Wein", "0,2 l", "Spanischer Rotwein aus der Rioja", "7,50", "Spanische Getränke", "Spanien", "Sulfite", "", "Gekühlt", "Rotwein", 1, 1, 1, 251),
        ("Cava Sekt", "Spanischer Schaumwein", "Katalanischer Cava", "6,90", "Spanische Getränke", "Spanien", "Sulfite", "", "Gekühlt", "Schaumwein", 1, 1, 1, 252),
    ]
    
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        
        # Lösche alle existierenden Artikel
        print("🗑️ Lösche alte Menü-Artikel...")
        cursor.execute("DELETE FROM menu_items")
        
        # Importiere neue Artikel mit vollständigen Details
        print("📥 Importiere vollständige Speisekarte...")
        imported_count = 0
        
        for item in menu_items:
            try:
                cursor.execute("""
                    INSERT INTO menu_items (
                        id, name, description, detailed_description, price, category, 
                        origin, allergens, additives, preparation_method, ingredients, 
                        vegan, vegetarian, glutenfree, order_index, is_active
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(uuid.uuid4()),
                    item[0],  # name
                    item[1],  # description
                    item[2],  # detailed_description
                    item[3],  # price
                    item[4],  # category
                    item[5],  # origin
                    item[6],  # allergens
                    item[7],  # additives
                    item[8],  # preparation_method
                    item[9],  # ingredients
                    item[10], # vegan
                    item[11], # vegetarian
                    item[12], # glutenfree
                    item[13], # order_index
                    True      # is_active
                ))
                imported_count += 1
                
            except Exception as e:
                print(f"❌ Fehler bei {item[0]}: {e}")
                continue
        
        conn.commit()
        print(f"✅ {imported_count} Menü-Artikel erfolgreich importiert!")
        return imported_count
        
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")
        return 0
    finally:
        conn.close()

if __name__ == "__main__":
    print("🍽️ Importiere finale komplette Speisekarte mit allen Details...")
    count = import_complete_final_menu()
    print(f"🎉 Import abgeschlossen: {count} Artikel in MySQL-Datenbank!")