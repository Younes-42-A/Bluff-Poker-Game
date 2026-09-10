import random
from typing import Tuple
class Player:
    def __init__(self, name: str , starting_ships: int = 100):
        self.name = name
        self.ships = starting_ships
        self.cards: Tuple[int, int] = (0, 0)
        self.actual_sum: int = 0
    def draw_cards(self) -> int:
        self.cards = (random.randint(1, 10),random.randint(1, 10))
        self.actual_sum = sum(self.cards)
        return self.actual_sum
    def get_ships(self) -> int:
        return self.ships
    def lose_ships(self, amount: int) -> int:
         self.ships -= amount
         if self.ships < 0:
             self.ships = 0
         return amount
    def gain_ships(self, amount: int) -> int:
         self.ships += amount
         return amount
    def bluff(self) -> int:
        bluffing_amount = int(input("Enter the amount you want to bluff (2-20): "))
        if bluffing_amount < 2 or bluffing_amount > 20:
            print("Invalid bluffing amount. Please enter a value between 2 and 20.")
            return self.bluff()
        return bluffing_amount