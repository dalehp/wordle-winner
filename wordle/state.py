from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class CharacterState(Enum):
    MISS = auto()
    IN_WORD = auto()
    EXACT = auto()

    def __str__(self):
        return {
            CharacterState.MISS: "x",
            CharacterState.IN_WORD: "o",
            CharacterState.EXACT: "O",
        }[self]


@dataclass
class GameState:
    # The exact positions of the characters known for sure
    exact: list[Optional[str]] = field(default_factory=lambda: [None] * 5)
    # The characters ruled out of each position (but not ruled out of the word)
    not_in_position: list[set[str]] = field(
        default_factory=lambda: [set(), set(), set(), set(), set()]
    )
    # Number of times in word (including known exact)
    in_word: dict[str, int] = field(default_factory=dict)
    # Letter has drawn a blank. Does _not_ mean it's not in the word
    # at all, it could mean e.g. you guessed "foods" but the game says
    # only 1 'o'
    misses: set[str] = field(default_factory=set)

    def __add__(self, o: GameState) -> GameState:
        exact = [c1 or c2 for c1, c2 in zip(self.exact, o.exact)]
        not_in_position = [
            n1 | n2 for n1, n2 in zip(self.not_in_position, o.not_in_position)
        ]
        in_word = {
            c: max(self.in_word.get(c, 0), o.in_word.get(c, 0))
            for c in self.in_word.keys() | o.in_word.keys()
        }
        misses = self.misses | o.misses
        return GameState(
            exact=exact, not_in_position=not_in_position, in_word=in_word, misses=misses
        )
