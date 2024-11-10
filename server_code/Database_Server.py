import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3 

@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  return 42

@anvil.server.callable
# def get_jugendherberge():
#     # Read the contents of a file
    
#     conn = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
#     cuursor = conn.cursor()
#     res = list(cuursor.execute("SELECT name, JID FROM jugendherbergen"))
#     print(res)
#     return res
def get_all_users():
    conn = sqlite3.connect(data_files['jugendherberge.db'])
    cursor = conn.cursor()
    
    res = [(f"{row[0]} {row[1]}", row[2]) for row in cursor.execute("SELECT Vorname, Nachname, BenutzerID FROM Benutzer")]
    
    conn.close()
    
    return res
@anvil.server.callable
def get_zimmer_with_preisklasse(benutzer_id):
    conn = sqlite3.connect(data_files['jugendherberge.db'])
    cursor = conn.cursor()
    query = """
    SELECT pk.KategorieName, z.ZimmerNummer
    FROM Benutzer b
    JOIN PreisKategorie pk ON b.PreisKategorieID = pk.PreisKategorieID
    JOIN Zimmer z ON pk.PreisKategorieID = z.PreisKategorieID
    WHERE b.BenutzerID = ?
    """
    cursor.execute(query, (benutzer_id,))
    res = cursor.fetchall()
    conn.close()
    result_strings = [f"Preisklasse: {row[0]}, Zimmernummer: {row[1]}" for row in res]
    print(result_strings)
    return result_strings
    result_strings = [f"Preisklasse: {row[0]}, Zimmernummer: {row[1]}" for row in res]
    return "\n".join(result_strings)

@anvil.server.callable
def add_booking(zimmer_nummer, benutzer_id, startdatum, enddatum):
    conn = sqlite3.connect(data_files['jugendherberge.db'])
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Buchung (ZimmerNummer, BenutzerID, Startdatum, Enddatum)
    VALUES (?, ?, ?, ?)
    ''', (zimmer_nummer, benutzer_id, startdatum, enddatum))
    
    conn.commit()
    conn.close()
    print((zimmer_nummer, benutzer_id, startdatum, enddatum))
    return "Buchung erfolgreich hinzugefügt."




@anvil.server.callable
def get_zimmer():
    conn = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
    cuursor = conn.cursor()
    res = list(cuursor.execute("SELECT CAST(bettenanZahl AS TEXT), ZID FROM zimmer"))
    
    print(res)
    
    return res

  
@anvil.server.callable
def get_all_bookings():
    conn = sqlite3.connect(data_files['jugendherberge.db'])
    cursor = conn.cursor()
    
    query = """
    SELECT b.BuchungID, z.ZimmerNummer, u.Vorname, u.Nachname, b.Startdatum, b.Enddatum
    FROM Buchung b
    JOIN Zimmer z ON b.ZimmerNummer = z.ZimmerNummer
    JOIN Benutzer u ON b.BenutzerID = u.BenutzerID
    """
    cursor.execute(query)
    res = cursor.fetchall()
    
    conn.close()
    
    result_strings = [f"BuchungID: {row[0]}, Zimmer: {row[1]}, Name: {row[2]} {row[3]}, Startdatum: {row[4]}, Enddatum: {row[5]}" for row in res]
    print(result_strings)
    return result_strings