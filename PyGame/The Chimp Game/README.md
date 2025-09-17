# Memory Circle Game 🎯

A memory & reflex game built with **Python + Pygame**.  
The player must click the circles in alphabetical order (A → B → C → …) without making a mistake.  
Levels get harder as more circles are added. Run out of lives, and it’s game over!

---

## 🎮 Features
- Randomly placed non-overlapping circles each round
- Progressive difficulty: each new level adds one more circle
- Lives system with visual feedback (circle colors change as lives decrease)
- Sound effects for:
  - ✅ Correct click (`pop.mp3`)
  - ⭐ Level clear (`bubbles.mp3`)
  - ❌ Wrong click (`error.mp3`)
- Game states:
  - **Intro** → choose a level by pressing a letter key or start with `A`
  - **Play** → click circles in order
  - **Win** → pass the round and level up
  - **Lose** → lose a life, retry
  - **Game Over** → restart by pressing `SPACE`

---

## 🖥️ Requirements
- Python 3.9+  
- [Pygame](https://www.pygame.org/news)

Install dependencies:
```bash
pip install pygame
