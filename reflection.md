# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

1. The game would give the wrong hint at times (ie would say higher when it should be lower and vice versa)
2. Pressing the New game button after a losing game does not reset the game
3. If you turn off the "Show hint" button, the game always ends with one guess left

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| guess of 28 | "Go HIGHER!" hint | "Go LOWER!" Hint | none |
| pressed New Game button after a losing game | Game restarts | Game is stuck in losing state | none |
| turn off "Show Hint" and then making 7 guesses | Have one more guess before game ends | Game ends with one guess left | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude for this project

Claude pointed out that `check_guess` returned the hints in the wrong direction. When a guess was too high it told the player to "Go HIGHER!" instead of "Go LOWER!", and that the broken `try/except` was only there to limp through cases where the secret was being passed as a string. It suggested coercing both values with `int()` and flipping the messages. I verified the fix by playing the game (guessing high now correctly says "Go LOWER!") and by writing a pytest case (`test_guess_too_high_says_go_lower`) that passed.

In its first overview, Claude claimed the emoji in `st.set_page_config(page_icon=...)` and the buttons were "mangled" due to an encoding bug. This was misleading. When I checked the actual file and ran the game, the emoji (🎮, 🚀, 🔁) displayed correctly, so there was no encoding problem to fix. It turned out to be an artifact of how the file text was shown to the AI, not a real bug in my code.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed by first reproducing the broken behavior, then confirming the fix two ways: playing the game in the browser and running automated tests. For the hint bug, I guessed a number above the secret and saw it correctly say "Go LOWER!", and for the New Game bug I pressed New Game after a loss and confirmed the game actually restarted instead of staying stuck.

I also wrote pytest cases in `test/test_game_logic.py` and ran them with `pytest`, and all 6 passed. One useful test was `test_new_game_resets_full_state`, which checks that a new game resets `status`, `score`, `attempts`, and `history`. This showed me the real bug wasn't the secret or attempts (those were already being reset) but that `status` was being left on "lost", which is what froze the game.

AI helped me design the tests. To make the New Game reset testable, Claude moved that logic out of the Streamlit UI code into a pure `new_game_state()` function in `logic_utils.py`, then explained that pure functions (ones with no `st.` calls) are easy to unit test because they just take inputs and return outputs. That helped me understand why separating game logic from UI makes a project easier to test.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

The thing that confused me at first is that Streamlit re-runs the entire script from top to bottom every single time you do anything: click a button, type in a box, change the dropdown. So it's not like a normal program that remembers where it left off. I'd tell a friend to picture it like the script has amnesia and reads itself start to finish on every interaction.

That's where session state comes in. Because all your normal variables get wiped on each rerun, you need somewhere to stash the stuff that has to survive, like the secret number, the score, and whether the game is over. `st.session_state` is basically a little backpack that Streamlit carries between reruns so those values don't reset. Once it clicked that the script is constantly restarting, the New Game bug made way more sense, because the only reason the old game stuck around at all was that its `status` was still sitting in that backpack.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

The habit I want to keep is reproducing a bug before I try to fix it. It's tempting to just start changing code the second something looks wrong, but actually triggering the bug first (and then writing a quick test for it) meant I knew for sure when it was really gone instead of just assuming. I also want to keep separating the plain logic from the UI, because the moment the game logic lived in its own file it became way easier to test.

One thing I'd do differently is be more skeptical of the AI's first read of the code. Early on it confidently flagged an "encoding bug" that turned out not to exist, and if I had taken that at face value I would have wasted time chasing a problem that wasn't there. Next time I'll verify each claim against the actual file or the running game before acting on it.

This project changed how I think about AI generated code because it showed me that code can look polished and even claim to be "production-ready" while being full of real bugs. I now treat AI output as a fast first draft from a teammate I still have to double-check, not as an answer I can trust on sight.
