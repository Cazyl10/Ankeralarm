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
        if int(self.radius_widget.text) - 10 <= 10:
                return
        # Verringere den aktuellen Wert um 10
        self.radius_widget.text = str(int(self.radius_widget.text) - 10)

def settings_error(self):
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
        self.radius_widget = self.root.ids.radius

        if self.radius_widget.text == '':
                self.radius_widget.text = "10"

        if len(self.radius_widget.text) < 2:
                self.radius_widget.text = "10"
                return