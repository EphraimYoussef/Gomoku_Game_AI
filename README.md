# Gomoku with AI (Minimax & Alpha‑Beta) GUI

A modern, customizable Gomoku (Five‑in‑a‑Row) game built in Python featuring:

* **Human vs Minimax AI**
* **Minimax AI vs Alpha‑Beta AI**
* Adjustable **board size** (5×5 up to 19×19)
* Configurable **search depth** for AI difficulty
* CustomTkinter‑based GUI with clean, responsive design

---

## 🔧 Features

* **Interactive GUI**: Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for sleek widgets and theming.
* **AI Algorithms**:

  * **Minimax** (depth‑limited)
  * **Alpha‑Beta Pruning**
* **Game Modes**:

  1. Human vs Minimax AI
  2. Minimax vs Alpha‑Beta AI (watch two AIs duel)
* **Alerts & Feedback**: Pop‑up notifications with sound cues on win, draw, or game over.
* **Threaded AI Play**: Non‑blocking AI computations to keep UI responsive.

## 📦 Prerequisites

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

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/EphraimYoussef/gomoku-ai-gui.git
   cd gomoku-ai-gui

2. **Install dependencies**

   ```bash
   pip install customtkinter
   ```

3. **Run the game**

   ```bash
   python GomokuGUI.py
   ```

> The GUI will launch, allowing you to select board size, AI depth, and game mode.

## 🎮 Usage

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

## 🗂️ Project Structure

```text
├── main.py            # Starts the CustomTkinter GUI (App + pages)
├── GomokuGame.py      # Core game logic & AI implementations
├── requirements.txt   # Python dependencies
└── README.md          # This documentation
```

## 🔍 How It Works

* **`GomokuGame.py`** encapsulates:

  * `Gomoku` class for board state, move validation, win/draw detection
  * `minimax` (depth‑limited) and `alphaBeta` recursive algorithms with evaluation heuristics
* **`main.py`** builds:

  * A CustomTkinter `App` with **HomePage**, **PageOne** (Human vs Minimax), and **PageTwo** (AI vs AI)
  * Threaded AI loops to prevent UI freezing
  * Custom alert windows (`CustomAlert`) for in‑game notifications





> Enjoy playing Gomoku with AI!
> Created by Ephraim / Kadry / Ramez / Omar / Abdallah
— Happy coding!
