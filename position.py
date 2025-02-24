


class Position:
    def __init__(self, name, x, y, width, height):
        super().__setattr__("_locked", False)
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.name = name
        super().__setattr__("_locked", True)