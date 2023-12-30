# Pixel Pacer

The "Pixel Pacer" game is a simple side-scrolling obstacle avoidance game created using the Pygame library in Python. Players control a character that can jump over obstacles to score points. The game features basic graphics and sound effects.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Game Overview](#game-overview)
- [Game Mechanics](#game-mechanics)
- [Credits](#credits)
- [License](#license)

## Features

- **Player Control:** The player can control the character using the space bar to jump over obstacles.
- **Obstacle Variety:** Two types of obstacles, snails and flies, appear randomly for the player to avoid.
- **Scoring System:** The player's score is based on the time survived in the game.
- **Graphics and Sound:** The game includes basic pixel art graphics and sound effects for jumping and background music.

## Requirements

- Python
- Pygame library

## How to Run

1. Make sure you have Python installed on your system.
2. Install the Pygame library using the following command:

   ```bash
   pip install pygame
   ```
3. Clone the repository:
   ```bash
   git clone https://github.com/thevoidop/pixel_pacer.git
   cd pixel-pacer-game
   ```

4. Run the game:

    ```bash
    python pixel_pacer.py
    ```
    Press the space bar to start playing.

## Game Overview
The game features a simple side-scrolling environment where the player must jump over incoming obstacles to survive. The goal is to achieve the highest score possible by avoiding collisions with obstacles.

## Game Mechanics
- **Player Class (Player):**

The player character is represented by a sprite with walking and jumping animations.
The player can jump by pressing the space bar, and a jump sound effect is played.
Gravity is applied to simulate a jumping motion, and the character's animation changes based on the jump state.

- **Obstacle Class (Obstacle):**
  
Two types of obstacles, snails and flies, are represented by sprites with animation frames.
Obstacles move from right to left on the screen, and new obstacles are added at regular intervals.
Obstacles are randomly chosen, with a higher probability of snails appearing.

- **Game Flow:**

The game initializes with a title screen displaying the game name and instructions to press the space bar to play.
Once the player presses the space bar, the game begins, and obstacles start appearing.
The player's score is displayed at the top of the screen, indicating the time survived.
If the player collides with an obstacle, the game ends, and the final score is displayed.
The player can restart the game by pressing the space bar.

## Credits
  
**Graphics:** The pixel art graphics used in the game are located in the "graphics" folder.

**Audio:** Sound effects and background music are located in the "audio" folder.

**Fonts:** The pixelated font used in the game is located in the "fonts" folder.

## License
This project is licensed under the MIT License 
