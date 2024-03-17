# Florian
def move_anchor(self, direction):
        """Bewegt mit dem D.PAD den Anker."""
        try:
            if direction == 'up':
                self.marker_anchor.lat += 0.0001
            if direction == 'left':
                self.marker_anchor.lon -= 0.0001
            if direction == 'right':
                self.marker_anchor.lon += 0.0001
            if direction == 'down':
                self.marker_anchor.lat -= 0.0001
        
            self.root.ids.mapview.trigger_update('full')
        except AttributeError:
            print("Anchor-Objekt bei MoveAnchor nicht gefunden!")