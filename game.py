"""
word_puzzle_final.py
Final Word Puzzle (windowed 1280x720) — side menu + right-side hint panel
Only Ctrl+H / Ctrl+S / Ctrl+R are shortcuts. ESC = menu. No sounds.
"""

import pygame
import random
import json
import os
import sys
from datetime import datetime

# -------- CONFIG --------
WINDOW_W, WINDOW_H = 1280, 720
FPS = 60
HIGHSCORE_FILE = "highscores.json"
MAX_HIGHS = 12
CTRL_MASK = pygame.KMOD_CTRL

# -------- INIT PYGAME --------
pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Word Puzzle Pro — Final")
clock = pygame.time.Clock()
pygame.key.set_repeat(0, 0)  # normal typing

# -------- FONTS & COLORS --------
FONT_BIG = pygame.font.SysFont("arial", 64)
FONT_MED = pygame.font.SysFont("arial", 36)
FONT_SM = pygame.font.SysFont("arial", 24)
FONT_XS = pygame.font.SysFont("arial", 18)

COLOR_BG = (28, 30, 38)
COLOR_PANEL = (36, 40, 50)
COLOR_LEFT_PANEL = (32, 36, 46)
COLOR_TEXT = (235, 240, 250)
COLOR_ACCENT = (60, 160, 240)
COLOR_HINT_BOX = (42, 46, 56)
COLOR_YELLOW = (255, 210, 60)
COLOR_GRAY = (160, 165, 175)
COLOR_RED = (220, 70, 70)
COLOR_GREEN = (80, 200, 120)

# -------- WORD LIST (word, hint) --------
WORDS = [
    ("planet", "A large celestial body that orbits a star."),
    ("forest", "A large area covered chiefly with trees and undergrowth."),
    ("camera", "A device for taking photographs or recording video."),
    ("school", "A place where people go to learn."),
    ("python", "A widely used high-level programming language."),
    ("battery", "Stores electrical energy for portable devices."),
    ("dolphin", "A highly intelligent marine mammal."),
    ("stadium", "A large venue where sports events are held."),
    ("project", "A planned set of tasks to achieve an objective."),
    ("network", "A group of interconnected computers or systems."),
    ("cricket", "A bat-and-ball sport popular in many countries."),
    ("captain", "The leader of a team on the field."),
    ("developer", "A person who writes and maintains software."),
    ("keyboard", "An input device used to type characters."),
    ("monitor", "A display screen for a computer."),
    ("storage", "Where data is kept for later access."),
    ("algorithm", "An ordered set of steps for solving a problem."),
    ("compiler", "A tool that translates source code to machine code."),
    ("debugger", "Software used to locate and fix errors."),
    ("framework", "A reusable set of libraries that provides structure."),
    ("latency", "Delay between an action and its response."),
    ("protocol", "Rules governing data exchange between systems."),
    ("database", "Organized collection of structured information."),
    ("encryption", "Encoding data to protect it from unauthorized access."),
    ("variable", "A named storage location in programming."),
    ("function", "A named block of code that performs a task."),
    ("package", "A bundle of code modules distributed together."),
    ("library", "Reusable code that helps solve common problems."),
    ("virtual", "Existing in digital form rather than physical."),
    ("container", "A lightweight, portable runtime environment."),
    ("deployment", "Releasing software to run in production."),
    ("optimization", "Improving efficiency or performance."),
    ("cruise", "A voyage on a ship for pleasure."),
    ("festival", "A public celebration with music and culture."),
    ("history", "The study of past events and people."),
    ("language", "A system of communication used by a community."),
    ("computer", "An electronic device for processing information."),
    ("monitoring", "Keeping track of system or application behavior."),
    ("antenna", "A structure for transmitting or receiving radio waves."),
    ("battery", "A device that provides electrical energy (duplicate allowed)."),
    ("bridge", "A structure spanning a physical obstacle."),
    ("camera", "Device that records images (duplicate allowed)."),
    ("pencil", "A writing instrument made of graphite."),
    ("notebook", "A book for writing notes and thoughts."),
    ("library", "A collection of books; also a code term."),
    ("athlete", "A person trained in physical sports."),
    ("stadium", "A venue for large sporting events (duplicate allowed)."),
    ("goalkeeper", "The player who protects the goal in football."),
    ("tournament", "A competition involving multiple competitors."),
    ("umpire", "The official who makes decisions in cricket."),
    ("hockey", "A team sport played on ice with sticks."),
    ("elephant", "The largest land mammal, with a trunk."),
    ("tiger", "A large wild cat with distinctive stripes."),
    ("giraffe", "A tall African mammal with a long neck."),
    ("kangaroo", "A hopping marsupial native to Australia."),
    ("penguin", "A flightless seabird adapted to cold climates."),
    ("leopard", "A big cat known for spotted fur."),
    ("octopus", "An intelligent sea creature with eight arms."),
    ("shark", "A powerful predatory fish of the oceans."),
    ("volcano", "An opening in the Earth's crust that can erupt lava."),
    ("mountain", "A very tall natural elevation of the earth's surface."),
    ("river", "A natural stream of water flowing to a larger body."),
    ("island", "A land area surrounded by water."),
    ("desert", "A dry region with little precipitation."),
    ("sunlight", "Light which comes from the sun."),
    ("rainbow", "A multicolored arc formed by light and water droplets."),
    ("history", "The study or record of past events (duplicate allowed)."),
    ("economy", "System of production, distribution, and consumption."),
    ("justice", "Fair and impartial treatment under the law."),
    ("science", "Systematic study of the physical and natural world."),
    ("biology", "The study of living organisms."),
    ("chemistry", "The study of substances and their reactions."),
    ("physics", "The study of matter and energy."),
    ("geometry", "Branch of mathematics concerning shapes and space."),
    ("triangle", "A three-sided polygon."),
    ("square", "A four-sided polygon with equal sides."),
    ("circle", "A round shape with all points equidistant from center."),
    ("notebook", "A book for recording notes (duplicate allowed)."),
    ("document", "A written or printed record providing information."),
    ("message", "A piece of information sent from one person to another."),
    ("browser", "An app used to view websites."),
    ("server", "A machine that provides resources to clients."),
    ("client", "A program or machine requesting services."),
    ("router", "A device that forwards data packets between networks."),
    ("switch", "A device that connects devices within a network."),
    ("protocol", "A rule set for data exchange (duplicate allowed)."),
    ("signal", "An electrical or radio wave carrying information."),
    ("volume", "Amount of space or loudness level."),
    ("texture", "The feel or appearance of a surface."),
    ("pattern", "A repeated decorative design or sequence."),
    ("gallery", "A place where artworks are displayed."),
    ("portrait", "A painting or photograph of a person."),
    ("novel", "A long fictional prose narrative."),
    ("poetry", "Literary work expressing ideas with style and rhythm."),
    ("concert", "A performance of music before an audience."),
    ("orchestra", "A large ensemble of musical instruments."),
    ("studio", "A room where creative work is made."),
    ("design", "The art of planning and creating."),
    ("engineer", "A person who designs, builds and maintains systems."),
    ("architect", "A designer of buildings and structures."),
    ("chef", "A professional cook."),
    ("recipe", "Instructions for preparing a dish."),
    ("kitchen", "The room where food is prepared (duplicate allowed)."),
]

