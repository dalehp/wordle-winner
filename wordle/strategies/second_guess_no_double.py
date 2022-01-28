"""A wordle strategy that tries to rule out letters early

A variation on 'second guess distinct' which also excludes
any words with double letters in the first two guesses.
"""

from wordle.state import GameState
from wordle.strategies import first_word
from wordle.words import ALLOWED_TARGETS


def find_distinct_word(gs: GameState, guess_no: int) -> str:
    for word in ALLOWED_TARGETS:
        if (
            not any(c in gs.in_word.keys() | gs.misses for c in word)
            and len(set(word)) == 5
        ):
            return word
    raise RuntimeError("Something went wrong - no possible words")


def strategy(gs: GameState, guess_no: int) -> str:
    if guess_no in (1, 2):
        return find_distinct_word(gs, guess_no)
    return first_word.strategy(gs, guess_no)
