#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import time
import math
import random
import copy

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QGridLayout, QVBoxLayout, QMessageBox
)
from PySide6.QtGui import QFont, QAction
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint

# — Spielregeln —
ROWS       = 10
COLS       = 10
WIN_COUNT  = 4
HUMAN      = 1
AI_PLAYER  = 2

# — Basis-Suchparameter —
WIN_SCORE  = 10_000_000
INF        = 1_000_000_000

# — Drei KI-Schwierigkeiten —
DIFFICULTIES = {
    "Einfach": {"max_depth": 6,  "time_budget": 1.0},
    "Schwer":  {"max_depth": 12, "time_budget": 2.5},
    "Experte":  {"max_depth": 16, "time_budget": 5.0},
}

# — Sprachpakete —
LANG = {
    "Deutsch": {
        "flag":             "🇩🇪",
        "title":            "4 in a Row – Bitboard + PVS",
        "menu_mode":        "Modus",
        "menu_diff":        "Schwierigkeit",
        "menu_lang":        "Sprache",
        "menu_new":         "Neues Spiel",
        "menu_undo":        "Rückgängig (Strg+Z)",
        "mode_hvh":         "Mensch vs. Mensch",
        "mode_hvc":         "Mensch vs. Computer",
        "diff_easy":        "Einfach",
        "diff_hard":        "Schwer",
        "diff_exp":         "Experte",
        "status_your_turn": "Du (Rot) bist am Zug",
        "status_p1":        "Spieler 1 (Rot) ist am Zug",
        "status_p2":        "Spieler 2 (Grün) ist am Zug",
        "status_ai":        "Computer (Grün) ist am Zug",
        "win_p1":           "Spieler 1 (Rot) hat gewonnen!",
        "win_p2":           "Spieler 2 (Grün) hat gewonnen!",
        "win_you":          "Du (Rot) hast gewonnen!",
        "win_ai":           "Computer (Grün) hat gewonnen!",
        "draw":             "Unentschieden!",
        "dlg_title":        "Spiel beendet",
        "dlg_question":     "Neue Partie?"
    },
    "English": {
        "flag":             "🇬🇧",
        "title":            "4 in a Row – Bitboard + PVS",
        "menu_mode":        "Mode",
        "menu_diff":        "Difficulty",
        "menu_lang":        "Language",
        "menu_new":         "New Game",
        "menu_undo":        "Undo (Ctrl+Z)",
        "mode_hvh":         "Player vs. Player",
        "mode_hvc":         "Player vs. Computer",
        "diff_easy":        "Easy",
        "diff_hard":        "Hard",
        "diff_exp":         "Expert",
        "status_your_turn": "Your turn (Red)",
        "status_p1":        "Player 1 (Red) turn",
        "status_p2":        "Player 2 (Green) turn",
        "status_ai":        "Computer (Green) turn",
        "win_p1":           "Player 1 (Red) wins!",
        "win_p2":           "Player 2 (Green) wins!",
        "win_you":          "You (Red) win!",
        "win_ai":           "Computer (Green) wins!",
        "draw":             "It's a Draw!",
        "dlg_title":        "Game Over",
        "dlg_question":     "Play again?"
    },
    "Français": {
        "flag":             "🇫🇷",
        "title":            "4 en Ligne – Bitboard + PVS",
        "menu_mode":        "Mode",
        "menu_diff":        "Difficulté",
        "menu_lang":        "Langue",
        "menu_new":         "Nouvelle Partie",
        "menu_undo":        "Annuler (Ctrl+Z)",
        "mode_hvh":         "Humain vs. Humain",
        "mode_hvc":         "Humain vs. Ordi",
        "diff_easy":        "Facile",
        "diff_hard":        "Difficile",
        "diff_exp":         "Expert",
        "status_your_turn": "À toi de jouer (Rouge)",
        "status_p1":        "Joueur 1 (Rouge) joue",
        "status_p2":        "Joueur 2 (Vert) joue",
        "status_ai":        "L'Ordinateur (Vert) joue",
        "win_p1":           "Joueur 1 (Rouge) a gagné !",
        "win_p2":           "Joueur 2 (Vert) a gagné !",
        "win_you":          "Tu as gagné (Rouge) !",
        "win_ai":           "L'Ordinateur (Vert) a gagné !",
        "draw":             "Match nul !",
        "dlg_title":        "Partie terminée",
        "dlg_question":     "Rejouer ?"
    },
    "Español": {
        "flag":             "🇪🇸",
        "title":            "4 en Raya – Bitboard + PVS",
        "menu_mode":        "Modo",
        "menu_diff":        "Dificultad",
        "menu_lang":        "Idioma",
        "menu_new":         "Nueva Partida",
        "menu_undo":        "Deshacer (Ctrl+Z)",
        "mode_hvh":         "Humano vs. Humano",
        "mode_hvc":         "Humano vs. Ordenador",
        "diff_easy":        "Fácil",
        "diff_hard":        "Difícil",
        "diff_exp":         "Experto",
        "status_your_turn": "Tu turno (Rojo)",
        "status_p1":        "Turno del Jugador 1 (Rojo)",
        "status_p2":        "Turno del Jugador 2 (Verde)",
        "status_ai":        "Turno del Ordenador (Verde)",
        "win_p1":           "¡Jugador 1 (Rojo) ha ganado!",
        "win_p2":           "¡Jugador 2 (Verde) ha ganado!",
        "win_you":          "¡Tú (Rojo) has ganado!",
        "win_ai":           "¡El Ordenador (Verde) ha ganado!",
        "draw":             "¡Empate!",
        "dlg_title":        "Juego terminado",
        "dlg_question":     "¿Nueva partida?"
    },
    "Italiano": {
        "flag":             "🇮🇹",
        "title":            "4 in Fila – Bitboard + PVS",
        "menu_mode":        "Modalità",
        "menu_diff":        "Difficoltà",
        "menu_lang":        "Lingua",
        "menu_new":         "Nuova Partita",
        "menu_undo":        "Annulla (Ctrl+Z)",
        "mode_hvh":         "Umano vs. Umano",
        "mode_hvc":         "Umano vs. Computer",
        "diff_easy":        "Facile",
        "diff_hard":        "Difficile",
        "diff_exp":         "Esperto",
        "status_your_turn": "Tocca a te (Rosso)",
        "status_p1":        "Turno del Giocatore 1 (Rosso)",
        "status_p2":        "Turno del Giocatore 2 (Verde)",
        "status_ai":        "Turno del Computer (Verde)",
        "win_p1":           "Il Giocatore 1 (Rosso) ha vinto!",
        "win_p2":           "Il Giocatore 2 (Verde) ha vinto!",
        "win_you":          "Hai vinto tu (Rosso)!",
        "win_ai":           "Il Computer (Verde) ha vinto!",
        "draw":             "Pareggio!",
        "dlg_title":        "Partita terminata",
        "dlg_question":     "Nuova partita?"
    },
    "Nederlands": {
        "flag":             "🇳🇱",
        "title":            "4 op een Rij – Bitboard + PVS",
        "menu_mode":        "Modus",
        "menu_diff":        "Moeilijkheid",
        "menu_lang":        "Taal",
        "menu_new":         "Nieuw Spel",
        "menu_undo":        "Ongedaan maken (Ctrl+Z)",
        "mode_hvh":         "Mens vs. Mens",
        "mode_hvc":         "Mens vs. Computer",
        "diff_easy":        "Makkelijk",
        "diff_hard":        "Moeilijk",
        "diff_exp":         "Expert",
        "status_your_turn": "Jij (Rood) bent aan de beurt",
        "status_p1":        "Speler 1 (Rood) is aan de beurt",
        "status_p2":        "Speler 2 (Groen) is aan de beurt",
        "status_ai":        "Computer (Groen) is aan de beurt",
        "win_p1":           "Speler 1 (Rood) heeft gewonnen!",
        "win_p2":           "Speler 2 (Groen) heeft gewonnen!",
        "win_you":          "Jij (Rood) hebt gewonnen!",
        "win_ai":           "Computer (Groen) heeft gewonnen!",
        "draw":             "Gelijkspel!",
        "dlg_title":        "Spel afgelopen",
        "dlg_question":     "Nieuw spel?"
    },
    "Polski": {
        "flag":             "🇵🇱",
        "title":            "4 w Linii – Bitboard + PVS",
        "menu_mode":        "Tryb",
        "menu_diff":        "Trudność",
        "menu_lang":        "Język",
        "menu_new":         "Nowa Gra",
        "menu_undo":        "Cofnij (Ctrl+Z)",
        "mode_hvh":         "Człowiek vs. Człowiek",
        "mode_hvc":         "Człowiek vs. Komputer",
        "diff_easy":        "Łatwy",
        "diff_hard":        "Trudny",
        "diff_exp":         "Ekspert",
        "status_your_turn": "Twój ruch (Czerwony)",
        "status_p1":        "Ruch Gracza 1 (Czerwony)",
        "status_p2":        "Ruch Gracza 2 (Zielony)",
        "status_ai":        "Ruch Komputera (Zielony)",
        "win_p1":           "Gracz 1 (Czerwony) wygrał!",
        "win_p2":           "Gracz 2 (Zielony) wygrał!",
        "win_you":          "Wygrałeś (Czerwony)!",
        "win_ai":           "Komputer (Zielony) wygrał!",
        "draw":             "Remis!",
        "dlg_title":        "Koniec gry",
        "dlg_question":     "Nowa partia?"
    },
    "Português": {
        "flag":             "🇵🇹",
        "title":            "4 em Linha – Bitboard + PVS",
        "menu_mode":        "Modo",
        "menu_diff":        "Dificuldade",
        "menu_lang":        "Idioma",
        "menu_new":         "Novo Jogo",
        "menu_undo":        "Desfazer (Ctrl+Z)",
        "mode_hvh":         "Humano vs. Humano",
        "mode_hvc":         "Humano vs. Computador",
        "diff_easy":        "Fácil",
        "diff_hard":        "Difícil",
        "diff_exp":         "Perito",
        "status_your_turn": "Sua vez (Vermelho)",
        "status_p1":        "Vez do Jogador 1 (Vermelho)",
        "status_p2":        "Vez do Jogador 2 (Verde)",
        "status_ai":        "Vez do Computador (Verde)",
        "win_p1":           "Jogador 1 (Vermelho) venceu!",
        "win_p2":           "Jogador 2 (Verde) venceu!",
        "win_you":          "Você (Vermelho) venceu!",
        "win_ai":           "Computador (Verde) venceu!",
        "draw":             "Empate!",
        "dlg_title":        "Fim do jogo",
        "dlg_question":     "Novo jogo?"
    }, 

     "Русский": {
        "flag":             "🇷🇺",
        "title":            "4 в Ряд – Bitboard + PVS",
        "menu_mode":        "Режим",
        "menu_diff":        "Сложность",
        "menu_lang":        "Язык",
        "menu_new":         "Новая Игра",
        "menu_undo":        "Отменить (Ctrl+Z)",
        "mode_hvh":         "Игрок против Игрока",
        "mode_hvc":         "Игрок против Робота",
        "diff_easy":        "Легко",
        "diff_hard":        "Сложно",
        "diff_exp":         "Эксперт",
        "status_your_turn": "Ваш ход (Красные)",
        "status_p1":        "Ход Игрока 1 (Красные)",
        "status_p2":        "Ход Игрока 2 (Зеленые)",
        "status_ai":        "Ход Компьютера (Зеленые)",
        "win_p1":           "Игрок 1 (Красные) победил!",
        "win_p2":           "Игрок 2 (Зеленые) победил!",
        "win_you":          "Вы (Красные) победили!",
        "win_ai":           "Компьютер (Зеленые) победил!",
        "draw":             "Ничья!",
        "dlg_title":        "Игра окончена",
        "dlg_question":     "Новая партия?"
    },
    "Українська": {
        "flag":             "🇺🇦",
        "title":            "4 в Ряд – Bitboard + PVS",
        "menu_mode":        "Режим",
        "menu_diff":        "Складність",
        "menu_lang":        "Мова",
        "menu_new":         "Нова Гра",
        "menu_undo":        "Скасувати (Ctrl+Z)",
        "mode_hvh":         "Гравець проти Гравця",
        "mode_hvc":         "Гравець проти Комп'ютера",
        "diff_easy":        "Легко",
        "diff_hard":        "Складно",
        "diff_exp":         "Експерт",
        "status_your_turn": "Ваш хід (Червоні)",
        "status_p1":        "Хід Гравця 1 (Червоні)",
        "status_p2":        "Хід Гравця 2 (Зелені)",
        "status_ai":        "Хід Комп'ютера (Зелені)",
        "win_p1":           "Гравець 1 (Червоні) переміг!",
        "win_p2":           "Гравець 2 (Зелені) переміг!",
        "win_you":          "Ви (Червоні) перемогли!",
        "win_ai":           "Комп'ютер (Зелені) переміг!",
        "draw":             "Нічия!",
        "dlg_title":        "Гра закінчена",
        "dlg_question":     "Нова партія?"
    },
    "Ελληνικά": {
        "flag":             "🇬🇷",
        "title":            "4 στη Σειρά – Bitboard + PVS",
        "menu_mode":        "Λειτουργία",
        "menu_diff":        "Δυσκολία",
        "menu_lang":        "Γλώσσα",
        "menu_new":         "Νέο Παιχνίδι",
        "menu_undo":        "Αναίρεση (Ctrl+Z)",
        "mode_hvh":         "Παίκτης vs Παίκτης",
        "mode_hvc":         "Παίκτης vs Υπολογιστής",
        "diff_easy":        "Εύκολο",
        "diff_hard":        "Δύσκολο",
        "diff_exp":         "Έμπειρος",
        "status_your_turn": "Σειρά σου (Κόκκινο)",
        "status_p1":        "Σειρά του Παίκτη 1 (Κόκκινο)",
        "status_p2":        "Σειρά του Παίκτη 2 (Πράσινο)",
        "status_ai":        "Σειρά του Υπολογιστή (Πράσινο)",
        "win_p1":           "Ο Παίκτης 1 (Κόκκινο) κέρδισε!",
        "win_p2":           "Ο Παίκτης 2 (Πράσινο) κέρδισε!",
        "win_you":          "Κέρδισες (Κόκκινο)!",
        "win_ai":           "Ο Υπολογιστής (Πράσινο) κέρδισε!",
        "draw":             "Ισοπαλία!",
        "dlg_title":        "Τέλος Παιχνιδιού",
        "dlg_question":     "Νέος αγώνας;"
    },
    "Magyar": {
        "flag":             "🇭🇺",
        "title":            "4 egy Sorban – Bitboard + PVS",
        "menu_mode":        "Mód",
        "menu_diff":        "Nehézség",
        "menu_lang":        "Nyelv",
        "menu_new":         "Új Játék",
        "menu_undo":        "Visszavon (Ctrl+Z)",
        "mode_hvh":         "Ember vs. Ember",
        "mode_hvc":         "Ember vs. Gép",
        "diff_easy":        "Könnyű",
        "diff_hard":        "Nehéz",
        "diff_exp":         "Szakértő",
        "status_your_turn": "Te jössz (Piros)",
        "status_p1":        "1. Játékos (Piros) jön",
        "status_p2":        "2. Játékos (Zöld) jön",
        "status_ai":        "Számítógép (Zöld) jön",
        "win_p1":           "Az 1. Játékos (Piros) nyert!",
        "win_p2":           "A 2. Játékos (Zöld) nyert!",
        "win_you":          "Te nyertél (Piros)!",
        "win_ai":           "A Számítógép (Zöld) nyert!",
        "draw":             "Döntetlen!",
        "dlg_title":        "Játék Vége",
        "dlg_question":     "Új játék?"
    },
    "Türkçe": {
        "flag":             "🇹🇷",
        "title":            "Bir Sırada 4 – Bitboard + PVS",
        "menu_mode":        "Mod",
        "menu_diff":        "Zorluk",
        "menu_lang":        "Dil",
        "menu_new":         "Yeni Oyun",
        "menu_undo":        "Geri Al (Ctrl+Z)",
        "mode_hvh":         "Oyuncu vs. Oyuncu",
        "mode_hvc":         "Oyuncu vs. Bilgisayar",
        "diff_easy":        "Kolay",
        "diff_hard":        "Zor",
        "diff_exp":         "Uzman",
        "status_your_turn": "Senin sıran (Kırmızı)",
        "status_p1":        "Oyuncu 1 (Kırmızı) sırası",
        "status_p2":        "Oyuncu 2 (Yeşil) sırası",
        "status_ai":        "Bilgisayar (Yeşil) sırası",
        "win_p1":           "Oyuncu 1 (Kırmızı) kazandı!",
        "win_p2":           "Oyuncu 2 (Yeşil) kazandı!",
        "win_you":          "Sen kazandın (Kırmızı)!",
        "win_ai":           "Bilgisayar (Yeşil) kazandı!",
        "draw":             "Berabere!",
        "dlg_title":        "Oyun Bitti",
        "dlg_question":     "Yeni oyun?"
    },
    "Čeština": {
        "flag":             "🇨🇿",
        "title":            "4 v Řadě – Bitboard + PVS",
        "menu_mode":        "Režim",
        "menu_diff":        "Obtížnost",
        "menu_lang":        "Jazyk",
        "menu_new":         "Nová Hra",
        "menu_undo":        "Zpět (Ctrl+Z)",
        "mode_hvh":         "Hráč vs. Hráč",
        "mode_hvc":         "Hráč vs. Počítač",
        "diff_easy":        "Lehká",
        "diff_hard":        "Těžká",
        "diff_exp":         "Expert",
        "status_your_turn": "Tvůj tah (Červený)",
        "status_p1":        "Tah Hráče 1 (Červený)",
        "status_p2":        "Tah Hráče 2 (Zelený)",
        "status_ai":        "Tah Počítače (Zelený)",
        "win_p1":           "Hráč 1 (Červený) vyhrál!",
        "win_p2":           "Hráč 2 (Zelený) vyhrál!",
        "win_you":          "Vyhrál jsi (Červený)!",
        "win_ai":           "Počítač (Zelený) vyhrál!",
        "draw":             "Remíza!",
        "dlg_title":        "Konec hry",
        "dlg_question":     "Nová partie?"
    },

}

