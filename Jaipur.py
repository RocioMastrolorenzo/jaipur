from Jaipur.board import Board
from Jaipur.deck import Deck
from Jaipur.player import Player

def choose_turn():
    #dictionary of valid words to input in addition to the corresponsing number
    valid_inputs = {
        "1": "1", "sell": "1", "sell cards": "1",
        "2": "2", "exchange": "2", "exchange cards": "2",
        "3": "3", "take": "3", "take one": "3", "resource": "3", "take one resource": "3",
        "4": "4", "camels": "4","take camels" : "4", "take all camels": "4", "camel": "4"
    }
    while True:
        print()
        turn = input('Choose your action to play \n'
                     '1. Sell cards\n'
                     '2. Exchange cards\n'
                     '3. Take one resource\n'
                     '4. Take all camels\n'
                     ).strip().lower()

        if turn in valid_inputs:
            return valid_inputs[turn] #returns a string with the number chosen
        else:
            print('Enter a valid action')

if __name__ == '__main__':
    deck = Deck()
    player1 = Player('Rocio')
    player2 = Player('Diego')
    deck.shuffle_cards()
    deck.deal_cards(player1, 5)
    deck.deal_cards(player2, 5)
    board = Board(player1, player2, deck)

    print(board)
    choose_turn()