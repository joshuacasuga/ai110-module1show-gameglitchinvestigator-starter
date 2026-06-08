# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## Document Your Experience

Purpose. The game is a number guessing game built with Streamlit. The user guesses a number in a range. The game gives a hint after each guess and tracks the score.

Bugs found.
1. The hints were backwards. A guess that was too high told the user to go higher.
2. New Game did not work after a game ended. The secret and attempts reset but the game stayed stuck in the won or lost state.
3. The secret was sometimes compared as a string, which broke the hints on some turns.

Fixes applied.
1. Rewrote check_guess to compare numbers and return the correct hint direction.
2. Made New Game reset the full state, including status, score, and history.
3. Moved the game logic into logic_utils.py and added pytest tests.

## Demo Walkthrough

Sample game on Normal difficulty. Range is 1 to 100. The secret for this run is 42.

1. The app loads. The score is 0.
2. User guesses 50. The game says Too High, Go Lower. The score is now 5.
3. User guesses 30. The game says Too Low, Go Higher. The score is now 0.
4. User guesses 42. The game says Correct. It shows You won. The final score is 50.
5. The game stops taking guesses and asks the user to start a new game.
6. User clicks New Game. The secret, attempts, score, and history reset. The user can guess again right away.

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
