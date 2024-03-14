from kivy.utils import platform

def get_permission(self, dt):
        """Holt Berechtigung für GPS"""
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            permissions = [Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]
            request_permissions(permissions, self.permission_callback)
            return True
        
        return False

