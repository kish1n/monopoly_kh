from game.entities.fields.Field import Field

class PrisonField(Field):
    def land_on_field(self, player):
        return "Вы попали в тюрьму!"

#TODO: Написать кубики и потом написать варианты посещениюе тюрьмы посетитель и заключение и механики для этого