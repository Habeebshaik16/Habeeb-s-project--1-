# 🎮 Word Puzzle Game (Python + Pygame)

A fast and interactive **word-scramble puzzle game** built using **Python** and **Pygame**.  
Players must **unscramble words**, use **logical hints**, beat the **countdown timer**,  
and reach high scores — all inside a clean, panel-based GUI layout.

This game is perfect for improving vocabulary and learning Python GUI programming.

---

## ✨ Features

### 🎮 Gameplay
- Scramble and guess words from **100+ vocabulary words**
- Fully windowed layout: **1280 × 720**
- Real-time smooth typing (no delay)
- Game-over system with correct word reveal
- Professional menu navigation (Play, Settings, Highscores, Quit)

### 💡 Hint System
Right-side hint panel includes:
- Full sentence clue for each word  
- Revealed letters (progressive hint)  
- Hint preview below input box  

### ⌨️ Shortcuts (No conflict with typing)
| Action | Shortcut |
|--------|----------|
| Reveal 1 Letter | **Ctrl + H** |
| Skip Word | **Ctrl + S** |
| Restart Game | **Ctrl + R** |
| Back to Menu | **ESC** |

*No single letter is used as a shortcut so typing stays smooth.*

### 🏆 High Score System
- Saves scores in **highscores.json**
- Enter your name after game-over
- Scores sorted automatically
- Stores score + date

### ⚙️ Settings Menu
- Difficulty Levels: **Easy / Medium / Hard**
- Categories: **General, Tech, Sports, Animals**
- Time & points adjust with difficulty

### 🧱 UI Layout
Clean 3-panel design:


---

## 🚀 How to Run

### 1. Install Pygame  
```bash
pip install pygame
python word_puzzle_final.py