# -------- HELPERS: scramble, highscores --------
def scramble_word(word):
    if len(word) <= 1:
        return word
    letters = list(word)
    for _ in range(10):
        random.shuffle(letters)
        if "".join(letters) != word:
            return "".join(letters)
    return "".join(letters)

def load_highscores():
    if not os.path.isfile(HIGHSCORE_FILE):
        return []
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_highscores(hs):
    try:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(hs, f, indent=2)
    except:
        pass

def add_highscore(name, score):
    hs = load_highscores()
    hs.append({"name": name, "score": score, "date": datetime.now().isoformat()})
    hs = sorted(hs, key=lambda x: x["score"], reverse=True)[:MAX_HIGHS]
    save_highscores(hs)

# -------- GAME CLASS --------
class Game:
    def __init__(self):
        self.state = "menu"   # menu, play, settings, scores, gameover, entername
        self.menu_index = 0
        self.left_items = ["Play", "Settings", "High Scores", "Quit"]

        # Gameplay settings
        self.category = "General"
        self.difficulty = "Medium"
        self.time_limit = 20
        self.points = 10

        self.score = 0
        self.player_input = ""
        self.revealed = 0  # number of letters revealed by Ctrl+H
        self.current = None
        self.hint = ""
        self.scrambled = ""
        self.start_tick = pygame.time.get_ticks()
        self.gameover_reason = ""
        self.name_entry = ""

        self.pick_new_word()

    def pick_new_word(self):
        self.revealed = 0
        self.player_input = ""
        # pick random word from large WORDS list
        self.current, self.hint = random.choice(WORDS)
        self.scrambled = scramble_word(self.current)
        self.start_tick = pygame.time.get_ticks()
        # set time_limit & points from difficulty
        if self.difficulty == "Easy":
            self.time_limit = 25; self.points = 10
        elif self.difficulty == "Medium":
            self.time_limit = 18; self.points = 20
        else:
            self.time_limit = 12; self.points = 30

    def restart_game(self):
        self.score = 0
        self.pick_new_word()
        self.state = "play"

    def update_timer(self):
        elapsed = (pygame.time.get_ticks() - self.start_tick) // 1000
        left = max(0, self.time_limit - elapsed)
        if left <= 0:
            self.gameover_reason = f"Time's up! Correct: {self.current.upper()}"
            self.state = "gameover"
        return left

    def reveal_letter(self):
        if self.revealed < len(self.current):
            self.revealed += 1

    def skip_word(self):
        self.score = max(0, self.score - max(1, self.points // 4))
        self.pick_new_word()

    def submit_answer(self):
        if self.player_input.strip().lower() == self.current.lower():
            self.score += self.points
            self.pick_new_word()
        else:
            self.gameover_reason = f"Wrong! Correct: {self.current.upper()}"
            self.state = "gameover"

# -------- DRAW HELPERS --------
def draw_text(surf, text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surf.blit(img, rect)



# Right-side hint panel
def draw_right_hint_panel(surf, game):
    panel_x = WINDOW_W - 340
    pygame.draw.rect(surf, COLOR_HINT_BOX, (panel_x, 0, 340, WINDOW_H))
    pygame.draw.rect(surf, COLOR_PANEL, (panel_x, 0, 340, WINDOW_H), 2)
    draw_text(surf, "HINT", FONT_MED, COLOR_YELLOW, panel_x + 170, 40)
    # hint wrapped
    words = game.hint.split()
    lines = []
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if FONT_SM.size(test)[0] <= 300:
            line = test
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    y = 90
    for ln in lines:
        draw_text(surf, ln, FONT_SM, COLOR_TEXT, panel_x + 20, y, center=False)
        y += 28
    # revealed letters
    revealed = game.current[:game.revealed]
    draw_text(surf, f"Revealed: {revealed}", FONT_SM, COLOR_GREEN, panel_x + 20, y+10, center=False)
    # controls info
    draw_text(surf, "Shortcuts:", FONT_SM, COLOR_YELLOW, panel_x + 170, WINDOW_H - 160)
    draw_text(surf, "Ctrl+H = Reveal letter", FONT_XS, COLOR_TEXT, panel_x + 20, WINDOW_H - 130, center=False)
    draw_text(surf, "Ctrl+S = Skip (-penalty)", FONT_XS, COLOR_TEXT, panel_x + 20, WINDOW_H - 104, center=False)
    draw_text(surf, "Ctrl+R = Restart", FONT_XS, COLOR_TEXT, panel_x + 20, WINDOW_H - 78, center=False)
    draw_text(surf, "ESC = Menu", FONT_XS, COLOR_TEXT, panel_x + 20, WINDOW_H - 52, center=False)

# -------- MAIN --------
game = Game()

def main_loop():
    running = True
    while running:
        dt = clock.tick(FPS)
        screen.fill(COLOR_BG)
    

        # Draw central play area background panel
        central_x = 260
        central_w = WINDOW_W - central_x - 340
        pygame.draw.rect(screen, COLOR_PANEL, (central_x, 0, central_w, WINDOW_H))
        pygame.draw.rect(screen, (60, 65, 80), (central_x, 0, central_w, WINDOW_H), 2)

        # Draw right hint panel
        draw_right_hint_panel(screen, game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()

                # ESC -> menu
                if event.key == pygame.K_ESCAPE:
                    game.state = "menu"

                # If in menu, use Up/Down + Enter to choose
                if game.state == "menu":
                    if event.key == pygame.K_DOWN:
                        game.menu_index = (game.menu_index + 1) % len(game.left_items)
                    elif event.key == pygame.K_UP:
                        game.menu_index = (game.menu_index - 1) % len(game.left_items)
                    elif event.key == pygame.K_RETURN:
                        sel = game.left_items[game.menu_index]
                        if sel == "Play":
                            game.state = "play"
                            game.restart_game()
                        elif sel == "Settings":
                            game.state = "settings"
                        elif sel == "High Scores":
                            game.state = "scores"
                        elif sel == "Quit":
                            running = False

                # SETTINGS screen input (left/right/up/down change category/difficulty)
                elif game.state == "settings":
                    if event.key == pygame.K_LEFT:
                        # cycle categories by name (not using heavy lists)
                        cats = ["General", "Tech", "Sports", "Animals"]
                        idx = cats.index(game.category) if game.category in cats else 0
                        game.category = cats[(idx - 1) % len(cats)]
                        # NOTE: we keep WORDS global; category selection is for UI only here
                    elif event.key == pygame.K_RIGHT:
                        cats = ["General", "Tech", "Sports", "Animals"]
                        idx = cats.index(game.category) if game.category in cats else 0
                        game.category = cats[(idx + 1) % len(cats)]
                    elif event.key == pygame.K_UP:
                        diffs = ["Easy", "Medium", "Hard"]
                        idx = diffs.index(game.difficulty) if game.difficulty in diffs else 1
                        game.difficulty = diffs[(idx - 1) % len(diffs)]
                    elif event.key == pygame.K_DOWN:
                        diffs = ["Easy", "Medium", "Hard"]
                        idx = diffs.index(game.difficulty) if game.difficulty in diffs else 1
                        game.difficulty = diffs[(idx + 1) % len(diffs)]
                    elif event.key == pygame.K_RETURN:
                        # apply difficulty/time
                        if game.difficulty == "Easy":
                            game.time_limit = 25; game.points = 10
                        elif game.difficulty == "Medium":
                            game.time_limit = 18; game.points = 20
                        else:
                            game.time_limit = 12; game.points = 30
                        game.pick_new_word()
                        game.state = "menu"

                # HIGH SCORES screen navigation
                elif game.state == "scores":
                    if event.key == pygame.K_RETURN:
                        game.state = "menu"

                # PLAY mode input handling
                elif game.state == "play":
                    # Only consider Ctrl shortcuts when CTRL is pressed
                    if (mods & CTRL_MASK) != 0:
                        if event.key == pygame.K_h:
                            # reveal a letter (Ctrl+H)
                            game.reveal_letter()
                        elif event.key == pygame.K_s:
                            # skip word (Ctrl+S)
                            game.skip_word()
                        elif event.key == pygame.K_r:
                            # restart game (Ctrl+R)
                            game.restart_game()
                        # ignore other ctrl+letter combos
                        continue

                    # Normal typing (no single-letter shortcuts)
                    if event.key == pygame.K_BACKSPACE:
                        game.player_input = game.player_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        # submit
                        game.submit_answer()
                    else:
                        # accept printable letters only
                        if event.unicode and event.unicode.isalpha():
                            # append lower-case
                            game.player_input += event.unicode.lower()

                # GAMEOVER state: enter name or go to menu
                elif game.state == "gameover":
                    if event.key == pygame.K_RETURN and not game.name_entry:
                        # move to enter name state
                        game.name_entry = ""
                        game.state = "entername"
                    elif event.key == pygame.K_r and (mods & CTRL_MASK):
                        game.restart_game()
                        game.state = "play"
                    elif event.key == pygame.K_m:
                        game.state = "menu"

                elif game.state == "entername":
                    # typing player name
                    if event.key == pygame.K_BACKSPACE:
                        game.name_entry = game.name_entry[:-1]
                    elif event.key == pygame.K_RETURN:
                        name = game.name_entry.strip() or "PLAYER"
                        add_highscore(name, game.score)
                        game.name_entry = ""
                        game.state = "scores"
                    else:
                        if event.unicode and event.unicode.isprintable() and len(game.name_entry) < 14:
                            game.name_entry += event.unicode

        # -------- RENDER UI depending on state --------
        # Draw central UI inside central panel rectangle
        central_x = 260
        central_w = WINDOW_W - central_x - 340
        # draw panel header
        pygame.draw.rect(screen, COLOR_PANEL, (central_x, 0, central_w, 120))
        draw_text(screen, "WORD PUZZLE PRO", FONT_BIG, COLOR_ACCENT, central_x + central_w/2, 54)
        # draw small status line
        draw_text(screen, f"Score: {game.score}", FONT_SM, COLOR_TEXT, central_x + 20, 140, center=False)
        # state-specific render
        if game.state == "menu":
            # draw big menu area in center-right side (not left)
            y = 200
            for i, item in enumerate(game.left_items):
                is_active = (i == game.menu_index)
                color = COLOR_ACCENT if is_active else COLOR_TEXT
                rect = pygame.Rect(central_x + 80, y - 30, central_w - 160, 64)
                pygame.draw.rect(screen, (45,50,60) if is_active else (36,40,50), rect, border_radius=10)
                draw_text(screen, item, FONT_MED, color, rect.centerx, rect.centery)
                y += 100

            draw_text(screen, "Use UP/DOWN and ENTER to choose", FONT_SM, COLOR_GRAY, central_x + central_w/2, y + 10)
            draw_text(screen, "ESC = Menu (from any screen)", FONT_XS, COLOR_GRAY, central_x + central_w/2, y + 40)

        elif game.state == "settings":
            draw_text(screen, "SETTINGS", FONT_BIG, COLOR_ACCENT, central_x + central_w/2, 160)
            draw_text(screen, f"Category: {game.category}", FONT_MED, COLOR_TEXT, central_x + central_w/2, 260)
            draw_text(screen, f"Difficulty: {game.difficulty}", FONT_MED, COLOR_TEXT, central_x + central_w/2, 320)
            draw_text(screen, "Left/Right to change category, Up/Down difficulty, Enter to apply", FONT_XS, COLOR_GRAY, central_x + central_w/2, 420)

        elif game.state == "scores":
            draw_text(screen, "HIGH SCORES", FONT_BIG, COLOR_ACCENT, central_x + central_w/2, 120)
            highs = load_highscores()[:MAX_HIGHS]
            y = 180
            if not highs:
                draw_text(screen, "No highscores saved yet", FONT_MED, COLOR_GRAY, central_x + central_w/2, y)
            else:
                for rec in highs:
                    draw_text(screen, f"{rec['name'][:12]:12s}  {rec['score']:>5d}  {rec['date'][:10]}", FONT_SM, COLOR_TEXT, central_x + central_w/2, y)
                    y += 30
            draw_text(screen, "Press ENTER to return to menu", FONT_XS, COLOR_GRAY, central_x + central_w/2, WINDOW_H - 60)

        elif game.state == "play":
            # update timer
            time_left = game.update_timer()
            draw_text(screen, f"Time: {int(time_left)}", FONT_SM, COLOR_YELLOW, central_x + central_w - 120, 140)
            # scrambled word
            draw_text(screen, "Unscramble:", FONT_MED, COLOR_GRAY, central_x + central_w/2, 190)
            draw_text(screen, game.scrambled.upper(), FONT_BIG, COLOR_ACCENT, central_x + central_w/2, 260)
            # input box
            box_rect = pygame.Rect(central_x + (central_w//2) - 260, 330, 520, 70)
            pygame.draw.rect(screen, (36,40,50), box_rect, border_radius=8)
            pygame.draw.rect(screen, (60,70,90), box_rect, 2, border_radius=8)
            draw_text(screen, game.player_input.upper(), FONT_MED, COLOR_TEXT, box_rect.centerx, box_rect.centery)
            # hint preview (a short line)
            draw_text(screen, f"Hint preview: {game.hint[:60]}{'...' if len(game.hint) > 60 else ''}", FONT_SM, COLOR_GRAY, central_x + 20, 420, center=False)
            draw_text(screen, "Type answer then ENTER to submit", FONT_XS, COLOR_GRAY, central_x + central_w/2, 520)
            draw_text(screen, "Use Ctrl+H (reveal), Ctrl+S (skip), Ctrl+R (restart)", FONT_XS, COLOR_GRAY, central_x + central_w/2, 548)

        elif game.state == "gameover":
            draw_text(screen, "GAME OVER", FONT_BIG, COLOR_RED, central_x + central_w/2, 160)
            draw_text(screen, game.gameover_reason, FONT_MED, COLOR_TEXT, central_x + central_w/2, 240)
            draw_text(screen, f"Score: {game.score}", FONT_MED, COLOR_YELLOW, central_x + central_w/2, 300)
            draw_text(screen, "Press ENTER to save score, CTRL+R restart, ESC menu", FONT_XS, COLOR_GRAY, central_x + central_w/2, 360)

        elif game.state == "entername":
            draw_text(screen, "SAVE SCORE", FONT_BIG, COLOR_ACCENT, central_x + central_w/2, 160)
            draw_text(screen, f"Score: {game.score}", FONT_MED, COLOR_TEXT, central_x + central_w/2, 220)
            # input rectangle
            name_rect = pygame.Rect(central_x + (central_w//2) - 200, 280, 400, 60)
            pygame.draw.rect(screen, (36,40,50), name_rect, border_radius=8)
            pygame.draw.rect(screen, (60,70,90), name_rect, 2, border_radius=8)
            draw_text(screen, game.name_entry.upper() or "(type name)", FONT_MED, COLOR_TEXT, name_rect.centerx, name_rect.centery)
            draw_text(screen, "Press ENTER to save", FONT_XS, COLOR_GRAY, central_x + central_w/2, 360)

        # draw the right-side hint panel (already drawn background)
        # (function draw_right_hint_panel handled rendering contents)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()
