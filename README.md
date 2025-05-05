# 🦖 Dino Runner Game

A Python remake of the classic "Chrome Dino" game, built with **Pygame**!  
Run, jump, duck, and survive as long as you can while dodging obstacles in a desert landscape.

---

## Game Features

- Smooth 60 FPS gameplay
- Running, jumping, and ducking mechanics
- Randomly generated obstacles (Cactus and Ptera)
- Moving clouds and stars in the background
- Increasing difficulty with time
- Cheat codes for fun and testing
- Custom pixelated score display
- Game over screen and high score tracking
- Sound effects for jumping, dying, and point milestones

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/dino-runner.git
   cd dino-runner

2. **Install Required Libraries**

bash
```
pip install pygame
```

3. **Prepare the Assets**

- Create a folder named Assets/
- Inside it, add subfolders:
    -   Assets/Dino/ (Dino images)
    -   Assets/Cactus/ (Cactus images)
    -   Assets/Ptera/ (Bird images)
    -   Assets/ (for ground, cloud, game_over, replay, numbers.png, stars.png)
    -   Sounds Folder
        - Create a Sounds/ folder
        - Add sounds:
            - jump.mp3
            - die.mp3
            - points.mp3

4. **How to Play**
- SPACE or UP Arrow → Jump
- DOWN Arrow → Duck
- ESC or Q → Quit Game
- Mouse Click on "Replay" → Restart after dying

5. **Cheat Codes**
While playing, you can type these codes (no need to press ENTER):
- GODMODE ~	Become invincible (no collision death)
- DNCYCLE ~ Toggle day/night background
- IAMRICH ~	Instantly add 10,000 points
- HISCORE ~	Set high score to 99,999
- SPEEDUP ~	Increase game speed


6. **Future Improvements (Optional Ideas)**
- Add a Pause/Resume feature
- Power-ups (e.g., Shield, Double Jump, Speed Boost)
- Day and Night cycle after a certain score
- New enemy types (meteor showers, rolling rocks)
- Background music
- Online Leaderboard integration

7. **License**
This project is open-sourced for learning and fun.
Feel free to modify and use it — but give credit if you share it publicly! 😊

8. **Acknowledgements**
Inspired by the Google Chrome offline Dino Game.
Built using Python and Pygame <3.