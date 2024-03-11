def increase_radius(self):
        """Erhöht den Radius."""
        #Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        #Erhöhen des aktuellen Wertes um 10
        self.radius_widget.text = str(int(self.radius_widget.text) + 10)