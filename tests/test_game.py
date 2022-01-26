import pytest

from wordle.game import CharacterState as Cs
from wordle.game import guess


@pytest.mark.parametrize(
    "target,guess_word,result",
    [
        # Test characters in word
        ("backs", "stack", [Cs.IN_WORD, Cs.MISS, Cs.IN_WORD, Cs.IN_WORD, Cs.IN_WORD]),
        # Test exact characters
        ("backs", "lacks", [Cs.MISS, Cs.EXACT, Cs.EXACT, Cs.EXACT, Cs.EXACT]),
        # Test mix
        ("exact", "entry", [Cs.EXACT, Cs.MISS, Cs.IN_WORD, Cs.MISS, Cs.MISS]),
        # Test double letter in target, exact hit of one
        ("boost", "boats", [Cs.EXACT, Cs.EXACT, Cs.MISS, Cs.IN_WORD, Cs.IN_WORD]),
        # Test double letter in target, exact hit of both
        ("boost", "boots", [Cs.EXACT, Cs.EXACT, Cs.EXACT, Cs.IN_WORD, Cs.IN_WORD]),
        # Test double letter in target, one exact, one elsewhere
        ("boost", "bozos", [Cs.EXACT, Cs.EXACT, Cs.MISS, Cs.IN_WORD, Cs.IN_WORD]),
        # Test double letter in _word, exact hit of one
        ("boats", "boost", [Cs.EXACT, Cs.EXACT, Cs.MISS, Cs.IN_WORD, Cs.IN_WORD]),
        # Test double letter in guess, one exact, one elsewhere
        ("bozos", "boost", [Cs.EXACT, Cs.EXACT, Cs.IN_WORD, Cs.IN_WORD, Cs.MISS]),
    ],
)
def test_guess(target: str, guess_word: str, result: list[Cs]):
    actual = guess(target=target, word=guess_word)
    assert actual == result
