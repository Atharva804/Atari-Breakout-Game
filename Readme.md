# 🎮 Atari Breakout Game with MySQL Integration

A classic Atari Breakout game built with Python and Pygame, featuring multiple game modes, power-ups, and MySQL database integration for score tracking and session management.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-v2.0+-green.svg)
![MySQL](https://img.shields.io/badge/mysql-v8.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Features

### Game Modes

- **Single Player**: Classic breakout gameplay against the computer
- **Double Player**: Two-player competitive mode
- **Rule-based AI**: Watch AI play with intelligent paddle movement

### Power-ups

- 🛡️ **Extra Lives**: Get additional chances to keep playing
- ⭐ **Bonus Points**: Multiply your score with special blocks
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
   pip install -r requirements.txt
   ```

3. **Set up MySQL Database**

   Create a new MySQL database and update the connection settings in the configuration file:

   ```sql
   CREATE DATABASE breakout_game;
   USE breakout_game;
   ```

   The application will automatically create the necessary tables on first run.

4. **Configure Database Connection**

   Update the database configuration in `config.py`:

   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'breakout_game'
   }
   ```

5. **Run the game**
   ```bash
   python main.py
   ```

## 🎮 How to Play

### Controls

- **Single Player Mode**:

  - `←` / `→` Arrow Keys: Move paddle left/right
  - `SPACE`: Launch ball
  - `P`: Pause game
  - `ESC`: Return to main menu

- **Double Player Mode**:
  - Player 1: `A` / `D` keys
  - Player 2: `←` / `→` Arrow keys

### Objective

- Break all the blocks using the ball
- Collect power-ups to enhance gameplay
- Achieve the highest score possible
- Don't let the ball fall below your paddle!

## 📁 Project Structure

```
atari-breakout-game/
│
├── main.py                 # Main game entry point
├── config.py               # Database and game configuration
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
├── game/
│   ├── __init__.py
│   ├── game_engine.py     # Core game logic
│   ├── player.py          # Player class and management
│   ├── ball.py            # Ball physics and behavior
│   ├── paddle.py          # Paddle mechanics
│   ├── blocks.py          # Block generation and management
│   ├── powerups.py        # Power-up system
│   └── ai_player.py       # AI logic for rule-based gameplay
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py      # Database connection and operations
│   ├── session_manager.py # User session handling
│   └── score_manager.py   # Score tracking and leaderboards
│
├── ui/
│   ├── __init__.py
│   ├── menu.py            # Main menu interface
│   ├── game_ui.py         # In-game UI elements
│   └── leaderboard.py     # Score display interface
│
└── assets/
    ├── images/            # Game sprites and graphics
    ├── sounds/            # Audio files
    └── fonts/             # Custom fonts
```

## 🏆 Database Schema

The game uses the following main tables:

- `players`: Store player information and statistics
- `game_sessions`: Track individual game sessions
- `scores`: High score leaderboard
- `powerups_collected`: Power-up collection history

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Pygame**: Game development framework
- **MySQL**: Database for persistent storage
- **mysql-connector-python**: MySQL database connector

## 📋 Requirements

Create a `requirements.txt` file with:

```
pygame>=2.1.0
mysql-connector-python>=8.0.32
numpy>=1.21.0
```

## 🎨 Screenshots

_Add screenshots of your game here showing different modes and gameplay_

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Performance may vary on older hardware
- Some power-ups may occasionally overlap
- AI difficulty could be adjusted for better gameplay balance

## 🔄 Future Enhancements

- [ ] Add sound effects and background music
- [ ] Implement online multiplayer mode
- [ ] Add more power-up types
- [ ] Create level editor functionality
- [ ] Add animated backgrounds and particle effects

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Inspired by the classic Atari Breakout game
- Thanks to the Pygame community for excellent documentation
- MySQL documentation for database integration guidance

---

⭐ Star this repository if you found it helpful!
