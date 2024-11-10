from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.Benutzer_DropDown.items = anvil.server.call('get_all_users')
    selected_user = self.Benutzer_DropDown.selected_value
    self.room_drop_down.items = anvil.server.call('get_zimmer_with_preisklasse', selected_user)
  
  def Benutzer_DropDown_change(self, **event_args):
    selected_user = self.Benutzer_DropDown.selected_value
    self.room_drop_down.items = anvil.server.call('get_zimmer_with_preisklasse', selected_user)
