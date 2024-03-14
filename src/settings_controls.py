from kivy.utils import platform
import json
from pathlib import Path

def increase_radius(self):
        """Erhöht den Radius."""
        #Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        if int(self.radius_widget.text) + 10 > 100000:
                return
        #Erhöhen des aktuellen Wertes um 10
        self.radius_widget.text = str(int(self.radius_widget.text) + 10)

def decrease_radius(self):
        """Reduziert den Radius."""
        # Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        if int(self.radius_widget.text) - 10 < 10:
                return
        # Verringere den aktuellen Wert um 10
        self.radius_widget.text = str(int(self.radius_widget.text) - 10)

def settings_error(self):
        """Prüfen der Usereingabe im Textfeld bei on_error"""
        self.radius_widget = self.root.ids.radius

        if self.radius_widget == None:
                return
        
        if len(self.radius_widget.text) > 6:
               self.radius_widget.text = "100000"
               return
        
        if int(self.radius_widget.text) < 10:
                self.radius_widget.text = "10"
                return     

def check_input(self):
        """Prüft Usereingabe im Textfeld, sodass keine Null und Werte kleiner 0
        eingegeben werden können"""
        self.radius_widget = self.root.ids.radius

        if self.radius_widget.text == '':
                self.radius_widget.text = "10"

        if len(self.radius_widget.text) < 2:
                self.radius_widget.text = "10"
                return
        
def write_to_file(self):
        """Schreibt den Radius und ausgewählten Sound in daten.json."""
        self.radius_widget = self.root.ids.radius.text
        self.spinner_widget = self.root.ids.sound_spinner.text

        if platform == 'android':
            pfad = Path(__file__).resolve().parent
            data_dir = pfad / 'src/json/daten.json'
            #data_dir = MainApp().user_data_dir
            dictionary = {
            "Bereich": "Einstellungen",
            "Radius": self.radius_widget,
            'Audio Data': self.spinner_widget
            }
            with open (data_dir, "w") as file:
                json.dump(dictionary,file)
        elif platform == 'win':
            dictionary = {
            "Bereich": "Einstellungen",
            "Radius": self.radius_widget,
            'Audio Data': self.spinner_widget
            }
            with open ("src/json/daten.json", "w") as file:
                json.dump(dictionary,file)

def load_settings(self):
        """Lädt den Radius und ausgewählten Sound aus daten.json."""
        if platform == 'android':
            pfad = Path(__file__).resolve().parent
            data_dir = pfad / 'json/daten.json'
            
            #data_dir = MainApp().user_data_dir + "/daten.json"
        elif platform == 'win':
            pfad = Path(__file__).resolve().parent
            data_dir = pfad / 'json/daten.json'
            #data_dir = "src/json/daten.json"

        f = open(data_dir)
        data = json.load(f)
        self.root.ids.radius.text = data['Radius']
        self.root.ids.sound_spinner.text = data['Audio Data']
        f.close()