# Fab's Python RPG

A turn-based RPG simulator built in Python featuring abilities, combat mechanics, leveling systems, and persistent data storage using MySQL.

---

## Features

- Turn-based combat system
- Ability system (damage, heal, buffs, effects)
- Player progression (XP, leveling, stats)
- Random events and boss fights
- Object-oriented design (classes, modular structure)
- Data persistence using MySQL

---

## Tech Stack

- Python
- MySQL
- Docker
- OOP (Object-Oriented Programming)

---

## Requirements

Make sure you have:

- Python 3.10+
- Docker

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Database Setup (Docker)

This project uses MySQL for persistent storage. You can quickly start a database instance using Docker:

```bash
docker run --name rpg-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=rpg_game -p 3306:3306 -v mysql_data:/var/lib/mysql -d mysql:8
```

### What this does

- Creates a MySQL container named `rpg-mysql`
- Sets root password to `root`
- Creates a database called `rpg_game`
- Exposes MySQL on port `3306`
- Persists data using a Docker volume

---

## Running the Project

```bash
python main.py
```

---

## Verify Database Connection

Make sure the container is running:

```bash
docker ps
```

If it's not running:

```bash
docker start rpg-mysql
```

---

## Stopping the Database

```bash
docker stop rpg-mysql
```

---

## Future Improvements

- Save/load full player state (stats, abilities)
- Leaderboard system
- Authentication system
- Improved enemy AI
- More abilities and game mechanics

---

## Notes

- The project is still under development
- Some features may be incomplete or experimental