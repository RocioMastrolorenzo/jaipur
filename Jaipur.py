import random
from enum import Enum
from tkinter import READABLE


class Resource(Enum):
    DIAMOND = 'di'
    GOLD = 'go'
    SILVER = 'si'
    CLOTH = 'cl'
    SPICES = 'sp'
    LEATHER = 'le'
    CAMEL = 'ca'
    TOKENX3 = 'x3'
    TOKENX4 = 'x4'
    TOKENX5 = 'x5'

    @classmethod
    def normal_resources(cls):
        return [cls.DIAMOND, cls.GOLD, cls.SILVER, cls.CLOTH, cls.SPICES, cls.LEATHER]

    @classmethod
    def bonus_tokens(cls):
        return [cls.TOKENX3, cls.TOKENX4, cls.TOKENX5]


class Card:
    def __init__(self, card_type):
        self.card_type = card_type

    def __repr__(self):
        return f"[{self.card_type.value}]"


class Deck:
    def __init__(self):
        self.deck = []
        for i in range(6):
            self.deck.append(Card(Resource.DIAMOND))
            self.deck.append(Card(Resource.GOLD))
            self.deck.append(Card(Resource.SILVER))
        for i in range(8):
            self.deck.append(Card(Resource.CLOTH))
            self.deck.append(Card(Resource.SPICES))
        for i in range(10):
            self.deck.append(Card(Resource.LEATHER))
        for i in range(11):
            self.deck.append(Card(Resource.CAMEL))
        self.shuffle_cards()

    def __repr__(self):
        return str(self.deck)

    def __len__(self):
        return len(self.deck)

    def shuffle_cards(self):
        random.shuffle(self.deck)
        return self

    def deal_cards(self, player, amount):
        for i in range(amount):
            player.hand.append(self.deck.pop())
        return player.hand

    def deal_market(self):
        market = []
        total_camels = 0
        total_resources = 0
        while len(market) < 5:
            c = self.deck.pop()
            if c.card_type == Resource.CAMEL and total_camels < 3:
                market.insert(0, c)
                total_camels += 1
            if c.card_type != Resource.CAMEL and total_resources < 2:
                market.append(c)
                total_resources += 1
            else:
                self.deck.insert(0, c)
        return market


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        if self.token_type in Resource.normal_resources():
            return str(self.value)
        else:
            return '?'


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def __repr__(self):
        s = ''
        for i in self.hand:
            s += str(i) + ' '
        return s

    def hide_hand(self):
        hidden_hand = ''
        for i in range(len(self.hand)):
            hidden_hand += '[??] '
        return hidden_hand


class Board:
    def __init__(self, p1, p2, deck):
        self.tokens = self.create_tokens()
        self.p1 = p1
        self.p2 = p2
        self.deck = deck

        self.shuffle_bonus_tokens()

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

    def shuffle_bonus_tokens(self):
        for i in Resource.bonus_tokens():
            random.shuffle(self.tokens[i])

    def __repr__(self):
        s = ""
        blank_line = "|" + " " * 104 + "|" + "\n"

        s += "+" + "-" * 104 + "+" + "\n"
        s += f'|{'Opponent hand: ' + self.p2.hide_hand():^104}|\n'
        s += blank_line
        s += f'|{'Opponent herd: ' + '3':^104}|\n'
        s += f'|{'Deck: ' + str(len(self.deck)):^104}|\n'
        s += blank_line
        for resource in Resource.normal_resources():
            temp_s = ''
            temp_s += f'| ({resource.value}) {self.print_tokens(resource)}'
            s += temp_s + ' ' * (105 - len(temp_s)) + '|\n'
        s += f'|{str(self.deck.deal_market()):^104}|\n'
        for resource in Resource.bonus_tokens():
            temp_s = ''
            temp_s += f'| ({resource.value}) {self.print_tokens(resource)}'
            s += temp_s + ' ' * (105 - len(temp_s)) + '|\n'
        s += blank_line * 3
        s += f'|{'Your herd: ' + '2':^104}|\n'
        s += f'|{'Your hand: ' + str(self.p1):^104}|\n'
        s += blank_line
        s += "+" + "-" * 104 + "+" + "\n"
        return s


deck = Deck()
player1 = Player('Rocio')
player2 = Player('Diego')
board = Board(player1, player2, deck)

print(deck)

deck.deal_cards(player1, 5)
deck.deal_cards(player2, 5)

print(board)
