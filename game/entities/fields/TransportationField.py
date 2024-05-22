from game.entities.fields.Field import Field

class TransportationField(Field):
    def __init__(self, num, name, buy_price, img, owner=None):
        super().__init__(num, name, img)
        self.buy_price = buy_price
        self.owner = owner

    def land_on_field(self, player):
        if self.owner and self.owner != player:
            return f"Оплатите аренду {self.owner.name}"
        elif self.owner is None:
            return f"{self.name} доступен для покупки."