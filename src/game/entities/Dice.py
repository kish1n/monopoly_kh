import random

class Dice:
    def __init__(self):
        self.last_roll = (0, 0)

    def roll(self):
        # Бросок двух костей
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.last_roll = (die1, die2)

        # Проверка на четность
        if (die1 + die2) % 2 == 0:
            die3 = random.randint(1, 6)
            return self.last_roll + (die3,)
        return self.last_roll

    def get_last_roll(self):
        return self.last_roll