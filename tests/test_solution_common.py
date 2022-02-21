from wordle.state import GameState
from wordle.strategies.first_word import is_word_possible


def test_is_word_possible():
    gs = GameState(
        exact=[None, "e", None, None, None],
        not_in_position=[set(), set(), set(), set(), set()],
        in_word={"e": 1},
        misses={"e", "r", "v"},
    )
    assert is_word_possible(gs, "being") == True


def test_is_word_possible_double_letter():
    gs = GameState(
        exact=[None, "e", None, None, None],
        not_in_position=[set(), set(), set(), set(), set()],
        in_word={"e": 1},
        misses={"f", "e", "r", "v"},
    )
    assert is_word_possible(gs, "jewel") == False


def test_is_word_possible_known_in_word_no_miss():
    gs = GameState(
        exact=[None, None, None, None, None],
        not_in_position=[set(), set(), set(), set(), set()],
        in_word={"o": 1},
        misses={"a", "g", "l", "w"},
    )
    assert is_word_possible(gs, "thief") == False


def test_is_word_possible_not_in_position():
    gs = GameState(
        exact=[None, "o", None, None, None],
        not_in_position=[set(), set(), {"o"}, {"e", "o"}, set()],
        in_word={"e": 1, "o": 1},
        misses={"a", "b", "u", "t", "p", "r", "i", "n", "h", "v", "l"},
    )
    assert is_word_possible(gs, "modem") == False
