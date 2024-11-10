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
    self.buchungen_drop_down.items = anvil.server.call('get_all_bookings')
  
  def Benutzer_DropDown_change(self, **event_args):
    selected_user = self.Benutzer_DropDown.selected_value
    self.room_drop_down.items = anvil.server.call('get_zimmer_with_preisklasse', selected_user)

  def button_1_click(self, **event_args):
    selected_user = self.Benutzer_DropDown.selected_value  
    selected_room = self.room_drop_down.selected_value  
    start_date = self.start_date_picker.date
    end_date = self.end_date_picker.date
    
    if selected_user and selected_room and start_date and end_date:
        result = anvil.server.call('add_booking', selected_room, selected_user, start_date, end_date)
        alert(result)
        self.buchungen_drop_down.items = anvil.server.call('get_all_bookings')
    else:
        alert("Bitte wählen Sie alle erforderlichen Felder aus.")


