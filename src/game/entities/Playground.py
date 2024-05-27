from src.game.entities.Dice import Dice

class Playground:
    def __init__(self):
        self.fields = []
        self.players = []
        self.dice = Dice()
        self.current_player_index = 0

    def add_field(self, field):
        self.fields.append(field)

    def add_player(self, player):
        self.players.append(player)

    def next_turn(self):
        current_player = self.players[self.current_player_index]
        roll_result = self.dice.roll()
        total_roll = sum(roll_result[:2])

        print(f"{current_player.name} бросил кости и выпало: {roll_result}")

        current_player.move(total_roll)
        current_position = current_player.position
        current_field = self.fields[current_position]

        print(f"{current_player.name} попал на {current_field.name}")

        action_result = current_field.land_on_field(current_player)
        print(action_result)

        # Дополнительный бросок, если сумма четная
        if len(roll_result) == 3:
            extra_roll = roll_result[2]
            print(f"Дополнительный бросок: {extra_roll}")
            current_player.move(extra_roll)
            current_position = current_player.position
            current_field = self.fields[current_position]

            print(f"{current_player.name} попал на {current_field.name} после дополнительного броска")

            action_result = current_field.land_on_field(current_player)
            print(action_result)

        # Переход к следующему игроку
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def start_game(self):
        while True:
            self.next_turn()
            # Условие завершения игры можно добавить здесь
