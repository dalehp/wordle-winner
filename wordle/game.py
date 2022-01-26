from __future__ import annotations

from statistics import mean
from typing import Callable, Optional

from pyparsing import Char

from wordle.state import CharacterState, GameState
from wordle.strategies.first_word import strategy as fw_strat
from wordle.words import ALLOWED_TARGETS

# A callable that calculates the next guess from current game state
Strategy = Callable[[GameState], str]


def _get_occurrance_indices(word: str, char: str) -> list[int]:
    return [i for i, c in enumerate(word) if c == char]


def _game_state_from_character_state(cs: list[CharacterState], word: str) -> GameState:
    exact: list[Optional[str]] = [None] * 5
    in_word: dict[str, int] = {}
    misses = set()
    for i, (state, c) in enumerate(zip(cs, word)):
        if state == CharacterState.EXACT:
            exact[i] = c
            in_word[c] = in_word.get(c, 0) + 1
        elif state == CharacterState.IN_WORD:
            in_word[c] = in_word.get(c, 0) + 1
        elif state == CharacterState.MISS:
            misses.add(c)
        else:
            raise ValueError(f"Unhandled state {state}")
    return GameState(exact=exact, in_word=in_word, misses=misses)


def guess(target: str, word: str) -> list[CharacterState]:
    guess_pos_to_target_pos = {}
    guess_state = [CharacterState.MISS] * 5

    for i, c in enumerate(word):
        if target[i] == c:
            guess_state[i] = CharacterState.EXACT
            guess_pos_to_target_pos[i] = i

    for j, ch in enumerate(word):
        if j in guess_pos_to_target_pos:
            continue
        if ch in target:
            occurances = _get_occurrance_indices(target, ch)
            while occurances:
                target_position = occurances.pop()
                if target_position in guess_pos_to_target_pos.values():
                    continue
                guess_pos_to_target_pos[j] = target_position
                guess_state[j] = CharacterState.IN_WORD

    return guess_state


def play_game(
    strategy: Strategy, target: str
) -> tuple[Optional[int], list[tuple[str, str]]]:
    state = GameState()
    guesses = []

    for guess_no in range(6):
        guess_word = strategy(state)
        if guess_word == target:
            guesses.append((guess_word, [CharacterState.EXACT] * 5))
            break
        char_state = guess(target=target, word=guess_word)
        state += _game_state_from_character_state(char_state, guess_word)
        guesses.append((guess_word, char_state))

    results = [(w, "".join(str(s) for s in ss)) for w, ss in guesses]
    if guess_word != target:
        return None, results
    return guess_no, results


def main():
    guesses = []
    failures = 0
    for tgt in ALLOWED_TARGETS:
        num_guesses, result = play_game(fw_strat, tgt)
        if num_guesses is None:
            print(tgt, result)
            failures += 1
            continue
        guesses.append(num_guesses)
    print(mean(guesses))
    print(
        f"missed {failures} out of {len(ALLOWED_TARGETS)}. "
        f"{failures/len(ALLOWED_TARGETS):%}"
    )
