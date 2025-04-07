from Jaipur.board import Board
from Jaipur.deck import Deck
from Jaipur.player import Player
from Jaipur.resource import Resource


def choose_turn():
    #dictionary of valid words to input in addition to the corresponsing number
    valid_inputs = {
        "1": 1, "sell": 1, "sell cards": 1,
        "2": 2, "exchange": 2, "exchange cards": 2,
        "3": 3, "take": 3, "take one": 3, "resource": 3, "take one resource": 3,
        "4": 4, "camels": 4,"take camels" : 4, "take all camels": 4, "camel": 4
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
            return valid_inputs[turn] #returns an int
        else:
            print('Enter a valid action')

def get_sell_input():
    user_amount = ""
    user_type = ""
    valid_inputs = {
        "diamond": Resource.DIAMOND, "di": Resource.DIAMOND,
        "gold": Resource.GOLD, "go": Resource.GOLD,
        "silver": Resource.SILVER, "si": Resource.SILVER,
        "cloth": Resource.CLOTH, "cl": Resource.CLOTH,
        "spices": Resource.SPICES, "sp": Resource.SPICES,
        "leather": Resource.LEATHER, "le": Resource.LEATHER,
        "camel": Resource.CAMEL, "ca": Resource.CAMEL
    }
    while True:
        try:
            user_amount = int(input('Enter amount to sell '))
            break
        except ValueError as e:
            print(e)
            continue
    while True:
        try:
            user_type_input = input('Enter type of resource to sell ')
            if user_type_input in valid_inputs:
                user_type = valid_inputs[user_type_input]
                break
            if user_type_input not in valid_inputs:
                raise ValueError('Enter a valid type of resource')
        except ValueError as e:
            print(e)
            continue


    return user_type, user_amount

if __name__ == '__main__':
    deck = Deck()
    player1 = Player('Rocio')
    player2 = Player('Diego')
    deck.shuffle_cards()
    deck.deal_cards(player1, 5)
    deck.deal_cards(player2, 5)
    board = Board(player1, player2, deck)

    print(board)
    while True:
        chosen_turn = choose_turn()
        if chosen_turn == 1: #sell
            try:
                user_type, user_amount = get_sell_input()
                player1.sell(board, user_type, user_amount)
                break
            except ValueError as e:
                print(e)
                continue
        #elif

