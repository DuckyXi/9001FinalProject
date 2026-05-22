# Five Elements Battlegrounds

A turn-based auto-battler game built with **Python** and **pygame**.

Players buy minions and spells, build a team around the Five Elements, and fight boss rounds across 18 rounds.  
The game supports both **English** and **Chinese**.

## Main Python File

Run:

```bash
python main.py
```

## Python Files

- `main.py`
- `card_pool.py`
- `minion.py`
- `text.py`

## Resource Files

This project uses external resource files for images, sound, music, and font assets.

Depending on the uploaded version, these resources may appear either as folders or as zip archives.

If you see compressed resource files, extract them as follows:

- `image.zip` -> extract into folder `image`
- `sound.zip` -> extract into folder `sound`
- `text.zip` -> extract into folder `text`
- `music1.zip` and `music2.zip` -> extract both into the same folder `music`

After extraction, the project folder should contain:

```text
9001FinalProject/
|-- main.py
|-- card_pool.py
|-- minion.py
|-- text.py
|-- image/
|-- sound/
|-- text/
`-- music/
```

All of these files and folders must stay together in the same project directory.

## How to Run

1. Download or clone this repository.
2. If needed, extract `image.zip`, `sound.zip`, `text.zip`, `music1.zip`, and `music2.zip`.
3. Make sure the extracted folders are in the same directory as `main.py`.
4. Open a terminal in the project folder.
5. Run:

```bash
python main.py
```

## Dependency

This project requires:

- `pygame`

Install it with:

```bash
pip install pygame
```

## Python Knowledge Used

This project applies several Python concepts, including:

- classes and objects
- modular program design
- lists and dictionaries
- functions and state management
- loops and conditional logic
- file reading and writing
- random generation
- GUI and event handling with `pygame`

## Main Gameplay

- Buy minions and spells from the shop
- Build a team around elemental synergies
- Arrange your board and manage your gold
- Fight automatic boss battles every few rounds
- Survive until the final boss and clear Round 18

## Notes

- This is a **GUI application** built with `pygame`.
- It uses **graphics**, **sound effects**, **background music**, and a **custom font**.
- It does **not** use web, networking, or online services.
- The project must be run with the full folder structure preserved.

## Output File

During play, the game creates or appends:

- `run_history.txt`

This file records the team history for each run.
