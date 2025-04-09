from logging import raiseExceptions

from Jaipur.card import Card
from Jaipur.resource import Resource


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

    def deal_hand(self, deck):
        self.hand.extend(deck.deal_cards(5))

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

        if amount <= 0:
            raise ValueError("No se puede vender menos de 1")

        if type in Resource.expensive_resources() and amount < 2:
            raise ValueError("Tenes que vender al menos 2 cartas de este tipo")

        # put sold cards on discard pile
        cards_sold = 0
        for i in range(len(self.hand))[::-1]:
            if self.hand[i].card_type == type and cards_sold != amount:
                board.discard_pile.append(self.hand.pop(i))
                cards_sold += 1

        # make amount equal to the amount of tokens left
        if amount > len(board.tokens[type]):
            amount = len(board.tokens[type])

        # get resource tokens
        for i in range(amount):
            self.token_pile.append(board.tokens[type].pop(0))

        # get bonus tokens

        if amount == 3 and len(board.tokens[Resource.TOKENX3]) > 0:
            self.token_pile.append(board.tokens[Resource.TOKENX3].pop(0))

        elif amount == 4 and len(board.tokens[Resource.TOKENX4]) > 0:
            self.token_pile.append(board.tokens[Resource.TOKENX4].pop(0))

        elif amount >= 5 and len(board.tokens[Resource.TOKENX5]) > 0:
            self.token_pile.append(board.tokens[Resource.TOKENX5].pop(0))

    def exchange(self, board, player_card_indices, market_card_indices):

        player_cards_ex = []
        market_cards_ex = []

        player_cards_types = set()
        market_cards_types = set()

        if 99 in market_card_indices:
            raise ValueError('No podes cambiar camellos')
        if len(player_card_indices) < 2:
            raise ValueError('Necesitas intercambiar al menos dos cartas')
        if len(player_card_indices) != len(market_card_indices):
            raise ValueError('Tenes que intercambiar la misma cantidad de cartas')
        if len(market_card_indices) > len(self.hand + self.herd):
            raise ValueError('No tenes suficientes cartas para intercambiar')
        if len(player_card_indices) > len(board.market):
            raise ValueError('No hay suficientes cartas en el mercado para intercambiar')
        if player_card_indices.count(99) > len(self.herd):
            raise ValueError('No tenes suficientes camellos')

        for i in player_card_indices:
            if i >= len(self.hand + self.herd) and i != 99:
                raise ValueError('')

        for i in market_card_indices:
            if i >= len(board.market) and i != 99:
                raise ValueError('MAl')

        for i in market_card_indices[::-1]:
            market_cards_types.add(board.market[i])
        for i in player_card_indices[::-1]:
            if i == 99:
                player_cards_types.add(self.herd[0])
            else:
                player_cards_types.add(self.hand[i])
        if player_cards_types.intersection(market_cards_types):
            raise ValueError('No se puede cambiar por el mismo tipo de cartas')



        for i in market_card_indices[::-1]:
            market_cards_ex.append(board.market.pop(i))
        for i in player_card_indices[::-1]:
            if i == 99:
                player_cards_ex.append(self.herd.pop())
            else:
                player_cards_ex.append(self.hand.pop(i))


        for i in range(len(player_cards_ex)):
            board.market.append(player_cards_ex.pop(0))

        for i in range(len(market_card_indices)):
            self.hand.append(market_cards_ex.pop(0))

    def take_one_resource(self, board, card_index):
        if len(self.hand) == 7:
            raise ValueError('No podes agarrar más de siete cartas')

        # take the card from the market and put it in the hand
        self.hand.append(board.market.pop(card_index))

    def take_all_camels(self, board):
        camel_count = board.market.count(Card(Resource.CAMEL))
        if camel_count == 0:
            raise ValueError('No hay camellos para agarrar')

        for i in range(len(board.market))[::-1]:
            if board.market[i].card_type == Resource.CAMEL:
                self.herd.append(board.market.pop(i))

    def print_token_pile(self):
        s = ''
        for i in self.token_pile:
            s += f'{i.token_type.value} {i.value} '
        return s
