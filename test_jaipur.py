import pytest

from Jaipur.board import Board
from Jaipur.card import Card
from Jaipur.deck import Deck
from Jaipur.player import Player
from Jaipur.resource import Resource
from Jaipur.token import Token


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
    with pytest.raises(ValueError, match='No tenes suficientes camellos'):
        player1.exchange(board, [0, 99, 99], [0, 1, 2])


def test_exchange_not_equal_amount(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    with pytest.raises(ValueError, match='Tenes que intercambiar la misma cantidad de cartas'):
        player1.exchange(board, [0, 1, 2], [0, 1, 2, 3])


def test_exchange_not_enough_player_cards(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    with pytest.raises(ValueError, match='No tenes suficientes cartas para intercambiar'):
        player1.exchange(board, [0, 1, 2, 3], [0, 1, 2, 3])


def test_exchange_not_enough_market_cards(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES)]
    board.market = [Card(Resource.SPICES), Card(Resource.SPICES)]
    with pytest.raises(ValueError, match='No hay suficientes cartas en el mercado para intercambiar'):
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

    with pytest.raises(ValueError, match='No se puede cambiar por el mismo tipo de cartas'):
        player1.exchange(board, [0, 1], [0, 1])


def test_exchange_one_card(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.CLOTH), Card(Resource.CLOTH)]
    board.market = [Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES), Card(Resource.SPICES),
                    Card(Resource.SPICES)]
    with pytest.raises(ValueError, match='Necesitas intercambiar al menos dos cartas'):
        player1.exchange(board, [0], [0, 1])


def test_sell_not_enough_cards_from_type(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.CLOTH), Card(Resource.CLOTH)]
    with pytest.raises(ValueError, match='No tenes suficientes cartas de este tipo'):
        player1.sell(board, Resource.LEATHER, 2)


def test_sell_zero_cards(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.SPICES), Card(Resource.CLOTH), Card(Resource.CLOTH)]
    with pytest.raises(ValueError, match='No se puede vender menos de 1'):
        player1.sell(board, Resource.SPICES, 0)


def test_sell_one_expensive_resource(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.GOLD)]
    with pytest.raises(ValueError, match="Tenes que vender al menos 2 cartas de este tipo"):
        player1.sell(board, Resource.GOLD, 1)


def test_sell_happy(game_objects):
    deck, board, player1, player2 = game_objects
    player1.hand = [Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.GOLD), Card(Resource.SPICES)]
    board.tokens[Resource.TOKENX3] = [Token(Resource.TOKENX3, 2), Token(Resource.TOKENX3, 3)]
    player1.sell(board, Resource.GOLD, 3)
    assert player1.hand == [Card(Resource.SPICES)]
    assert player1.token_pile == [Token(Resource.GOLD, 6), Token(Resource.GOLD, 6), Token(Resource.GOLD, 5),
                                  Token(Resource.TOKENX3, 2)]
