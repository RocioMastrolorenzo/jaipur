from Jaipur.board import Board
from Jaipur.deck import Deck
from Jaipur.player import Player
from Jaipur.resource import Resource



def choose_turn():
    # dictionary of valid words to input in addition to the corresponsing number
    valid_inputs = {
        "1": 1, "sell": 1, "sell cards": 1,
        "2": 2, "exchange": 2, "exchange cards": 2,
        "3": 3, "take": 3, "take one": 3, "resource": 3, "take one resource": 3,
        "4": 4, "camels": 4, "take camels": 4, "take all camels": 4, "camel": 4
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
            return valid_inputs[turn]  # returns an int
        else:
            print('Enter a valid action')


def print_hand(player):
    print_hand = ''

    # adds the cards from the hand
    for i in range(len(player.hand)):
        print_hand += str(player.hand[i]) + ' '

    print_hand += '| '

    # adds the cards from the herd
    for i in range(len(player.herd)):
        print_hand += str(player.herd[i]) + ' '

    print_hand += '\n'

    # adds the index number on the bottom
    for i in range(len(player.hand)):
        print_hand += " " + str(i) + "   "

    print_hand += '| '

    for i in range(len(player.herd)):
        print_hand += ' ' + str(i + len(player.hand)) + '  '

    print(print_hand)


def print_market(board):
    print_market = ""

    # adds the cards from the market
    for i in range(len(board.market)):
        print_market += str(board.market[i]) + ' '
    print_market += '\n'

    # adds the index number on the bottom
    for i in range(len(board.market)):
        print_market += " " + str(i) + "   "

    print(print_market)


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
            print('Enter a valid amount')
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


def get_exchange_input(board, player):
    market_indices = ""
    while True:
        try:
            print_market(board)
            market_indices = input('choose the cards you want to exchange: (0-1-2) ').split('-')
            market_indices = list({int(i) for i in market_indices})
            break
        except ValueError:
            print(f"Choose a valid card number.")
            continue

    # changes input to 99 if a camel was chosen
    for i in market_indices:
        if i >= len(board.market):
            raise ValueError(f"{i} is not a valid card number.")
        if board.market[i].card_type == Resource.CAMEL:
            raise ValueError("No se puede intercambiar con camellos")
    market_indices.sort()

    player_indices = ""
    while True:
        try:
            print_hand(player)
            player_indices = input(f'select {len(market_indices)} of your cards (0-1-2) ').split('-')
            player_indices = list({int(i) for i in player_indices})
            break
        except ValueError:
            print(f"Choose a valid card number.")
            continue
    player_indices.sort()
    for i in player_indices:
        if i >= len(player.hand) + len(player.herd):
            raise ValueError(f"{i} is not a valid card number.")

    # changes input to 99 if a camel was chosen
    for i in range(len(player_indices)):
        if player_indices[i] >= len(player.hand):
            player_indices[i] = 99

    return player_indices, market_indices


def get_take_one_resource_input(board):
    card_index_user = ""
    while True:
        try:
            print_market(board)
            card_index_user = int(input("Select the card to take "))
            break
        except ValueError:
            print(f"Choose a valid card number.")
            continue
    if card_index_user >= len(board.market):
        raise ValueError(f"{card_index_user} is not a valid card number.")

    if board.market[card_index_user].card_type == Resource.CAMEL:
        raise ValueError("You can't take a single camel")

    return card_index_user


if __name__ == '__main__':
    deck = Deck()
    player1 = Player('Rocio')
    player2 = Player('Diego')
    deck.shuffle_cards()
    player1.deal_hand(deck)
    player2.deal_hand(deck)
    board = Board(player1, player2, deck)

    print(board)
    while True:
        chosen_turn = choose_turn()
        if chosen_turn == 1:  # sell
            try:
                user_type, user_amount = get_sell_input()
                player1.sell(board, user_type, user_amount)
                break
            except ValueError as e:
                print(e)
                continue
        elif chosen_turn == 2:  # exchange
            try:
                player_indices, market_indices = get_exchange_input(board, player1)
                player1.exchange(board, player_indices, market_indices)
                break
            except ValueError as e:
                print(e)
                continue
        elif chosen_turn == 3:  # take one
            try:
                card_index = get_take_one_resource_input(board)
                player1.take_one_resource(board, card_index)
                break
            except ValueError as e:
                print(e)
                continue
        elif chosen_turn == 4: #take all camels
            try:
                player1.take_all_camels(board)
                break
            except ValueError as e:
                print(e)
                continue
    board.fill_market()
    print(board)