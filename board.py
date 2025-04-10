import random

from Jaipur.resource import Resource
from Jaipur.token import Token


class Board:
    def __init__(self, p1, p2, deck):
        self.align_offset = 30

        self.tokens = self.create_tokens()
        self.p1 = p1
        self.p2 = p2
        self.deck = deck
        self.market = self.deck.deal_market_setup()
        self.discard_pile = []

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
        }

        for resource_type in token_mapping:
            for value in token_mapping[resource_type]:
                tokens[resource_type].append(Token(resource_type, value))

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


    def __repr__(self):
        s = ""
        blank_line = " " * 104  + "\n"

        s += "+" + "-" * 104 + "+" + "\n"
        s += f'{" " * self.align_offset}{'Opponent hand: ' + self.p2.hide_hand()}\n'
        s += blank_line
        s += f'{'Opponent herd: ' + str(len(self.p2.herd)) :^104}\n'
        s += f'{'Deck: ' + str(len(self.deck)):^104}\n'
        s += f'{"Tokens: " + str(len(self.p2.token_pile)):>104}\n'
        s += f'{"Current points: " + str(self.p2.count_tokens_no_bonus()):>104}\n'
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
        s += f'{"Tokens: " + str(len(self.p1.token_pile)):>104}\n'
        s += f'{"Current points: " + str(self.p1.count_tokens_no_bonus()):>104}\n'
        s += f'{'Your herd: ' + str(len(self.p1.herd)) :^104}\n'
        s += blank_line
        s += f'{" " * self.align_offset}{'Your hand: ' + str(self.p1)}\n'
        s += "+" + "-" * 104 + "+" + "\n"
        return s
