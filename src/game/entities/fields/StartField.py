from src.game.entities.fields.Field import Field

class StartField(Field):
    def land_on_field(self, player):
        player.money += 200  # Предполагаем, что прохождение через старт приносит деньги
        return "Вы прошли через старт и получили 200!"

    def land_through_field(self, player):
        player.money += 200
        return "Вы прошли через старт и получили 200!"

