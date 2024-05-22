class Field:
    def __init__(self, num, name, img):
        self.num = num
        self.name = name
        self.img = img

    def land_on_field(self, player):
        raise NotImplementedError("This method should be overridden by subclasses.")

