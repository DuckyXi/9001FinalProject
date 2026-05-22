# Five Elements Battlegrounds

A turn-based Python auto-battler built with **pygame**.  
The player buys minions and spells, arranges a team, and fights boss rounds across 18 rounds.

This project supports **English** and **Chinese**.

## Main File

Run:

```bash
python main.py
```

## Project Files

Python code files:

- `main.py`
- `card_pool.py`
- `minion.py`
- `text.py`

Resource archives uploaded separately:

- `image.zip`
- `music.zip`
- `sound.zip`
- `text.zip`

## Important Setup Step

Before running the game, you must extract the resource zip files so that the project folder looks like this:

```text
finalprogram/
├── main.py
├── card_pool.py
├── minion.py
├── text.py
├── image/
├── music/
├── sound/
└── text/
```

In other words:

- extract `image.zip` into an `image` folder
- extract `music1.zip` and `music2.zip` into the `music` folder.
- extract `sound.zip` into a `sound` folder
- extract `text.zip` into a `text` folder

These folders must stay in the same directory as `main.py`.

## How to Run

1. Download or clone this repository.
2. Extract `image.zip`, `music.zip`, `sound.zip`, and `text.zip`.
3. Make sure the extracted folders are in the same folder as `main.py`.
4. Open a terminal in the project folder.
5. Run:

```bash
python main.py
```

## Dependency

This project uses the external library:

- `pygame`

Install it with:

```bash
pip install pygame
```

## Built-in Python Libraries Used

- `random`
- `copy`
- `math`
- `os`
- `sys`
- `datetime`

## Features

- Turn-based auto-battler gameplay
- Boss battles
- Minion and spell system
- English / Chinese language support
- Sound effects and background music
- Run history export to `run_history.txt`

## Notes for Running

- This is a **GUI application** built with `pygame`.
- It uses **graphics**, **sound effects**, **background music**, and a **custom font**.
- It does **not** use web, networking, or online features.
- The resource folders must remain together with the Python files after extraction.

## Output File

During play, the program creates/appends:

- `run_history.txt`

This file stores the history of each run.
