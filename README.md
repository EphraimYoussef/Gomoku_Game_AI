# Gomoku with AI (Minimax & Alpha‑Beta) GUI

A modern, customizable Gomoku (Five‑in‑a‑Row) game built in Python featuring:

* **Human vs Minimax AI**
* **Minimax AI vs Alpha‑Beta AI**
* Adjustable **board size** (5×5 up to 19×19)
* Configurable **search depth** for AI difficulty
* CustomTkinter‑based GUI with clean, responsive design

---

## Features

* **Interactive GUI**: Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for sleek widgets and theming.
* **AI Algorithms**:

  * **Minimax** (depth‑limited)
  * **Alpha‑Beta Pruning**
* **Game Modes**:

  1. Human vs Minimax AI
  2. Minimax vs Alpha‑Beta AI (watch two AIs duel)
* **Alerts & Feedback**: Pop‑up notifications with sound cues on win, draw, or game over.
* **Threaded AI Play**: Non‑blocking AI computations to keep UI responsive.

---

## Prerequisites

* **Python 3.7+**
* **Windows** (for `winsound.MessageBeep`; cross‑platform support coming)
* **Dependencies** (install via `pip`):

  ```bash
  pip install customtkinter
  ```

> If you encounter installation issues, ensure you have the latest `pip`:
>
> ```bash
> python -m pip install --upgrade pip
> ```

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/EphraimYoussef/Gomoku_Game.git
   cd Gomoku_Game

2. **Install dependencies**

   ```bash
   pip install customtkinter
   ```

3. **Run the game**

   ```bash
   python GomokuGUI.py
   ```

> The GUI will launch, allowing you to select board size, AI depth, and game mode.

---

## Usage

1. **Home Screen**:

   * Enter your desired **Board Size** (default `6`, range `5`–`19`).
   * Enter **AI Depth** (default `2`, minimum `1`). Higher depth → stronger but slower AI.
   * Click **Human VS MiniMax** or **MiniMax VS Alpha‑Beta**.

2. **Gameplay**:

   * **Human vs Minimax**: Click on a grid cell to place your stone (black). The AI (white) will respond.
   * **Minimax vs Alpha‑Beta**: Watch the two AIs play automatically.

3. **Controls**:

   * **Back to Home**: Return to the configuration screen.
   * **Restart**: Reset the board and replay the same mode.

4. **Alerts**:

   * A pop‑up with sound will announce **“You win!”**, **“AI wins!”**, or **“Draw!”**.

---

## Project Structure

```text
├── GomokuGUI.py       # Starts the CustomTkinter GUI (App + pages)
├── GomokuGame.py      # Core game logic & AI implementations
└── README.md          # This documentation
```

---

## How It Works

* **`GomokuGame.py`** encapsulates:

  * `Gomoku` class for board state, move validation, win/draw detection
  * `minimax` (depth‑limited) and `alphaBeta` recursive algorithms with evaluation heuristics
* **`GomokuGUI.py`** builds:

  * A CustomTkinter `App` with **HomePage**, **PageOne** (Human vs Minimax), and **PageTwo** (AI vs AI)
  * Threaded AI loops to prevent UI freezing
  * Custom alert windows (`CustomAlert`) for in‑game notifications

---

## Video
### Example with Board size = 8 * 8 and AI Depth = 2
https://github.com/user-attachments/assets/5706cda7-692d-4435-9f9c-9d09ab61cf26

---

## Contact

For further inquiries or collaboration, please contact:


- **Ephraim Youssef**\
[GitHub Profile](https://github.com/EphraimYoussef)
- **Abdelrahman Kadry**\
[GitHub Profile](https://github.com/Kadry-jr)
- **Ramez Ragaay**\
[GitHub Profile](https://github.com/RamezRagaay)
- **Omar Ahmed**\
[GitHub Profile](https://github.com/Omar-Badwilan)
- **Abdallah Nassar**\
[GitHub Profile](https://github.com/bodawy04)

---

> Enjoy playing Gomoku with AI!
