
import random
from abc import ABC, abstractmethod
from typing import Tuple

class AIPlayer:
    def __init__(self, name: str, starting_ships: int = 100):
        self.name = name
        self.ships = starting_ships
        self.cards: Tuple[int, int] = (0, 0)
        self.actual_sum: int = 0

    def draw_cards(self) -> int:
        self.cards = (random.randint(1, 10), random.randint(1, 10))
        self.actual_sum = sum(self.cards)
        return self.actual_sum
    def make_defense_decision(self, current_bluff):
        """Evaluates the opponent's claimed sum and selects a defensive action based on risk assessment.
        Strategy Breakdown:
        -------------------
        1. Extreme / Unlikely Claims (>= 16 or <= 4):
        - Statistically rare sums for two cards (1-10 range).
        - High bluff probability -> Leans heavily toward Call Bluff ("1") or high-stakes Raise ("3").

        2. Moderate / Realistic Claims (10 - 15):
        - Highly probable sums around the statistical median (~11).
        - Conservative play -> Leans toward Pass ("2") to minimize risk, with balanced Call ("1") challenges.

        3. Low / Feasible Claims (5 - 9):
        - Believable low totals.
        - Risk-averse play -> Balanced mix between Pass ("2") and Call Bluff ("1").

        Returns:
            str: "1" for Call Bluff (10 ships), "2" for Pass (-10 ships), or "3" for Raise (25 ships).
        """
        if current_bluff >= 17 or current_bluff <= 4:
            if self.ships >= 50 and random.random() < 0.35:
                return "3"  # Raise
            return "1"  # Call Bluff

        elif 10 <= current_bluff <= 15:
            rand_val = random.random()
            if rand_val < 0.45:
                return "2"  # Pass 
            elif rand_val < 0.85:
                return "1"  # Call Bluff
            else:
                return "3"  # Raise

        else:
            rand_val = random.random()
            if rand_val < 0.60:
                return "2"  # Pass
            else:
                return "1"  # Call Bluff

    def bluff(self) -> int:
        """Calculates the bot's claimed sum using a strategic, weighted probability algorithm.
        Strategy Breakdown:
        -------------------
        1. Strong Hand (15 - 20):
        - 80% Truth: Value-claims to trap defenders into making an incorrect challenge.
        - 20% Over-Bluff: Adds +1 or +2 to maximize ship gains.

        2. Medium Hand (10 - 14):
        - 60% Truth: Standard balanced play to maintain credibility.
        - 40% Moderate Bluff: Inflates claim by +2 to +4 to pressure defenders into passing.

        3. Weak Hand (2 - 9):
        - 70% Aggressive Bluff: Claims a high range (13 - 17) to force a pass.
        - 30% Pure Truth: Reverse-psychology play to punish over-aggressive challenges.

        Returns:
            int: The claimed total sum (clamped between 2 and 20).
        """
        if random.random() < 0.60:
            return self.actual_sum

        if self.actual_sum < 10:
            return random.choice([11, 12, 13, 14, 15])
        else:
            bluff_val = self.actual_sum + random.choice([1, 2, -1, -2])
            return max(2, min(20, bluff_val))

    def lose_ships(self, amount: int) -> int:
        self.ships -= amount
        if self.ships < 0:
            self.ships = 0
        return amount

    def gain_ships(self, amount: int) -> int:
        self.ships += amount
        return amount