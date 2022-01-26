from wordle.state import GameState
from wordle.strategies.first_word import is_word_possible


def test_is_word_possible():
    gs = GameState(
        exact=[None, "e", None, None, None], in_word={"e": 1}, misses={"e", "r", "v"}
    )
    assert is_word_possible(gs, "being") == True


def test_is_word_possible_double_letter():
    gs = GameState(
        exact=[None, "e", None, None, None],
        in_word={"e": 1},
        misses={"f", "e", "r", "v"},
    )
    assert is_word_possible(gs, "jewel") == False
