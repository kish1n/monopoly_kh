from game.fields.Field import Field

class ChanceField(Field):
    def land_on_field(self, player):
        # Здесь можно добавить логику выбора карты шанса
        return "Вытяните карту шанса!"