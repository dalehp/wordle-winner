"""A _very_ basic wordle strategy

Chooses the first possible word in the list.
"""

from wordle.state import GameState
from wordle.words import ALLOWED_TARGETS


def is_word_possible(gs: GameState, word: str) -> bool:
    for i, c in enumerate(gs.exact):
        if c is None:
            continue
        if word[i] != c:
            return False

    if set(word) & (gs.misses - gs.in_word.keys()):
        return False

    for c, count in gs.in_word.items():
        guess_count = word.count(c)
        if c in gs.misses:
            # We know the exact number in the word
            if guess_count != count:
                return False
        else:
            if guess_count < count:
                return False

    return True


def strategy(gs: GameState) -> str:
    for word in ALLOWED_TARGETS:
        if is_word_possible(gs, word):
            return word
