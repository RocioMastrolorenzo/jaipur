import random

from Jaipur.card import Card
from Jaipur.resource import Resource


class Deck:
    def __init__(self):
        self.deck: list[Card] = []
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

    def __repr__(self):
        return str(self.deck)

    def __len__(self):
        return len(self.deck)

    def shuffle_cards(self):
        random.shuffle(self.deck)
        return self

    def deal_cards(self, amount):
        cards = [self.deck.pop() for i in range(amount)]
        return cards

    def deal_market_setup(self):
        market = []
        total_camels = 0
        total_resources = 0
        while len(market) < 5:
            c = self.deck.pop()
            if c.card_type == Resource.CAMEL and total_camels < 3:
                market.insert(0, c)
                total_camels += 1
            elif c.card_type != Resource.CAMEL and total_resources < 2:
                market.append(c)
                total_resources += 1
            else:
                self.deck.insert(0, c)
        return market