# — Einstellungen speichern/laden —
def _settings_path():
    """Gibt den plattformgerechten Pfad zur settings.json zurück."""
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        # Linux und alles andere: XDG_CONFIG_HOME oder ~/.config
        base = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config"))
    folder = os.path.join(base, "4inARow")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "settings.json")

def load_settings():
    """Lädt gespeicherte Einstellungen. Gibt Defaults zurück falls keine Datei vorhanden."""
    defaults = {"lang": "Deutsch", "difficulty": "Einfach", "mode": "Mensch vs. Computer"}
    try:
        path = _settings_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Nur bekannte Werte übernehmen
            if data.get("lang") in LANG:
                defaults["lang"] = data["lang"]
            if data.get("difficulty") in DIFFICULTIES:
                defaults["difficulty"] = data["difficulty"]
            if data.get("mode") in ("Mensch vs. Computer", "Mensch vs. Mensch"):
                defaults["mode"] = data["mode"]
    except Exception:
        pass
    return defaults

def save_settings(lang, difficulty, mode):
    """Speichert aktuelle Einstellungen auf die Festplatte."""
    try:
        path = _settings_path()
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"lang": lang, "difficulty": difficulty, "mode": mode}, f, indent=2)
    except Exception:
        pass

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4 in a Row – Bitboard + PVS")

        # Spielzustand
        self.human_board    = 0
        self.ai_board       = 0
        self.board_grid     = [[0] * COLS for _ in range(ROWS)]
        self.heights        = [0] * COLS
        self.transpo        = {}
        self.killer_moves   = [[None, None] for _ in range(20)]  # Killer-Heuristik
        self.move_history   = []   # Zughistorie für Rückgängig
        self.win_cells      = []   # Gewinnzellen für Markierung
        self.current_player = HUMAN  # 1 = Rot, 2 = Grün

        # Startmodus — aus gespeicherten Einstellungen laden
        _s               = load_settings()
        self.lang        = _s["lang"]
        self.mode        = _s["mode"]
        self.difficulty  = _s["difficulty"]
        cfg             = DIFFICULTIES[self.difficulty]
        self.max_depth   = cfg["max_depth"]
        self.time_budget = cfg["time_budget"]

        # UI-Elemente
        self.drop_buttons = []
        self.cell_labels  = []
        self._anims       = []   # hält laufende Animationen am Leben
        self._build_ui()
        self._create_menu()
        self.start_new_game()

    def _build_ui(self):
        central = QWidget()
        central.setStyleSheet(
            "QWidget { background: qlineargradient("
            "x1:0, y1:0, x2:0, y2:1, "
            "stop:0 #ffffff, stop:1 #f2f5f8); }"
        )
        vlay = QVBoxLayout(central)
        vlay.setContentsMargins(16, 16, 16, 16)
        vlay.setSpacing(12)
        self.setCentralWidget(central)

        self.lbl_status = QLabel("", self)
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setFont(QFont("Arial", 17, QFont.Bold))
        self.lbl_status.setStyleSheet(
            "QLabel {"
            "  color: #1a2733;"
            "  background-color: #ffffff;"
            "  border: 2px solid #b7c3d0;"
            "  border-radius: 10px;"
            "  padding: 8px;"
            "}"
        )
        vlay.addWidget(self.lbl_status)

        board = QWidget()
        board.setStyleSheet(
            "QWidget {"
            "  background: qlineargradient(x1:0, y1:0, x2:1, y2:1,"
            "              stop:0 #9ccbec, stop:1 #7aafda);"
            "  border-radius: 14px;"
            "}"
        )
        self.board = board
        gl = QGridLayout(board)
        gl.setSpacing(6)
        gl.setContentsMargins(14, 14, 14, 14)

        # Drop-Buttons
        for c in range(COLS):
            btn = QPushButton("↓")
            btn.setFont(QFont("Arial", 18, QFont.Bold))
            btn.setFixedSize(50, 36)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(
                "QPushButton {"
                "  color: white;"
                "  background-color: #4d84b8;"
                "  border: none;"
                "  border-radius: 8px;"
                "}"
                "QPushButton:hover {"
                "  background-color: #f4b400;"
                "  color: #123a6b;"
                "}"
                "QPushButton:pressed {"
                "  background-color: #d99e00;"
                "}"
                "QPushButton:disabled {"
                "  background-color: #8fb2d4;"
                "  color: #eef2f7;"
                "}"
            )
            btn.clicked.connect(lambda _, col=c: self._player_move(col))
            gl.addWidget(btn, 0, c)
            self.drop_buttons.append(btn)

        # Spielbrett — runde "Löcher"
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                lbl = QLabel(" ")
                lbl.setFixedSize(50, 50)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFont(QFont("Arial", 30, QFont.Bold))
                lbl.setStyleSheet(self._empty_cell_style())
                gl.addWidget(lbl, r+1, c)
                row.append(lbl)
            self.cell_labels.append(row)

        vlay.addWidget(board)

    @staticmethod
    def _empty_cell_style():
        return (
            "QLabel {"
            "  background-color: #eef2f7;"
            "  border: 2px solid #0d2a4d;"
            "  border-radius: 25px;"
            "}"
        )

    @staticmethod
    def _piece_cell_style(color):
        if color == "red":
            grad = "stop:0 #ff8a7a, stop:0.5 #e6342b, stop:1 #a30f08"
        else:
            grad = "stop:0 #9ce89a, stop:0.5 #2fae3f, stop:1 #146c1f"
        return (
            "QLabel {"
            f"  background: qradialgradient(cx:0.35, cy:0.3, radius:0.9,"
            f"              fx:0.35, fy:0.3, {grad});"
            "  border: 2px solid #0d2a4d;"
            "  border-radius: 25px;"
            "}"
        )

    @staticmethod
    def _highlight_cell_style():
        return (
            "QLabel {"
            "  background: qradialgradient(cx:0.35, cy:0.3, radius:0.9,"
            "              fx:0.35, fy:0.3, stop:0 #fff3b0, stop:0.5 #ffd700, stop:1 #b8860b);"
            "  border: 3px solid #7a5c00;"
            "  border-radius: 25px;"
            "}"
        )

    def _animate_drop(self, scr_r, col, color, on_finished=None):
        """Lässt einen Stein sichtbar von oben in die Spalte fallen."""
        target_lbl = self.cell_labels[scr_r][col]
        target_pos = target_lbl.pos()

        top_lbl   = self.cell_labels[0][col]
        start_pos = top_lbl.pos()
        start_pos = QPoint(start_pos.x(), start_pos.y() - top_lbl.height() - 10)

        falling = QLabel(self.board)
        falling.setFixedSize(target_lbl.width(), target_lbl.height())
        falling.setStyleSheet(self._piece_cell_style(color))
        falling.move(start_pos)
        falling.show()
        falling.raise_()

        distance = max(1, target_pos.y() - start_pos.y())
        duration = max(220, min(650, int(distance * 1.4)))

        anim = QPropertyAnimation(falling, b"pos", self)
        anim.setDuration(duration)
        anim.setStartValue(start_pos)
        anim.setEndValue(target_pos)
        anim.setEasingCurve(QEasingCurve.InQuad)

        def _finish():
            target_lbl.setStyleSheet(self._piece_cell_style(color))
            falling.deleteLater()
            if anim in self._anims:
                self._anims.remove(anim)
            if on_finished:
                on_finished()

        anim.finished.connect(_finish)
        self._anims.append(anim)
        anim.start()

    def _t(self, key):
        """Übersetzungshelfer – gibt den Text in der aktuellen Sprache zurück."""
        return LANG[self.lang][key]

    def _create_menu(self):
        mb = self.menuBar()
        mb.setNativeMenuBar(False)
        mb.clear()

        L = LANG[self.lang]

        # --- Modus ---
        modus       = mb.addMenu(L["menu_mode"])
        self._act_hvh = QAction(L["mode_hvh"], self)
        self._act_hvh.setCheckable(True)
        self._act_hvc = QAction(L["mode_hvc"], self)
        self._act_hvc.setCheckable(True)
        self._act_hvc.setChecked(self.mode in ("Mensch vs. Computer", "Human vs. Computer"))
        self._act_hvh.setChecked(self.mode in ("Mensch vs. Mensch", "Human vs. Human"))
        for act in (self._act_hvh, self._act_hvc):
            act.triggered.connect(
                lambda _, a=act: self._switch_mode_by_label(a.text())
            )
        modus.addAction(self._act_hvh)
        modus.addAction(self._act_hvc)

        # --- Schwierigkeit ---
        diff           = mb.addMenu(L["menu_diff"])
        self._act_easy = QAction(L["diff_easy"], self)
        self._act_easy.setCheckable(True)
        self._act_hard = QAction(L["diff_hard"], self)
        self._act_hard.setCheckable(True)
        self._act_exp  = QAction(L["diff_exp"],  self)
        self._act_exp.setCheckable(True)
        checked_map    = {"Einfach": self._act_easy, "Schwer": self._act_hard, "Experte": self._act_exp}
        checked_map[self.difficulty].setChecked(True)
        for act, key in zip((self._act_easy, self._act_hard, self._act_exp),
                            ("Einfach", "Schwer", "Experte")):
            act.triggered.connect(
                lambda _, k=key, grp=[self._act_easy, self._act_hard, self._act_exp]:
                    self._switch_difficulty(k, grp)
            )
        diff.addAction(self._act_easy)
        diff.addAction(self._act_hard)
        diff.addAction(self._act_exp)

        # --- Sprache / Language --- (automatisch aus LANG-Dictionary) ---
        lang_menu = mb.addMenu(L["menu_lang"])
        for lang_key, lang_data in LANG.items():
            flag  = lang_data.get("flag", "")
            label = f"{flag}  {lang_key}" if flag else lang_key
            act   = QAction(label, self)
            act.setCheckable(True)
            act.setChecked(lang_key == self.lang)
            act.triggered.connect(lambda _, k=lang_key: self._switch_language(k))
            lang_menu.addAction(act)

        # --- Neues Spiel ---
        act_new = QAction(L["menu_new"], self)
        act_new.triggered.connect(self.start_new_game)
        mb.addAction(act_new)

        # --- Rückgängig ---
        act_undo = QAction(L["menu_undo"], self)
        act_undo.setShortcut("Ctrl+Z")
        act_undo.triggered.connect(self._undo)
        mb.addAction(act_undo)

    def _switch_language(self, lang):
        self.lang = lang
        save_settings(self.lang, self.difficulty, self.mode)
        self._create_menu()
        self._refresh_status()
        self.setWindowTitle(self._t("title"))

    def _switch_mode_by_label(self, label):
        """Setzt den internen Modus anhand des (übersetzten) Labels."""
        L = LANG[self.lang]
        if label == L["mode_hvh"]:
            self.mode = "Mensch vs. Mensch"
        else:
            self.mode = "Mensch vs. Computer"
        self._act_hvh.setChecked(self.mode == "Mensch vs. Mensch")
        self._act_hvc.setChecked(self.mode == "Mensch vs. Computer")
        save_settings(self.lang, self.difficulty, self.mode)
        self.start_new_game()

    def _refresh_status(self):
        """Statustext neu setzen ohne Spielreset."""
        L = LANG[self.lang]
        if self.mode == "Mensch vs. Computer":
            if self.current_player == HUMAN:
                self.lbl_status.setText(L["status_your_turn"])
            else:
                self.lbl_status.setText(L["status_ai"])
        else:
            if self.current_player == HUMAN:
                self.lbl_status.setText(L["status_p1"])
            else:
                self.lbl_status.setText(L["status_p2"])

    def _switch_difficulty(self, diff_key, group):
        self.difficulty  = diff_key
        for act in group:
            act.setChecked(False)
        checked_map = {"Einfach": self._act_easy, "Schwer": self._act_hard, "Experte": self._act_exp}
        checked_map[diff_key].setChecked(True)
        cfg = DIFFICULTIES[diff_key]
        self.max_depth   = cfg["max_depth"]
        self.time_budget = cfg["time_budget"]
        save_settings(self.lang, self.difficulty, self.mode)

    def start_new_game(self):
        # Reset Spielzustand
        self.human_board    = 0
        self.ai_board       = 0
        self.board_grid     = [[0]*COLS for _ in range(ROWS)]
        self.heights        = [0]*COLS
        self.transpo.clear()
        self.killer_moves   = [[None, None] for _ in range(20)]
        self.move_history   = []
        self.win_cells      = []
        self.current_player = HUMAN

        # UI
        self._update_ui()
        if self.mode == "Mensch vs. Computer":
            self.lbl_status.setText(self._t("status_your_turn"))
        else:
            self.lbl_status.setText(self._t("status_p1"))
        for b in self.drop_buttons:
            b.setEnabled(True)

    def _player_move(self, col):
        if self.heights[col] >= ROWS:
            return
        row = self.heights[col]
        mover = self.current_player

        # Zustand vor dem Zug speichern
        self.move_history.append({
            "board_grid":   [r[:] for r in self.board_grid],
            "human_board":  self.human_board,
            "ai_board":     self.ai_board,
            "heights":      self.heights[:],
            "player":       self.current_player,
        })

        self.board_grid[row][col] = mover

        # Bitboards updaten
        bit = 1 << (row*COLS + col)
        if mover == HUMAN:
            self.human_board |= bit
        else:
            self.ai_board |= bit

        self.heights[col] += 1

        scr_r = ROWS - 1 - row
        color = "red" if mover == HUMAN else "green"
        self._update_ui(skip_cell=(scr_r, col))

        # Während der Fallanimation keine weiteren Klicks zulassen
        for b in self.drop_buttons:
            b.setEnabled(False)

        self._animate_drop(scr_r, col, color, lambda: self._after_player_drop(mover))

    def _after_player_drop(self, mover):
        """Wird aufgerufen, sobald der Stein sichtbar gelandet ist."""
        # Sieg- oder Unentschieden-Prüfung
        board_bb = self.human_board if mover == HUMAN else self.ai_board
        won, cells = self._win_matrix(mover)
        if won or self._check_win_bitboard(board_bb):
            self._update_ui(highlight=cells)
            if self.mode == "Mensch vs. Computer":
                msg = self._t("win_you") if mover == HUMAN else self._t("win_ai")
            else:
                msg = self._t("win_p1") if mover == HUMAN else self._t("win_p2")
            self._end(msg)
            return
        if all(h == ROWS for h in self.heights):
            self._end(self._t("draw"))
            return

        # Spielmodus-Logik
        if self.mode == "Mensch vs. Computer" and mover == HUMAN:
            self.lbl_status.setText(self._t("status_ai"))
            # Buttons bleiben gesperrt, bis der Computer gezogen hat
            QTimer.singleShot(150, self._computer_move)
        else:
            self.current_player = AI_PLAYER if mover == HUMAN else HUMAN
            if self.mode == "Mensch vs. Mensch":
                text = self._t("status_p1") if self.current_player == HUMAN else self._t("status_p2")
                self.lbl_status.setText(text)
            else:
                self.lbl_status.setText(self._t("status_your_turn"))
            for b in self.drop_buttons:
                b.setEnabled(True)

    def _computer_move(self):
        start     = time.time()
        best_move = None

        # Iterative Deepening PVS
        for depth in range(2, self.max_depth+1, 2):
            alpha, beta = -INF, INF
            score, move = self._negamax_pvs(
                self.ai_board, self.human_board,
                copy.copy(self.heights),
                depth, alpha, beta, True, start, 0
            )
            if time.time() - start > self.time_budget:
                break
            if move is not None:
                best_move = move
            if score >= WIN_SCORE:
                break

        valid = [c for c in range(COLS) if self.heights[c] < ROWS]
        if best_move is None:
            best_move = random.choice(valid) if valid else 0

        # KI-Zug im Board vermerken
        row = self.heights[best_move]
        # Zustand vor KI-Zug speichern
        self.move_history.append({
            "board_grid":   [r[:] for r in self.board_grid],
            "human_board":  self.human_board,
            "ai_board":     self.ai_board,
            "heights":      self.heights[:],
            "player":       AI_PLAYER,
        })
        self.board_grid[row][best_move] = AI_PLAYER
        self.ai_board |= 1 << (row*COLS + best_move)
        self.heights[best_move] += 1

        scr_r = ROWS - 1 - row
        self._update_ui(skip_cell=(scr_r, best_move))
        self._animate_drop(scr_r, best_move, "green", self._after_computer_drop)

    def _after_computer_drop(self):
        """Wird aufgerufen, sobald der KI-Stein sichtbar gelandet ist."""
        won, cells = self._win_matrix(AI_PLAYER)
        if won or self._check_win_bitboard(self.ai_board):
            self._update_ui(highlight=cells)
            self._end(self._t("win_ai"))
            return
        if all(h == ROWS for h in self.heights):
            self._end(self._t("draw"))
            return

        # Nach KI-Zug wieder Mensch — Buttons freigeben
        self.current_player = HUMAN
        self.lbl_status.setText(self._t("status_your_turn"))
        for b in self.drop_buttons:
            b.setEnabled(True)

    def _undo(self):
        """Rückgängig: Im HvC-Modus werden Mensch+KI-Zug zusammen zurückgenommen."""
        if not self.move_history:
            return
        # Im Mensch-vs-Computer Modus: zwei Züge zurück (KI + Mensch)
        steps = 2 if self.mode == "Mensch vs. Computer" and len(self.move_history) >= 2 else 1
        for _ in range(steps):
            if self.move_history:
                state = self.move_history.pop()
        # Zustand wiederherstellen
        self.board_grid   = [r[:] for r in state["board_grid"]]
        self.human_board  = state["human_board"]
        self.ai_board     = state["ai_board"]
        self.heights      = state["heights"][:]
        self.current_player = HUMAN
        self.win_cells    = []
        self.transpo.clear()
        self._update_ui()
        self.lbl_status.setText(self._t("status_your_turn")
                                if self.mode == "Mensch vs. Computer"
                                else self._t("status_p1"))
        for b in self.drop_buttons:
            b.setEnabled(True)

    def _update_ui(self, highlight=None, skip_cell=None):
        """highlight: Liste von (screen_r, c) Tupeln die golden markiert werden.
        skip_cell: (screen_r, c) wird als leer belassen, weil die Fallanimation
        diesen Platz gerade selbst einfärbt, sobald der Stein ankommt."""
        for r in range(ROWS):
            for c in range(COLS):
                lbl = self.cell_labels[r][c]
                lbl.setStyleSheet(self._empty_cell_style())

        for r in range(ROWS):
            for c in range(COLS):
                val = self.board_grid[r][c]
                if val in (HUMAN, AI_PLAYER):
                    scr_r = ROWS - 1 - r
                    if skip_cell == (scr_r, c):
                        continue
                    lbl   = self.cell_labels[scr_r][c]
                    color = "red" if val == HUMAN else "green"
                    lbl.setStyleSheet(self._piece_cell_style(color))

        # Gewinnzellen golden hinterlegen
        if highlight:
            for (scr_r, c) in highlight:
                lbl = self.cell_labels[scr_r][c]
                lbl.setStyleSheet(self._highlight_cell_style())

    def _win_matrix(self, player):
        """Gibt (True, [(scr_r,c),...]) zurück wenn Spieler gewonnen hat, sonst (False, [])."""
        g = self.board_grid
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - WIN_COUNT + 1):
                if all(g[r][c+i] == player for i in range(WIN_COUNT)):
                    return True, [(ROWS-1-r, c+i) for i in range(WIN_COUNT)]
        # Vertikal
        for c in range(COLS):
            for r in range(ROWS - WIN_COUNT + 1):
                if all(g[r+i][c] == player for i in range(WIN_COUNT)):
                    return True, [(ROWS-1-(r+i), c) for i in range(WIN_COUNT)]
        # Diagonal ↗
        for r in range(ROWS - WIN_COUNT + 1):
            for c in range(COLS - WIN_COUNT + 1):
                if all(g[r+i][c+i] == player for i in range(WIN_COUNT)):
                    return True, [(ROWS-1-(r+i), c+i) for i in range(WIN_COUNT)]
        # Diagonal ↘
        for r in range(WIN_COUNT - 1, ROWS):
            for c in range(COLS - WIN_COUNT + 1):
                if all(g[r-i][c+i] == player for i in range(WIN_COUNT)):
                    return True, [(ROWS-1-(r-i), c+i) for i in range(WIN_COUNT)]
        return False, []

    def _negamax_pvs(self, pos, opp, heights, depth, alpha, beta, is_pv, start, ply=0):
        if time.time() - start > self.time_budget:
            return 0, None
        key = (pos, opp, tuple(heights), depth)
        if key in self.transpo:
            cached_score, cached_move, cached_flag, cached_alpha, cached_beta = self.transpo[key]
            if cached_flag == 'exact':
                return cached_score, cached_move
            elif cached_flag == 'lower' and cached_score >= beta:
                return cached_score, cached_move
            elif cached_flag == 'upper' and cached_score <= alpha:
                return cached_score, cached_move

        if depth == 0 or self._check_win_bitboard(pos) or self._check_win_bitboard(opp):
            return self._evaluate(pos, opp), None

        orig_alpha = alpha
        best_move  = None
        valid_cols = [c for c in range(COLS) if heights[c] < ROWS]

        # Sofortiger Gewinnzug der KI
        for col in valid_cols:
            row = heights[col]
            bit = 1 << (row * COLS + col)
            if self._check_win_bitboard(pos | bit):
                return WIN_SCORE - (self.max_depth - depth), col

        # Sofortige Blockierung eines gegnerischen Gewinns
        threat_block = None
        for col in valid_cols:
            row = heights[col]
            bit = 1 << (row * COLS + col)
            if self._check_win_bitboard(opp | bit):
                threat_block = col
                break
        if threat_block is not None:
            valid_cols = [threat_block]

        # Zugordnung: Killer → Zentrum → Rest
        killers = self.killer_moves[ply] if ply < len(self.killer_moves) else []
        def move_order(c):
            if c in killers:
                return 0
            return abs(c - COLS // 2) + 1
        moves = sorted(valid_cols, key=move_order)

        first = True
        for col in moves:
            row = heights[col]
            heights[col] += 1
            bit     = 1 << (row * COLS + col)
            new_pos = pos | bit

            if first or is_pv:
                sc, _ = self._negamax_pvs(opp, new_pos, heights, depth-1, -beta, -alpha, True,  start, ply+1)
                sc = -sc
            else:
                sc, _ = self._negamax_pvs(opp, new_pos, heights, depth-1, -alpha-1, -alpha, False, start, ply+1)
                sc = -sc
                if alpha < sc < beta:
                    sc, _ = self._negamax_pvs(opp, new_pos, heights, depth-1, -beta, -sc, True, start, ply+1)
                    sc = -sc

            heights[col] -= 1

            if sc > alpha:
                alpha     = sc
                best_move = col
            if alpha >= beta:
                # Killer-Move speichern
                if ply < len(self.killer_moves) and col not in self.killer_moves[ply]:
                    self.killer_moves[ply][1] = self.killer_moves[ply][0]
                    self.killer_moves[ply][0] = col
                break
            first = False

        # Transpositionstabelle mit Flag
        if alpha <= orig_alpha:
            flag = 'upper'
        elif alpha >= beta:
            flag = 'lower'
        else:
            flag = 'exact'
        self.transpo[key] = (alpha, best_move, flag, orig_alpha, beta)
        return alpha, best_move

    def _check_win_bitboard(self, bb):
        # Horizontale Maske: verhindert dass Spalte 9→Spalte 0 als benachbart gilt
        # Jede Spalte c bekommt eine Maske mit allen Bits in dieser Spalte
        h_mask = 0
        for r in range(ROWS):
            for c in range(COLS - WIN_COUNT + 1):   # nur Spalten die einen 4er-Start erlauben
                h_mask |= 1 << (r * COLS + c)

        # Horizontal (Richtung 1) — nur mit Maske
        m = (bb & h_mask) & ((bb & h_mask) >> 1)
        if m & (m >> 2):
            return True

        # Vertikal (Richtung COLS) — keine Zeilengrenze möglich
        m = bb & (bb >> COLS)
        if m & (m >> (2 * COLS)):
            return True

        # Diagonale ↘ (Richtung COLS+1) — Zeilengrenze absichern
        m = (bb & h_mask) & ((bb & h_mask) >> (COLS + 1))
        if m & (m >> (2 * (COLS + 1))):
            return True

        # Diagonale ↙ (Richtung COLS-1) — Zeilengrenze absichern
        # Startpunkte müssen in Spalte WIN_COUNT-1 bis COLS-1 liegen
        h_mask2 = 0
        for r in range(ROWS):
            for c in range(WIN_COUNT - 1, COLS):    # Spalten WIN_COUNT-1 bis COLS-1
                h_mask2 |= 1 << (r * COLS + c)
        m = (bb & h_mask2) & ((bb & h_mask2) >> (COLS - 1))
        if m & (m >> (2 * (COLS - 1))):
            return True

        return False

    def _evaluate(self, pos, opp):
        if self._check_win_bitboard(pos): return  WIN_SCORE
        if self._check_win_bitboard(opp): return -WIN_SCORE
        return self._score_position(pos, opp) - self._score_position(opp, pos)

    # Masken als Klassenvariablen (einmal berechnet)
    _BOARD_MASK = (1 << (ROWS * COLS)) - 1
    _H_MASK  = sum(1 << (r*COLS+c) for r in range(ROWS) for c in range(COLS-WIN_COUNT+1))
    _H_MASK2 = sum(1 << (r*COLS+c) for r in range(ROWS) for c in range(WIN_COUNT-1, COLS))

    def _score_position(self, pos, opp):
        """
        Prüft jedes mögliche WIN_COUNT-Fenster auf dem Board.
        Erkennt ALLE Bedrohungen — auch Lücken wie x_xx oder xx_x.
        """
        score = 0
        directions = [
            (1,        self._H_MASK),
            (COLS,     self._BOARD_MASK),
            (COLS + 1, self._H_MASK),
            (COLS - 1, self._H_MASK2),
        ]

        for d, start_mask in directions:
            s = start_mask
            while s:
                lsb = s & (-s)
                s  &= s - 1
                # 4 Positionen des Fensters
                window = lsb | (lsb << d) | (lsb << (2*d)) | (lsb << (3*d))
                if (window & self._BOARD_MASK) != window:
                    continue

                pos_in = bin(pos & window).count("1")
                opp_in = bin(opp & window).count("1")

                # Fenster ohne Gegner → Chance für pos
                if opp_in == 0:
                    if   pos_in == 3: score += 2000
                    elif pos_in == 2: score += 50
                    elif pos_in == 1: score += 5

                # Fenster ohne eigene Steine → Bedrohung durch opp
                if pos_in == 0:
                    if   opp_in == 3: score -= 5000   # Lücken-3er wird erkannt!
                    elif opp_in == 2: score -= 150
                    elif opp_in == 1: score -= 10

        # Zentrumsgewichtung
        center = COLS // 2
        for c in range(COLS):
            w = (COLS // 2) - abs(c - center) + 1
            col_bits = sum(1 << (r*COLS+c) for r in range(ROWS))
            score += bin(pos & col_bits).count("1") * w * 3
            score -= bin(opp & col_bits).count("1") * w * 3

        return score

    def _score_bitboard(self, bb, is_experte=False):
        # Nur noch als Fallback — Hauptlogik in _score_position
        score = 0
        dirs = [(1, self._H_MASK), (COLS, self._BOARD_MASK),
                (COLS+1, self._H_MASK), (COLS-1, self._H_MASK2)]
        for d, mask in dirs:
            m = (bb & mask) & ((bb & mask) >> d)
            score += bin(m & (m >> d) & mask).count("1") * 1000
        return score

    def _end(self, msg):
        for b in self.drop_buttons:
            b.setEnabled(False)
        dlg = QMessageBox(self)
        dlg.setWindowTitle(self._t("dlg_title"))
        dlg.setText(f"{msg}\n\n{self._t('dlg_question')}")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setDefaultButton(QMessageBox.Yes)
        if dlg.exec() == QMessageBox.Yes:
            self.start_new_game()
        else:
            self.close()

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w   = GameWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()