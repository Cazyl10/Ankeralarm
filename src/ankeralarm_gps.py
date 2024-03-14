from kivy.utils import platform

def get_permission(self, dt):
        """Holt Berechtigung für GPS"""
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            permissions = [Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]
            request_permissions(permissions, self.permission_callback)
            return True
        
        return False

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