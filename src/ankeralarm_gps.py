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
            # gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.configure(on_location=self.on_location)
            gps.start(minTime=100, minDistance=0)
        except:
            import traceback
            traceback.print_exc()
            self.gps_status= "GPS is not implemented for your platform"