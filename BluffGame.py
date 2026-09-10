import random
import bluff_poker_AI
import player


class BluffGame:
    def __init__(self):
        try:
            self.player1 = player.Player(name='Gambler', starting_chips=100)
            self.bot = bluff_poker_AI.AIPlayer(name="Yomeko", starting_chips=100)
        except:
            self.player1 = player.Player(name='Gambler', starting_ships=100)
            self.bot = bluff_poker_AI.AIPlayer(name="Yomeko", starting_ships=100)

        self.players = [self.player1, self.bot]
        self.current_player_index = random.choice([0, 1])
        self.round_number = 1
        self.is_game_over = False
        self.current_bluff = 0
        self.last_message = "Game Started! Round 1"
        self.winner = None
        self.setup_round()
    @property
    def attacker(self):
        return self.players[self.current_player_index]
    @property
    def defender(self):
        return self.players[1 - self.current_player_index]

    def _get_chips(self, p):
        return getattr(p, 'chips', getattr(p, 'ships', 0))

    def _add_chips(self, p, amount):
        if hasattr(p, 'gain_chips'):
            p.gain_chips(amount)
        elif hasattr(p, 'gain_ships'):
            p.gain_ships(amount)

    def _remove_chips(self, p, amount):
        if hasattr(p, 'lose_chips'):
            p.lose_chips(amount)
        elif hasattr(p, 'lose_ships'):
            p.lose_ships(amount)

    def setup_round(self):
        if self.is_game_over:
            return

        self.attacker.draw_cards()

        if isinstance(self.attacker, bluff_poker_AI.AIPlayer):
            if hasattr(self.attacker, 'make_bluff'):
                self.current_bluff = self.attacker.make_bluff()
            elif hasattr(self.attacker, 'bluff'):
                self.current_bluff = self.attacker.bluff()
            else:
                self.current_bluff = self.attacker.actual_sum
            
            self.last_message = f"🤖 {self.bot.name} claims a total sum of [{self.current_bluff}]. Make your defense move!"

    def set_player_bluff(self, claimed_sum: int):
        self.current_bluff = claimed_sum
        self.last_message = f"⚔️ You claimed [{self.current_bluff}]! {self.bot.name} is making a defense decision..."
        
        bot_decision = self.bot.make_defense_decision(self.current_bluff)
        decision_map = {"1": "call", "2": "pass", "3": "raise"}
        chosen_action = decision_map.get(str(bot_decision), "call")
        
        if chosen_action == "pass":
            self.pass_turn(self.player1, self.bot)
        else:
            self.resolve_round(self.player1, self.bot, chosen_action)

        self.finish_turn()

    def play_human_defense(self, decision: str):
        if self.is_game_over:
            return

        if decision == "pass":
            self.pass_turn(self.bot, self.player1)
        else:
            self.resolve_round(self.bot, self.player1, decision)

        self.finish_turn()

    def pass_turn(self, attacker, defender):
        self._remove_chips(defender, 10)
        self._add_chips(attacker, 10)
        self.last_message = f"🏳️ {defender.name} PASSED! 10 chips transferred to {attacker.name}."

    def resolve_round(self, attacker, defender, decision: str):
        stakes = 25 if decision == "raise" else 10
        is_lying = (attacker.actual_sum != self.current_bluff)

        if is_lying:
            self._add_chips(defender, stakes)
            self._remove_chips(attacker, stakes)
            self.last_message = (
                f"🚨 BLUFF DETECTED! {attacker.name} lied! "
                f"(Actual: {attacker.actual_sum} | Claimed: {self.current_bluff}). "
                f"{defender.name} gains +{stakes} chips!"
            )
        else:
            self._remove_chips(defender, stakes)
            self._add_chips(attacker, stakes)
            self.last_message = (
                f"✅ TRUTH! {attacker.name} was honest! "
                f"(Actual sum: {attacker.actual_sum}). "
                f"{defender.name} loses -{stakes} chips!"
            )

    def finish_turn(self):
        self.check_game_over()
        if not self.is_game_over:
            self.current_player_index = 1 - self.current_player_index
            self.round_number += 1
            if self.round_number > 12:
                self.check_game_over()
            else:
                self.setup_round()

    def check_game_over(self):
        p1_chips = self._get_chips(self.player1)
        p2_chips = self._get_chips(self.bot)

        if p1_chips <= 0 or p2_chips <= 0 or self.round_number > 12:
            self.is_game_over = True
            if p1_chips > p2_chips:
                self.winner = self.player1.name
            elif p2_chips > p1_chips:
                self.winner = self.bot.name
            else:
                self.winner = "Draw"
            self.last_message = f"🏆 GAME OVER! Winner: {self.winner}"