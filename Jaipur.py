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
        for i in range(11):
            self.deck.append(Card(Resource.CAMEL))
        for i in range(6):
            self.deck.append(Card(Resource.DIAMOND))
            self.deck.append(Card(Resource.GOLD))
            self.deck.append(Card(Resource.SILVER))
        for i in range(8):
            self.deck.append(Card(Resource.CLOTH))
            self.deck.append(Card(Resource.SPICES))
        for i in range(10):
            self.deck.append(Card(Resource.LEATHER))

        # self.shuffle_cards()

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
        self.herd = []
        self.token_pile = []

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

    def check_herd(self):
        for i in range(len(self.hand))[::-1]:
            if self.hand[i].card_type == Resource.CAMEL:
                self.herd.append(self.hand.pop(i))

    def sell(self, board, type, amount):
        total_from_type = 0
        for i in self.hand:
            if i.card_type == type:
                total_from_type += 1

        if amount > total_from_type:
            raise ValueError("No tenes suficientes cartas de este tipo")

        if amount >= 0:
            raise ValueError("No se puede vender menos de 1")

        if amount > len(board.tokens[type]):
            amount = len(board.tokens[type])

        for i in range(amount):
            self.token_pile.append(board.tokens[type].pop(0))

        if amount == 3 and len(board.tokens[Resource.TOKENX3]) > 0:
            self.token_pile.append(board.tokens[Resource.TOKENX3].pop(0))

        elif amount == 4 and len(board.tokens[Resource.TOKENX4]) > 0:
            self.token_pile.append(board.tokens[Resource.TOKENX4].pop(0))

        elif amount >= 5 and len(board.tokens[Resource.TOKENX5]) > 0:
            self.token_pile.append(board.tokens[Resource.TOKENX5].pop(0))

        cards_sold = 0
        for i in range(len(self.hand))[::-1]:
            if self.hand[i].card_type == type and cards_sold != amount:
                board.discard_pile.append(self.hand.pop(i))
                cards_sold += 1

    def exchange(self, board, player_card_indices, market_card_indices):

        if len(player_card_indices) != len(market_card_indices):
            raise ValueError('Tenes que intercambiar la misma cantidad de cartas')
        if len(market_card_indices) > len(self.hand + self.herd):
            raise ValueError('No tenes suficientes cartas para intercambiar')
        if len(player_card_indices) > len(board.market):
            raise ValueError('No hay suficientes cartas en el mercado para intercambiar')
        if player_card_indices.count(99) > len(self.herd):
            raise ValueError('No tenes suficientes camellos')

        for i in market_card_indices[::-1]:
            self.hand.append(board.market.pop(i))
        for i in player_card_indices[::-1]:
            if i == 99:
                board.market.append(self.herd.pop())
            else:
                board.market.append(self.hand.pop(i))


    def print_token_pile(self):
        s = ''
        for i in self.token_pile:
            s += f'{i.token_type.value} {i.value} '
        return s


class Board:
    def __init__(self, p1, p2, deck):
        self.tokens = self.create_tokens()
        self.p1 = p1
        self.p2 = p2
        self.deck = deck
        self.market = self.deck.deal_market()
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

    def __repr__(self):
        s = ""
        blank_line = "|" + " " * 104 + "|" + "\n"

        s += "+" + "-" * 104 + "+" + "\n"
        s += f'|{'Opponent hand: ' + self.p2.hide_hand():^104}|\n'
        s += blank_line
        s += f'|{'Opponent herd: ' + str(len(self.p2.herd)) :^104}|\n'
        s += f'|{'Deck: ' + str(len(self.deck)):^104}|\n'
        s += blank_line
        for resource in Resource.normal_resources():
            temp_s = ''
            temp_s += f'| ({resource.value}) {self.print_tokens(resource)}'
            s += temp_s + ' ' * (105 - len(temp_s)) + '|\n'
        s += f'|{self.print_market() :^104}|\n'
        for resource in Resource.bonus_tokens():
            temp_s = ''
            temp_s += f'| ({resource.value}) {self.print_tokens(resource)}'
            s += temp_s + ' ' * (105 - len(temp_s)) + '|\n'
        s += blank_line * 3
        s += f'|{'Your herd: ' + str(len(self.p1.herd)) :^104}|\n'
        s += blank_line
        s += f'|{'Your hand: ' + str(self.p1):^104}|\n'
        s += "+" + "-" * 104 + "+" + "\n"
        return s


deck = Deck()
player1 = Player('Rocio')
player2 = Player('Diego')
deck.shuffle_cards()
deck.deal_cards(player1, 5)
deck.deal_cards(player2, 5)
board = Board(player1, player2, deck)

print(deck)

print(board.tokens)

print(board)

player1.exchange(board,[0, 1, 2, 3, 4, 99], [0, 1, 2, 3, 4, 5])

print(board)


