import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3 

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  return 42

@anvil.server.callable
def get_jugendherberge():
    # Read the contents of a file
    
    conn = sqlite3.connect(data_files["jugendherbergen_verwaltung.db"])
    cuursor = conn.cursor()
    res = list(cuursor.execute("SELECT name, JID FROM jugendherbergen"))
    print(res)
    return res

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