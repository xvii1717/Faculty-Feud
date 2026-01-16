# JMHS Faculty Feud
## 📂 Files

| File | Description |
|------|-------------|
| `setup.exe` | Run this **first** to add rounds, questions, answers, and point values. |
| `game.exe` | Run this to play the game with teams and buzzers. |
| `data/questions.json` | Stores all your rounds and answers (auto-created by setup). |

---

##  Setup: Adding Rounds

Before playing, you **must run `setup.exe`** to add questions and point values.

1. Double-click `setup.exe`.
2. Click **Add Round**.
3. Add a **multiplier** (optional).
4. Enter the **question text**.
5. Add **answers** one by one:
   - Enter the answer text.
   - Enter **points** for this answer.
   - Make sure to press **save question** when done
6. Repeat to add more rounds.
7. Close the window when done. All data is saved automatically to `questions.json`.

> Tip: You can come back later and add more rounds — the game will use all rounds in the file.

---

##  Playing the Game

1. Double-click `game.exe`.
2. Enter the names of the **two teams** when prompted.
3. Teams take turns **buzzing in** to answer questions.
4. Each round will show a question. Teams try to guess answers.
5. Points for each answer are added to the team score automatically.

---

###  Hotkeys / Controls


 Buzz in using the left and right arrow keys 
 Add an X for an incorrect answer | `X` | 
 Press backspace to mark answer as incorrect but does not add it to team's total Xs (should be used ONLY after the initial buzz-in, use `X` instead while teams are playing)
 Answer numbers correspond to numbers (ex. press 1 to reveal the top answer)
 Move to next round after playing | Space |

---

###  Gameplay Flow

1. A round question appears.
2. Teams try to guess the top answers.
3. The first team to buzz can answer first.
4. Correct answers are revealed, and points are added.
5. Move to the next round until all rounds are finished.
6. The team with the highest total score after all of the rounds **wins**! (or you can finish the game at any time by pressing esc)


---

##  Tips

- Manually edit points at any time with the button on the top right corner of the screen!
- Run `setup.exe` **before** `game.exe` — otherwise, the game will have no questions or points.
- Make sure both `setup.exe` and `game.exe` are in the same folder as the `data` directory.
- You can add rounds anytime — the game will pick up new questions automatically.
- Keep your questions fun and varied for maximum enjoyment!

---

##  Requirements

- Nothing extra needed — just double-click the `.exe` files.
- These are **standalone executables**, so you don’t need Python or any other software to play.
