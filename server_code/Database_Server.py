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
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(data_files['jugendherberge.db'])
    cursor = conn.cursor()
    
    # Benutzer abfragen und Ergebnisse formatieren
    res = [(f"{row[0]} {row[1]}", row[2]) for row in cursor.execute("SELECT Vorname, Nachname, BenutzerID FROM Benutzer")]
    
    # Verbindung schließen
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


    
    # Ergebnis als formatierte Strings zurückgeben
    result_strings = [f"Preisklasse: {row[0]}, Zimmernummer: {row[1]}" for row in res]
    return "\n".join(result_strings)




@anvil.server.callable
def get_zimmer():
    conn = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
    cuursor = conn.cursor()
    res = list(cuursor.execute("SELECT CAST(bettenanZahl AS TEXT), ZID FROM zimmer"))
    
    print(res)
    
    return res


@anvil.server.callable
def get_zimmer_jugendherberge():
    conn = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
    cuursor = conn.cursor()
    res = list(cuursor.execute('''
    SELECT z.ZID, z.bettenanZahl, j.name
    FROM zimmer z
    JOIN jugendherbergen j ON z.herbergeFK = j.JID'''))

    print(res)