class User11111:
    def __init__(self, game_id, name, color, starting_money=1500):
        self.game_id = game_id
        self.name = name
        self.money = starting_money
        self.properties = []
        self.in_jail = False
        self.position = 0
        self.color = None

    def move(self, steps):
        self.position = (self.position + steps) % 40
        return self.position

    def pay_rent(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        else:
            self.declare_bankruptcy()
            return False

    def buy_property(self, property):
        if self.money >= property.buy_price and property.owner is None:
            self.money -= property.buy_price
            self.properties.append(property)
            property.owner = self
            return True
        return False

    def sell_property(self, property, price):
        if property in self.properties:
            self.money += price
            self.properties.remove(property)
            property.owner = None
            return True
        return False

    def declare_bankruptcy(self):
        self.money = 0
        for property in self.properties:
            property.owner = None
        self.properties = []
        print(f"{self.name} объявил о банкротстве.")
        return True
