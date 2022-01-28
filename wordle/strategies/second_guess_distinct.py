"""A wordle strategy that tries to rule out letters early

Guess first word in the word list.
Second guess picks a word with no common letters to the first.
Third onwards reverts to the 'first word' strategy.
"""

from wordle.state import GameState
from wordle.strategies import first_word
from wordle.words import ALLOWED_TARGETS


def find_distinct_word(gs: GameState, guess_no: int) -> str:
    for word in ALLOWED_TARGETS:
        if not any(c in gs.in_word.keys() | gs.misses for c in word):
            return word
    raise RuntimeError("Something went wrong - no possible words")


def strategy(gs: GameState, guess_no: int) -> str:
    if guess_no in (1, 2):
        return find_distinct_word(gs, guess_no)
    return first_word.strategy(gs, guess_no)
