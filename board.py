import random

from Jaipur.player import Player
from Jaipur.resource import Resource
from Jaipur.gametoken import GameToken


class Board:
    def __init__(self, p1, p2, deck):
        self.align_offset = 30

        self.tokens = self.create_tokens()
        self.p1: Player = p1
        self.p2: Player = p2
        self.deck = deck
        self.market = self.deck.deal_market_setup()
        self.discard_pile = []
        self.current_player = p1
        self.other_player = p2

        self.shuffle_bonus_tokens()
        self.p1.check_herd()
        self.p2.check_herd()

    # noinspection PyMethodMayBeStatic
    def create_tokens(self):
        token_mapping = {
            Resource.DIAMOND: [7, 7, 5, 5, 5],
            Resource.GOLD: [6, 6, 5, 5, 5],
            Resource.SILVER: [5, 5, 5, 5, 5],
            Resource.CLOTH: [5, 3, 3, 2, 2, 1, 1],
            Resource.SPICES: [5, 3, 3, 2, 2, 1, 1],
            Resource.LEATHER: [4, 3, 2, 1, 1, 1, 1, 1, 1],
            Resource.TOKENX5: [10, 10, 9, 8, 8],
            Resource.TOKENX4: [6, 6, 5, 5, 4, 4],
            Resource.TOKENX3: [3, 3, 2, 2, 2, 1, 1],
            Resource.CAMEL: [5],
        }

        tokens = {
            Resource.DIAMOND: [],
            Resource.GOLD: [],
            Resource.SILVER: [],
            Resource.CLOTH: [],
            Resource.SPICES: [],
            Resource.LEATHER: [],
            Resource.TOKENX5: [],
            Resource.TOKENX4: [],
            Resource.TOKENX3: [],
            Resource.CAMEL: [],
        }

        for i in token_mapping:
            for j in token_mapping[i]:
                tokens[i].append(GameToken(i, j))


        return tokens

    def print_tokens(self, resource_type):
        s = ''
        for i in self.tokens[resource_type]:
            s += str(i) + ' '
        return s

    def print_market(self):
        s = ''
        for i in self.market:
            s += f"{i} "
        return s

    def shuffle_bonus_tokens(self):
        for i in Resource.bonus_tokens():
            random.shuffle(self.tokens[i])

    def fill_market(self):
        fill_amount = 5 - len(self.market)
        if len(self.market) < 5:
            self.market.extend(self.deck.deal_cards(fill_amount))

    def switch_players(self):
        temp = self.current_player
        self.current_player = self.other_player
        self.other_player = temp

    def round_end_check(self):
        empty_token_pile = 0
        for i in self.tokens:
            if len(self.tokens[i]) == 0 and i in Resource.normal_resources():
                empty_token_pile += 1
        if empty_token_pile >= 3:
            return True
        elif len(self.deck) == 0 and len(self.market) < 5:
            return True
        else:
            return False

    def give_camel_token(self):
        if len(self.p1.herd) != len(self.p2.herd):
            winner = max([self.p1, self.p2], key=lambda p: len(p.herd))
            winner.token_pile.append(self.tokens[Resource.CAMEL].pop())

    def give_point(self):
        if self.p1.count_points() != self.p2.count_points():
            winner = max([self.p1, self.p2], key=lambda p: p.count_points())
            winner.score += 1
        else:
            winner = "No one"
        return f"player 1: {self.p1.count_points()} player 2: {self.p2.count_points()} \n {winner} wins!"

    def __repr__(self):
        s = ""
        blank_line = " " * 104  + "\n"

        s += "+" + "-" * 104 + "+" + "\n"
        s += f'{" " * self.align_offset}{'Opponent hand: ' + self.other_player.hide_hand()}\n'
        s += blank_line
        s += f'{'Opponent herd: ' + str(len(self.other_player.herd)) :^104}\n'
        s += f'{'Deck: ' + str(len(self.deck)):^104}\n'
        s += f'{"Tokens: " + str(len(self.other_player.token_pile)):>104}\n'
        s += f'{"Current points: " + str(self.other_player.count_tokens_no_bonus()):>104}\n'
        s += blank_line
        for resource in Resource.normal_resources():
            temp_s = ''
            temp_s += f' ({resource.value}) {self.print_tokens(resource)}'
            s += temp_s + ' ' * (105 - len(temp_s)) + '\n'
        s += f'{" " * (self.align_offset+10)}{self.print_market()}\n'
        for resource in Resource.bonus_tokens():
            temp_s = ''
            temp_s += f' ({resource.value}) {self.print_tokens(resource)}'
            s += temp_s + ' ' * (105 - len(temp_s)) + '\n'
        s += blank_line
        s += f'{"Tokens: " + str(len(self.current_player.token_pile)):>104}\n'
        s += f'{"Current points: " + str(self.current_player.count_tokens_no_bonus()):>104}\n'
        s += f'{'Your herd: ' + str(len(self.current_player.herd)) :^104}\n'
        s += blank_line
        s += f'{" " * self.align_offset}{'Your hand: ' + str(self.current_player)}\n'
        s += "+" + "-" * 104 + "+" + "\n"
        return s
