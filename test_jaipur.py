import pytest

from Jaipur.board import Board
from Jaipur.card import Card
from Jaipur.deck import Deck
from Jaipur.player import Player
from Jaipur.resource import Resource
from Jaipur.gametoken import GameToken


@pytest.fixture
def game_objects():
    deck = Deck()
    player1 = Player('a')
    player2 = Player('b')
    board = Board(player1, player2, deck)
    return deck, board, player1, player2


def test_exchange_not_enough_camels(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    player1.herd = []
    with pytest.raises(ValueError, match="You don't have enough camels"):
        player1.exchange(board, [0, 99, 99], [0, 1, 2])


def test_exchange_not_equal_amount(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    with pytest.raises(ValueError, match="You must exchange the same amount of cards"):
        player1.exchange(board, [0, 1, 2], [0, 1, 2, 3])


def test_exchange_not_enough_player_cards(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    with pytest.raises(ValueError, match="You don't have enough cards to exchange"):
        player1.exchange(board, [0, 1, 2, 3], [0, 1, 2, 3])


def test_exchange_not_enough_market_cards(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    board.market = [Card(Resource.SPICES), Card(Resource.SPICES)]
    with pytest.raises(ValueError, match="There's not enough cards on the market to exchange"):
        player1.exchange(board, [0, 1, 2], [0, 1, 2])


def test_exchange_mixed_cards(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.CLOTH), Card(Resource.SPICES)]
    board.market = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES),
                    Card(Resource.SPICES)]
    player1.herd = [Card(Resource.CAMEL), Card(Resource.CAMEL)]
    player1.exchange(board, [1, 99], [0, 1])
    assert player1.hand == [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    assert player1.herd == [Card(Resource.CAMEL)]
    assert board.market == [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.CAMEL),
                            Card(Resource.CLOTH)]


def test_exchange_same_goods(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.CLOTH), Card(Resource.CLOTH)]
    board.market = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES),
                    Card(Resource.SPICES)]

    with pytest.raises(ValueError, match="You can't exchange the same type of card"):
        player1.exchange(board, [0, 1], [0, 1])


def test_exchange_one_card(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.CLOTH), Card(Resource.CLOTH)]
    board.market = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES),
                    Card(Resource.SPICES)]
    with pytest.raises(ValueError, match="You must exchange at least two cards"):
        player1.exchange(board, [0], [0, 1])

def test_exchange_camels(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.CLOTH), Card(Resource.CLOTH)]
    board.market = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.CAMEL)]
    with pytest.raises(ValueError, match="You can't exchange camels"):
        player1.exchange(board, [0, 2], [0, 99])

def test_sell_not_enough_cards_from_type(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.CLOTH), Card(Resource.CLOTH)]
    with pytest.raises(ValueError, match="You don't have enough cards of this type"):
        player1.sell(board, Resource.LEATHER, 2)


def test_sell_zero_cards(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.CLOTH), Card(Resource.CLOTH)]
    with pytest.raises(ValueError, match="You can't sell less than one card"):
        player1.sell(board, Resource.SPICES, 0)


def test_sell_one_expensive_resource(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.GOLD)]
    with pytest.raises(ValueError, match="You must sell at least two cards of this type"):
        player1.sell(board, Resource.GOLD, 1)


def test_sell_happy(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.SPICES)]
    board.tokens[Resource.TOKENX3] = [GameToken(Resource.TOKENX3, 2), GameToken(Resource.TOKENX3, 3)]
    player1.sell(board, Resource.GOLD, 3)
    assert player1.hand == [Card(Resource.SPICES)]
    assert player1.token_pile == [GameToken(Resource.GOLD, 6), GameToken(Resource.GOLD, 6), GameToken(Resource.GOLD, 5),
                                  GameToken(Resource.TOKENX3, 2)]


def test_take_one_resource_hand_too_big(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.SPICES),Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    with pytest.raises(ValueError, match="You can't have more than seven cards in your hand"):
        player1.take_one_resource(board, 0)

def test_take_one_resource_happy(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES)]
    board.market = [Card(Resource.CAMEL), Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.GOLD),
                    Card(Resource.SPICES)]
    player1.take_one_resource(board, 2)
    assert player1.hand == [Card(Resource.SPICES), Card(Resource.GOLD)]
    assert board.market == [Card(Resource.CAMEL), Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.SPICES)]

def test_take_all_camels_happy(game_objects):
    deck, board, player1, player2 = game_objects
    board.market = [Card(Resource.SPICES), Card(Resource.CAMEL), Card(Resource.CAMEL), Card(Resource.CAMEL), Card(Resource.GOLD)]
    player1.herd = [Card(Resource.CAMEL)]
    player1.take_all_camels(board)
    assert player1.herd == [Card(Resource.CAMEL), Card(Resource.CAMEL), Card(Resource.CAMEL), Card(Resource.CAMEL)]
    assert board.market == [Card(Resource.SPICES), Card(Resource.GOLD)]

def test_take_all_camels_no_camels_left(game_objects):
    deck, board, player1, player2 = game_objects
    board.market = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.GOLD)]
    with pytest.raises(ValueError, match="There's no camels to take"):
        player1.take_all_camels(board)

def test_round_end_no_cards_left_happy(game_objects):
    deck, board, player1, player2 = game_objects
    board.market = [Card(Resource.CAMEL), Card(Resource.CAMEL), Card(Resource.CAMEL), Card(Resource.CAMEL),
                    Card(Resource.SPICES)]
    deck.deck = []
    player1.take_one_resource(board, 4)
    assert board.round_end_check() == True

def test_round_end_take_camels_with_empty_deck(game_objects):
    deck, board, player1, player2 = game_objects
    board.market = [Card(Resource.CAMEL), Card(Resource.CAMEL), Card(Resource.CAMEL), Card(Resource.CAMEL), Card(Resource.CAMEL)]
    deck.deck = []
    player1.take_all_camels(board)
    assert board.round_end_check() == True

def test_round_end_exchange_no_cards_left(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    board.market = [Card(Resource.CLOTH), Card(Resource.CLOTH), Card(Resource.CLOTH), Card(Resource.CLOTH), Card(Resource.CLOTH)]
    deck.deck = []
    player1.exchange(board, [0,1],[0,1])
    assert board.round_end_check() == False
    assert board.market == [Card(Resource.CLOTH), Card(Resource.CLOTH), Card(Resource.CLOTH), Card(Resource.SPICES), Card(Resource.SPICES)]

def test_round_end_sell_with_empty_deck(game_objects):
    deck, board, player1, player2 = game_objects
    board.market = [Card(Resource.CLOTH), Card(Resource.CLOTH), Card(Resource.CLOTH), Card(Resource.CLOTH),
                    Card(Resource.CLOTH)]
    player1.hand = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.GOLD)]
    deck.deck = []
    player1.sell(board, Resource.SPICES, 4)
    assert board.round_end_check() == False
