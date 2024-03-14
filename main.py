"""Programm für Ankeralarm-App"""

import os
import json
import math
from pathlib import Path
from random import random

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Line, Color
from kivy.core.audio import SoundLoader
from kivy_garden.mapview import MapMarker

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout

import src.ankeralarm_gps as gps
import src.settings_controls as sc
import src.d_pad as d_pad

class MainApp(MDApp):
    """Hauptklasse der Anwendung."""
    def __init__(self, **kwargs):
        """Initialisiert die Anwendung."""
        self.title = "Ankeralarm"
        super().__init__(**kwargs)
        self.marker = False
        self.dialog = None
        self.is_program_stopped = True
        self.use_once = True
        self.is_anchor_visible = True
        Clock.schedule_once(self.get_permission, 0)
        os.environ["SDL_AUDIODRIVER"] = "android"

    def build(self):
        screen = Builder.load_file("windowsmd.kv")
        self.theme_cls.theme_style = "Dark"
        Clock.schedule_once(self.class_that_does_everything, 1)
        return screen
    
    #region GPS
    def get_permission(self, dt):
        """Holt Berechtigung für GPS"""
        # if platform == 'android':
        #     from android.permissions import Permission, request_permissions
        #     permissions = [Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]
        #     request_permissions(permissions, self.permission_callback)
        #     return True
        
        # return False
        gps.get_permission(self, dt)

    def permission_callback(self, permissions, results):
        """Callback-Funktion für Berechtigungen."""
        if all(results):
            print("Rechte erteilt")
            self.get_gps()
        else:
            print("Rechte abgelehnt")

    def get_gps(self, *args):
        """Holt GPS-Daten mithilfe von plyer"""
        if platform == 'android':
            from plyer import gps   
            try:                           
                gps.configure(on_location=self.on_location)
                gps.start(minTime=100, minDistance=0)
            except:
                import traceback
                traceback.print_exc()
                self.gps_status= "GPS is not implemented for your platform"

    def on_location(self, **kwargs):
        """Holt lat und lon Werte des aktuellen Standorts. 
        Zudem fügt es diese beim Start der Mapview hinzu."""
        self.gps_latitude = kwargs.get('lat', None) 
        self.gps_longitude = kwargs.get('lon', None)
        if hasattr(self,'gps_latitude') and hasattr(self,'gps_longitude'):
            if self.use_once:
                if  self.root.ids.mapview.lat and self.root.ids.mapview.lon:
                    self.root.ids.mapview.lat = self.gps_latitude
                    self.root.ids.mapview.lon = self.gps_longitude
                    self.center_map(self.gps_latitude, self.gps_longitude)
                    self.use_once = False
            self.update_boat()
    #endregion
    
    def toggle_program(self):
        """Startet oder stoppt das Programm."""
        if self.is_program_stopped:
            self.draw_circle()
            self.root.ids.launchButton.text = "Stop"
            self.is_program_stopped = False
            return
        if not self.is_program_stopped:
            self.stop_update_circle()
            self.root.ids.launchButton.text = "Start"
            self.is_program_stopped = True
            return

    def add_marker(self):
        """Fügt einen Marker hinzu."""
        if self.marker:
            return

        self.marker_anchor = MapMarker(lat=self.marker_boat.lat, 
                                       lon=self.marker_boat.lon, 
                                       source='src/images/anchor_32.png')
        self.root.ids.mapview.add_widget(self.marker_anchor)

        self.marker = True

    def update_boat(self):
        """Aktualisiert den aktuellen Standort."""
        if platform == 'win':
            self.marker_boat.lat = 50.0
            self.marker_boat.lon = 8.0
            self.root.ids.mapview.trigger_update('full')
        elif platform == 'android':
            if self.boat_exist():
                print(f"LAT:{self.marker_boat.lat}, LON:{self.marker_boat.lon}")
                self.marker_boat.lat = self.gps_latitude
                self.marker_boat.lon = self.gps_longitude
                print(f"LAT:{self.marker_boat.lat}, LON:{self.marker_boat.lon}")
                self.root.ids.mapview.trigger_update('full')

    def boat_exist(self):
        """Prüfen ob Boot-Marker bereits vorhanden ist."""
        if hasattr(self,'marker_boat'):
            return True
        else:
            return False
        
    def draw_circle(self):
        """Zeichne den Kreis auf dem Canvas."""
        self.offcenter = 21
        if platform == 'win':
            lat = 50.0
            lon = 8.0
        elif platform == 'android':
            lat = self.gps_latitude
            lon = self.gps_longitude

        try:
            self.marker_boat.lat = lat
            self.marker_boat.lon = lon
        except AttributeError:
            print("Marker Boot bei DrawCircle wurde nicht gefunden!")
            return

        self.center_map(lat=lat, lon=lon)
        self.add_marker()
        self.calculate_distance()

        # with self.root.canvas:
        #     Color(1,0,0,1)
        #     self.line = Line(circle=(self.marker_anchor.pos[0]+self.offcenter, 
        #                              self.marker_anchor.pos[1]+self.offcenter, 
        #                              int(self.root.ids.radius.text)*self.pixel_per_meter), 
        #                              width=2)
        with self.root.ids.mapview.canvas:
            self.line = Line(circle=(self.marker_anchor.pos[0]+self.offcenter, 
                                     self.marker_anchor.pos[1]+self.offcenter, 
                                     int(self.root.ids.radius.text)*self.pixel_per_meter), 
                                     width=2)

        self.clock = Clock.schedule_interval(self.update_circle, 1/1000)

        return
    
    def back_action(self):
        """Beim zurück Navigieren zur MainView wird der Kreis wieder gesetzt, soweit dieser vorher gestartet wurde."""
        if  not self.is_program_stopped:
            self.is_program_stopped = False
            self.root.ids.launchButton.text = "Stop"
            self.draw_circle()            
            return
        sc.check_input(self)

    def move_anchor_button(self, direction):
        """Bewegt mit dem D.PAD den Anker."""
        d_pad.move_anchor(self, direction)

    def calculate_distance(self):
        """Berechnet die Distanz zwischen 2 Markern in Pixeln."""
        current_width_x=self.root.size[0]

        # hole Koordinaten vom linken Rand
        left_coord = self.root.ids.mapview.get_latlon_at(0,
                                                         0,
                                                         self.root.ids.mapview.zoom)
        # hole Koordinaten vom rechten Rand
        right_coord = self.root.ids.mapview.get_latlon_at(current_width_x,
                                                          0,
                                                          self.root.ids.mapview.zoom)

        # Entfernungsberechnung
        dx = 71.5 * (left_coord[1] - right_coord[1])
        dy = 111.3 * (left_coord[0] - right_coord[0])

        distance = math.sqrt((dx * dx) + (dy * dy))

        # Umrechnung von Fensterbreite in Pixel und Distanz in Meter zu Pixel Pro Meter 
        self.pixel_per_meter = (current_width_x / distance) / 1000

    def update_circle(self, *args):
        """Aktualisiere den Kreis auf dem Canvas"""
        self.calculate_distance()

        anchor_lat = self.marker_anchor.pos[0]+self.offcenter
        anchor_lon = self.marker_anchor.pos[1]+self.offcenter
        radius = int(self.root.ids.radius.text)*self.pixel_per_meter

        if self.is_anchor_visible:
            self.line.circle = anchor_lat, anchor_lon, radius
        else:
            self.line.circle = 0, 0, 0
        self.update_boat()

        # hole aktuelle Marker Positionen und prüfen, ob Boot innerhalb des Radius ist
        currAnchorPos = self.get_current_anchor_location()
        currBoatPos = self.get_current_boat_location()
        self.is_inside_circle(currAnchorPos[0], 
                              currAnchorPos[1], 
                              int(self.root.ids.radius.text)*self.pixel_per_meter, 
                              currBoatPos[0], 
                              currBoatPos[1])
        
        self.check_if_marker_out_of_screen()

    def get_current_anchor_location(self):
        """Gibt die aktuelle Ankerposition zurück."""
        return self.root.ids.mapview.get_window_xy_from(self.marker_anchor.lat, 
                                                        self.marker_anchor.lon, 
                                                        self.root.ids.mapview.zoom)
    
    def get_current_boat_location(self):
        """Gibt die aktuelle Bootposition zurück."""
        return self.root.ids.mapview.get_window_xy_from(self.marker_boat.lat, 
                                                        self.marker_boat.lon, 
                                                        self.root.ids.mapview.zoom)
    
    # check if point is inside circle
    def is_inside_circle(self, circle_x, circle_y, rad, x, y, *args):
        """Prüfen ob Boot innerhalb des Radius ist."""
        if (x - circle_x) * (x - circle_x) + (y - circle_y) * (y - circle_y) <= rad * rad:
            return
        else:
            self.stop_update_circle()
            self.show_dialog()
            self.play_sound()
            return
    
    def show_dialog(self):
        """Alarm Meldung falls der Kreis verlassen wurde."""
        if not self.dialog:
            self.dialog = MDDialog(
                title="ALARM!",
                type="custom",
                md_bg_color= "#880015",
                content_cls=MDBoxLayout(
                    Image(source='src/images/error.png'),
                    MDLabel( 
                        text='IHR SCHIFF TREIBT AB!',
                        halign="center"
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp"
                ),
                buttons=[
                    MDFlatButton(
                        text="CLOSE",
                        on_release=self.close_dialog,
                        
                    )
                ],
                on_dismiss=self.close_without_cancel_button,
            )
        self.dialog.open()

    def close_without_cancel_button(self,  *args):
        """Kreis zeichnen und Sound stoppen sobald Warnung ausgeblendet wird."""
        self.draw_circle()
        self.sound.stop()

    def close_dialog(self, *args):
        """Schließe den Dialog mit dem Titel ALARM! """
        self.dialog.dismiss()

    def center_map_button(self):
        """Zentriere Map beim Button-Click."""
        if platform == 'win':
            lat =  48.4715279
            lon = 7.9512879
            self.center_map(lat, lon, 16)
        elif platform == 'android':
            self.center_map(self.gps_latitude, self.gps_longitude, zoom=19)

    def center_map(self, lat, lon, zoom=19):
        """Zentriert die Map."""
        self.root.ids.mapview.zoom = zoom
        self.root.ids.mapview.center_on(lat, lon)
        return
   
    def stop_update_circle(self):
        """Stoppt das zeichnen des Kreises."""
        try:
            self.clock.cancel()
            self.line.circle = 0,0,0
            self.root.ids.mapview.remove_widget(self.marker_anchor)
            self.marker = False
        except AttributeError:
            print("AttributeError crash bei Stop_Update_Circle wurde abgefangen!")

    def button_increase_radius(self):
        """Erhöht den Radius."""
        sc.increase_radius(self)

    def button_decrease_radius(self):
        """Reduziert den Radius."""
        sc.decrease_radius(self)
    
    def settings_error_button(self):
        """Prüfen ob eingabe den grenzwert unter- oder überschreitet"""
        sc.settings_error(self)

    def write_to_file_button(self):
        """Schreibt den Radius und ausgewählten Sound in daten.json."""
        sc.write_to_file(self)
        # self.radius_widget = self.root.ids.radius.text
        # self.spinner_widget = self.root.ids.sound_spinner.text

        # if platform == 'android':
        #     pfad = Path(__file__).resolve().parent
        #     data_dir = pfad / 'src/json/daten.json'
        #     #data_dir = MainApp().user_data_dir
        #     dictionary = {
        #     "Bereich": "Einstellungen",
        #     "Radius": self.radius_widget,
        #     'Audio Data': self.spinner_widget
        #     }
        #     with open (data_dir, "w") as file:
        #         json.dump(dictionary,file)
        # elif platform == 'win':
        #     dictionary = {
        #     "Bereich": "Einstellungen",
        #     "Radius": self.radius_widget,
        #     'Audio Data': self.spinner_widget
        #     }
        #     with open ("src/json/daten.json", "w") as file:
        #         json.dump(dictionary,file)

    def load_settings_button(self):
        """Lädt den Radius und ausgewählten Sound aus daten.json."""
        sc.load_settings(self)
        # if platform == 'android':
        #     pfad = Path(__file__).resolve().parent
        #     data_dir = pfad / 'src/json/daten.json'
            
        #     #data_dir = MainApp().user_data_dir + "/daten.json"
        # elif platform == 'win':
        #     pfad = Path(__file__).resolve().parent
        #     data_dir = pfad / 'src/json/daten.json'
        #     #data_dir = "src/json/daten.json"

        # f = open(data_dir)
        # data = json.load(f)
        # self.root.ids.radius.text = data['Radius']
        # self.root.ids.sound_spinner.text = data['Audio Data']
        # f.close()

    def play_sound(self):
        """Spielt den ausgewählten Sound ab."""
        wahlsound = self.root.ids.sound_spinner.text
        soundNamenListe =["Alarm1","Alarm2","Alarm3"]
        if wahlsound in soundNamenListe:
            self.sound = SoundLoader.load(os.path.join(f'src/sounds/{wahlsound}.wav'))
            self.sound.play()
            self.sound.volume = 1
                                 
    def add_boat_marker(self, lat, lon):
        """Fügt Boot-Marker hinzu."""
        if platform == 'win':
            lat = 50.0
            lon = 8.0
        elif platform == 'android':
            try:
                lat = self.gps_latitude
                lon = self.gps_longitude
            except AttributeError:
                print("Excepton in AddBoatMarker")
                lat = 50.0
                lon = 8.0

        if not self.boat_exist():
            self.marker_boat = MapMarker(lat=lat, lon=lon, source='src/images/boat_32.png')
            self.root.ids.mapview.add_widget(self.marker_boat)
            
    def class_that_does_everything(self, dt):
        """Startet das Programm."""
        # while 1:
        if platform == 'win':
            lat = 50.0
            lon = 8.0
            # break
        elif platform == 'android':
            try:
                lat = self.gps_latitude
                lon = self.gps_longitude
                # break
            except AttributeError:
                print("Exception in ClassThatDoes")
                lat = 50.0
                lon = 8.0

        self.add_boat_marker(lat, lon)
        self.center_map(lat, lon)
        self.root.ids.mapview.trigger_update('full')

    # Prüfen, ob Anker innhalb des Mapview Frames ist um Radius auszublenden
    def check_if_marker_out_of_screen(self):
        """Prüfen ob der Anker innerhalb des Frames ist."""
        bbox = self.root.ids.mapview.get_bbox()
        
        lat_condition = bbox[0] <= self.marker_anchor.lat <= bbox[2]
        lon_condition = bbox[1] <= self.marker_anchor.lon <= bbox[3]

        # Prüfen, ob Anker innerhalb der Boxgrenzen ist
        if   lat_condition and lon_condition:
            self.is_anchor_visible = True
        else:
            self.is_anchor_visible = False
        
if __name__ == "__main__":
    MainApp().run()
