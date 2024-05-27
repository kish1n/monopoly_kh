from src.game.entities.fields.Field import Field

class PropertyField(Field):
    def __init__(self, num, name, group, buy_price, mortgage, rent_prices, house_prices,
                 img, owner=None, houses=0, mortgaged=False):
        super().__init__(num, name, img)
        self.group = group
        self.buy_price = buy_price
        self.mortgage = mortgage
        self.rent_prices = rent_prices
        self.house_prices = house_prices
        self.owner = owner
        self.houses = houses
        self.mortgaged = mortgaged

#geters
    def get_rent_price(self):
        return self.rent_prices[self.houses]

#property management
    def buy_field(self, player):
        if self.owner is None and player.money >= self.buy_price:
            self.owner = player
            player.money -= self.buy_price
            return True
        return False

    def mortgage_field(self):
        if self.owner is not None and not self.mortgaged:
            self.mortgaged = True
            self.owner.money += self.mortgage
            return True
        return False

    def unmortgage_field(self):
        if self.owner is not None and self.mortgaged:
            unmortgage_cost = self.mortgage * 1.1  # 10% штраф за выкуп
            if self.owner.money >= unmortgage_cost:
                self.owner.money -= unmortgage_cost
                self.mortgaged = False
                return True
            return False
        return False

#house management
    def build_house(self):
        if self.owner is not None and self.houses < 5:
            house_price = self.get_new_house_price()
            if self.owner.money >= house_price:
                self.owner.money -= house_price
                self.houses += 1
                return True
            return False
        return False

    def sell_house(self):
        if self.owner is not None and self.houses > 0:
            refund = self.house_prices[self.houses - 1] // 2
            self.owner.money += refund
            self.houses -= 1
            return refund
        return 0

#game logic
    def land_on_field(self, player):
        if self.owner is not None and self.owner != player:
            rent = self.get_rent_price()
            if player.money >= rent:
                player.money -= rent
                self.owner.money += rent
                return f"{player.name} заплатил {rent} {self.owner.name} за аренду {self.name}."
            else:
                return f"{player.name} не может оплатить аренду и объявляет банкротство."
        elif self.owner is None:
            return f"{self.name} доступен для покупки."
        return f"{player.name} находится на своем собственном поле."

    def upgrade_property(self):
        if self.houses < 5 and self.owner is not None:
            if self.houses == 4:
                hotel_cost = self.house_prices[4] * 4
                if self.owner.money >= hotel_cost:
                    self.owner.money -= hotel_cost
                    self.houses = 5
                    return True
                return False
            else:
                return self.build_house()
        return False

    def downgrade_property(self):
        if self.houses > 0:
            return self.sell_house()
        return 0

#method for strategy
    def calculate_total_value(self):
        total_value = self.buy_price + self.house_prices.get(self.houses, 0)
        if self.mortgaged:
            total_value -= self.mortgage
        return total_value

    def is_monopoly(self):
        if all(field.owner == self.owner for field in self.owner.properties if field.group == self.group):
            return True
        return False