# 🎮 Atari Breakout Game with MySQL Integration

A classic Atari Breakout game built with Python and Pygame, featuring multiple game modes, power-ups, and MySQL database integration for score tracking and session management.

## 🎯 Features

### Game Modes

- **Single Player**: Classic breakout gameplay against the computer
- **Double Player**: Two-player competitive mode
- **Rule-based AI**: Watch AI play with intelligent paddle movement

### Power-ups

- 🛡️ **Extra Lives**: Get additional chances to keep playing
- ⭐ **Bonus Points**: Add your score with special blocks
- 📏 **Paddle Resizing**: Temporarily increase or decrease paddle size
- ⚡ **Speed Boost**: Faster ball movement for increased difficulty

### Technical Features

- Object-Oriented Programming (OOP) architecture
- MySQL database integration for persistent data storage
- Session management system
- Interactive and user-friendly UI design
- Real-time score tracking and leaderboards

## 🚀 Getting Started

### Prerequisites

Before running the game, make sure you have the following installed:

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/atari-breakout-game.git
   cd atari-breakout-game
   ```

2. **Install required packages**

   ```bash
   pip install pygame mysql-connector-python
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

## 🎮 How to Play

### Controls

- **Single Player Mode**:

  - `←` / `→` Arrow Keys: Move paddle left/right
  - `SPACE`: Launch ball
  - `ESC`: Pause game
 

- **Double Player Mode**:
  - Player 1: `A` / `D` keys
  - Player 2: `←` / `→` Arrow keys

### Objective

- Break all the blocks using the ball
- Collect power-ups to enhance gameplay
- Achieve the highest score possible
- Don't let the ball fall below your paddle!

## 🏆 Database Schema

The game uses the following main tables:

- `users`: Store player information and statistics
- `statistics`: Track user statistics
- `scores`: High score leaderboard

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Pygame**: Game development framework
- **MySQL**: Database for persistent storage
- **mysql-connector-python**: MySQL database connector

## 👨‍💻 Author

**Atharva Jain**

- GitHub: [@Atharva804](https://github.com/Atharva804)
- LinkedIn: [Atharva Jain](https://www.linkedin.com/in/atharva-jain-65a192290/)
