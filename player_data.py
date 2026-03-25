import mysql.connector
from player import Player

def try_connection():
  try:
      conn = mysql.connector.connect(
          host="localhost",
          user="root",
          password="root",
          database="rpg_game"
      )
      print("Connected to MySQL!")
      return conn
  except Exception as e:
      print("Error:", e)
      return None

def init_data(conn):
    cursor = conn.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS players (
          id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(50),
          level INT,
          xp INT,
          xp_to_next_level INT
      )
      """)
    conn.commit()

def get_players(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name, level FROM players")

    players = cursor.fetchall()

    cursor.close()
    return players

def create_player(conn):
    print("Create a new player!")

    while True:
        name = input("Name: ")
        players = get_players(conn)  
        player_names = [p[0] for p in players]

        if name in player_names:
            print("There's already a player with that name")
        else:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO players (name, level, xp, xp_to_next_level) VALUES (%s, %s, %s, %s)",
                (name, 1, 0, 100)
            )
            conn.commit()
            cursor.close()

            print(f"Player {name} created!")

            return name
        
def load_player(conn, name):
    data = get_player_by_name(conn, name)

    if not data:
        return None

    name, level, xp, xp_to_next = data

    player = Player(name, is_bot=False)
    player.level = level
    player.xp = xp
    player.xp_to_next_level = xp_to_next

    return player

def get_player_by_name(conn, name):
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT name, level, xp, xp_to_next_level FROM players WHERE name = %s",
        (name,)
    )
    
    result = cursor.fetchone()
    cursor.close()
    
    return result

def save_player(conn, player):
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM players WHERE name = %s", (player.name,))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE players 
            SET level=%s, xp=%s, xp_to_next_level=%s
            WHERE name=%s
        """, (player.level, player.xp, player.xp_to_next_level, player.name))
    else:
        cursor.execute("""
            INSERT INTO players (name, level, xp, xp_to_next_level)
            VALUES (%s, %s, %s, %s)
        """, (player.name, player.level, player.xp, player.xp_to_next_level))

    conn.commit()
    cursor.close()
