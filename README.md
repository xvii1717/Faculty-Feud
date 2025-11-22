# Faculty Feud — MVP Scaffold

This repository contains a minimal MVP scaffold for a Family Feud-style game.

Files added:

- `faculty_feud.py` — Pygame-based game skeleton. Controls:
  - `A` = Team A buzz
  - `L` = Team B buzz
  - Click an answer box to reveal it (adds points to active team)
  - `X` = give active team a strike
  - `R` = reset round
  - `ESC` = quit
- `editor.py` — simple Tkinter editor to add rounds and answers to `data/questions.json`.
- `data/questions.json` — sample round data.
- `requirements.txt` — lists `pygame`.

Run locally (PowerShell):
```powershell
pip install -r requirements.txt
python .\faculty_feud.py
```

To edit/add questions:
```powershell
python .\editor.py
```

This is an initial scaffold implementing the MVP items:
- editable questions (via `editor.py`)
- two teams and scores
- buzzer keys to decide who answers
- reveal answers by clicking
- strike key (`X`) increments strikes

Next steps: add persistent team names, nicer UI, fullscreen toggle, and buzzer hardware support.
# Faculty-Feud
The official Faculty Feud code for James Madison High School