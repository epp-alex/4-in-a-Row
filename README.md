# 🔴 4 in a Row – Bitboard + PVS

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Qt](https://img.shields.io/badge/GUI-PyQt5%20%7C%20PySide6-green?logo=qt)
![Compiler](https://img.shields.io/badge/Compiler-Nuitka-ff69b4)
![License](https://img.shields.io/badge/License-MIT-yellow)

Ein performantes **Vier-Gewinnt-Spiel** (10×10 Spielfeld, 4 gewinnt) entwickelt in Python und mit **Nuitka** zu autarken, nativen Anwendungen kompiliert.

Das Spiel besitzt eine extrem starke KI-Engine basierend auf **Principal Variation Search (PVS)** mit Iterative Deepening, Bitboard-Evaluierung und Killer-Move-Heuristiken.

---

## 📥 Downloads (Standalone Executables)

Keine Python-Installation erforderlich! Lade einfach das Paket für dein Betriebssystem im **[Releases-Bereich](../../releases)** herunter:

| Plattform | Release-Archiv | Inhalt & Anleitung |
| :--- | :--- | :--- |
| 🪟 **Windows** | `4_in_a_Row.7z` | Archiventpacken & `4_in_a_Row.exe` per Doppelklick starten. |
| 🍎 **macOS** | `4_in_a_Row.dmg` | Disk Image öffnen & `4_in_a_Row.app` in den Programme-Ordner ziehen. |
| 🐧 **Linux** | `4_in_a_Row.tar.gz` | Entpacken & ausführen:<br>`tar -xzf 4_in_a_Row.tar.gz`<br>`chmod +x 4_in_a_Row && ./4_in_a_Row` |

> **Linux Note:** Die Binary enthält alle nötigen `xcb`-Systembibliotheken (`libxcb-cursor.so.0`) und läuft ohne zusätzliche Abhängigkeiten direkt out-of-the-box!

---

## 🎮 Spielanleitung & Steuerung

* **Spielen:** Klicke auf den **↓** Pfeil über einer Spalte, um deinen Spielstein (🔴 Rot) einzuwerfen.
* **Ziel:** Bringe **4 Steine in eine Reihe** – horizontal, vertikal oder diagonal.
* **Hervorhebung:** Die gewinnenden Steine werden am Ende **gold markiert**.

| Tastenkürzel / Menü | Funktion |
| :--- | :--- |
| `Strg + Z` | **Rückgängig:** Nimmt deinen letzten Zug und die Antwort der KI gleichzeitig zurück. |
| `Menü → Neues Spiel` | Startet ein neues Match mit den aktuellen Einstellungen. |
| `Menü → Sprache` | Welchsle nahtlos zwischen 14 Sprachen im laufenden Spiel. |

---

## ✨ Highlights & Features

* **10×10 Grid:** Großes Spielfeld für tiefere taktische Möglichkeiten als das klassische 7×6.
* **3 KI-Schwierigkeiten:** Von Anfänger-freundlich bis extrem stark.
* **2-Spieler-Modus:** Lokales Match gegen einen Freund (Mensch vs. Mensch).
* **Persistente Einstellungen:** Sprache, Schwierigkeit und Spielmodus werden automatisch im System-Konfigurationspfad gespeichert.
* **14 Sprachen:** 🇩🇪 🇬🇧 🇫🇷 🇪🇸 🇮🇹 🇳🇱 🇵🇱 🇵🇹 🇷🇺 🇺🇦 🇬🇷 🇭🇺 🇹🇷 🇨🇿

---

## 🤖 KI-Engine & Bitboard Architecture

Die KI verwendet moderne Engine-Techniken für maximale Spielstärke bei minimaler Bedenkzeit:

| Level | Suchtiefe | Bedenkzeit | Spielstärke |
| :--- | :--- | :--- | :--- |
| **Einfach** | Depth 6 | ~1.0s | Gelegentliche strategische Fehler |
| **Schwer** | Depth 12 | ~2.5s | Sehr solide, übersieht fast keine Drohungen |
| **Experte** | Depth 16 | ~5.0s | Erkennt komplexe Muster inklusive Lücken-Fallen (`x_xx`) |

### Technische Details:
* **Principal Variation Search (PVS)** mit Iterative Deepening
* **Transposition Table (TT)** mit Exact/Lower/Upper-Bound Flags
* **Killer-Move Heuristic** für starkes Alpha-Beta-Pruning
* Exakte **Bitboard-Gewinnerkennung** mit Zeilen-Boundary-Masken
* **Pattern-Window-Evaluation** zur Erkennung verdeckter Drohungen

---

## 🛠️ Aus dem Quellcode ausführen (Developer)

Voraussetzungen: Python 3.8+ und PyQt5 oder PySide6.

```bash
# Repository klonen
git clone [https://github.com/DeinUsername/4_in_a_Row.git](https://github.com/DeinUsername/4_in_a_Row.git)
cd 4_in_a_Row

# Abhängigkeiten installieren
pip install PyQt5 zstandard

# Spiel starten

python 4_in_a_Row.py

<img width="616" height="767" alt="Screenshot 2026-09-13 210822" src="https://github.com/user-attachments/assets/62aba1da-e980-4e2c-b856-ca71b504fc7e" />
