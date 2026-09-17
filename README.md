# 🔴 4 in a Row – Bitboard + PVS

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Qt](https://img.shields.io/badge/GUI-PyQt5%20%7C%20PySide6-green?logo=qt)
![Compiler](https://img.shields.io/badge/Compiler-Nuitka-ff69b4)
![License](https://img.shields.io/badge/License-MIT-yellow)

A highly optimized **Connect Four-style puzzle game** (10×10 grid, 4 in a row to win) built with Python and compiled into standalone, native executables using **Nuitka**.

Features a powerful AI engine powered by **Principal Variation Search (PVS)** with iterative deepening, bitboard evaluation, and killer-move heuristics.


## 📥 Download & Run (No Python Needed)

No installation required! Simply download the package for your platform from the **[Releases](../../releases)** section:

| Platform | File / Archive | Instructions |
| :--- | :--- | :--- |
| 🪟 **Windows** | `4_in_a_Row.7z` | Extract the archive and double-click `4_in_a_Row.exe` to run. |
| 🍎 **macOS** | `4_in_a_Row.dmg` | Open the `.dmg` image and drag `4_in_a_Row.app` to your Applications folder *(Right-click → Open if prompted by Gatekeeper)*. |
| 🐧 **Linux** | `4_in_a_Row.tar.gz` | Extract and execute via terminal:<br>`tar -xzf 4_in_a_Row.tar.gz`<br>`chmod +x 4_in_a_Row && ./4_in_a_Row` |

> **Linux Note:** Thanks to embedded `libxcb-cursor` libraries, the Linux binary runs instantly out-of-the-box on modern distributions without installing system dependencies!

---

## 🎮 How to Play & Controls

* **Gameplay:** Click the **↓** arrow button above a column to drop your piece (🔴 Red).
* **Objective:** Connect **4 pieces in a row**—horizontally, vertically, or diagonally.
* **Victory:** The winning sequence is **highlighted in gold** when the game ends.

| Action / Shortcut | Function |
| :--- | :--- |
| `Click ↓ Button` | Drop piece into the selected column |
| `Ctrl + Z` / `Menu → Undo` | **Undo Move:** Takes back your move and the AI's response simultaneously |
| `Menu → New Game` | Start a fresh game with current settings |
| `Menu → Language` | Switch seamlessly between 14 supported languages on the fly |

---

## ✨ Key Features

* **10×10 Board:** Expanded grid offering deeper tactical gameplay than the classic 7×6 board.
* **3 AI Difficulty Levels:** Tailored search depth and thinking time for all player skill levels.
* **Player vs. Player:** Play locally with a friend on the same computer (Human vs. Human mode).
* **Persistent Settings:** Language, difficulty, and game mode are automatically saved across sessions.
* **14 Built-in Languages:** 🇩🇪 🇬🇧 🇫🇷 🇪🇸 🇮🇹 🇳🇱 🇵🇱 🇵🇹 🇷🇺 🇺🇦 🇬🇷 🇭🇺 🇹🇷 🇨🇿

---

## 🤖 AI Engine & Performance

The AI engine utilizes modern chess-engine algorithms for strong gameplay and fast decision-making:

| Level | Search Depth | Thinking Time | Engine Behavior |
| :--- | :--- | :--- | :--- |
| **Easy** | Depth 6 | ~1.0 s | Casual play, makes occasional strategic mistakes |
| **Hard** | Depth 12 | ~2.5 s | Solid play, rarely misses immediate threats |
| **Expert** | Depth 16 | ~5.0 s | Master level, detects complex gap traps like `x_xx` |

### Technical Engine Architecture:
* **Principal Variation Search (PVS)** with Iterative Deepening
* **Transposition Table (TT)** with exact/lower/upper bound flags
* **Killer-Move Heuristic** for enhanced Alpha-Beta pruning efficiency
* Exact **Bitboard Win Detection** using row-boundary masking
* **Pattern Window Evaluation** for detecting split-threat combinations

---
