def increase_radius(self):
        """Erhöht den Radius."""
        #Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        #Erhöhen des aktuellen Wertes um 10
        self.radius_widget.text = str(int(self.radius_widget.text) + 10)

def decrease_radius(self):
        """Reduziert den Radius."""
        # Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        # Verringere den aktuellen Wert um 10
        self.radius_widget.text = str(int(self.radius_widget.text) - 10)