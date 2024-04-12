class Ship:
    def __init__(self, ship_type=None, size=None, positions=[],  is_sunk=None):
        self.ship_type = ship_type
        self.size = size
        self.positions = positions
        self.is_sunk = is_sunk
    def __init__(self):
        self.positions = []

    def __str__(self):
        return f"Ship(ship_type={self.ship_type}, size={self.size}, positions={self.positions}, orientation={self.orientation}, is_sunk={self.is_sunk})"