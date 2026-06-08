"""
Regression tests for the two bugs fixed in the Game Glitch Investigator.

Bug 1: check_guess returned the WRONG direction hint
        (said "Go HIGHER!" when the guess was too high, and vice versa).
Bug 2: the New Game action only reset attempts + secret, leaving status,
        score, and history stuck from the previous game -- so a finished
        game could never actually be replayed.

Run from the project root with:  pytest
"""

import os
import sys

# Make logic_utils.py (one directory up) importable no matter where pytest
# is launched from.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess, new_game_state


# ---------------------------------------------------------------------------
# Bug 1: check_guess hint direction
# ---------------------------------------------------------------------------

def test_guess_too_high_says_go_lower():
    # Guess (75) is above the secret (50) -> player must go LOWER.
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    # Regression guard: must NOT tell the player to go higher.
    assert "HIGHER" not in message


def test_guess_too_low_says_go_higher():
    # Guess (10) is below the secret (50) -> player must go HIGHER.
    outcome, message = check_guess(10, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message


def test_correct_guess_wins():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_check_guess_handles_string_secret():
    # The submit handler used to pass the secret as a string on some turns;
    # check_guess must still compare numerically, not lexicographically
    # (e.g. "9" > "100" is True as strings, but 9 < 100 as ints).
    outcome, _ = check_guess(9, "100")
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# Bug 2: New Game must reset the FULL game state
# ---------------------------------------------------------------------------

def test_new_game_resets_full_state():
    state = new_game_state(1, 100)
    assert state["status"] == "playing"   # was stuck on "won"/"lost" before
    assert state["score"] == 0            # used to carry over
    assert state["attempts"] == 0
    assert state["history"] == []         # used to carry over


def test_new_game_secret_respects_difficulty_range():
    # Easy difficulty is 1-20; the new secret must fall inside the given range
    # (the old code hardcoded random.randint(1, 100)).
    for _ in range(100):
        state = new_game_state(1, 20)
        assert 1 <= state["secret"] <= 20
