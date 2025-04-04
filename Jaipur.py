from Jaipur.board import Board
from Jaipur.deck import Deck
from Jaipur.player import Player

if __name__ == '__main__':
    deck = Deck()
    player1 = Player('Rocio')
    player2 = Player('Diego')
    deck.shuffle_cards()
    deck.deal_cards(player1, 5)
    deck.deal_cards(player2, 5)
    board = Board(player1, player2, deck)

    print(board)
