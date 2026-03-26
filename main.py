import random
from skills import Skill
from player import Player
from player_data import *

# -----------------------
# Utility Functions
# -----------------------

def choose_target(enemies):
    """Let player choose a living enemy to attack."""
    alive_enemies = [enemy for enemy in enemies if enemy.actual_hp > 0]
    for idx, enemy in enumerate(alive_enemies):
        print(f"{idx+1}: {enemy.name} (HP: {enemy.actual_hp})")
    while True:
        try:
            choice = int(input("Choose enemy number to attack: ")) - 1
            if 0 <= choice < len(alive_enemies):
                return alive_enemies[choice]
        except ValueError:
            pass
        print("Invalid choice. Try again.")

def regen(player):
    """Regenerate HP and Mana each turn."""
    player.actual_mana = min(player.mana, player.actual_mana + player.mana_regen)
    player.actual_hp = min(player.hp, player.actual_hp + player.hp_regen)


def print_status(player, enemies):
    """Print current status of player and enemies."""
    print(f"\n{player.name} - HP: {player.actual_hp}, Mana: {player.actual_mana}, "
          f"XP: {player.xp}/{player.xp_to_next_level}, Level: {player.level}")
    print("\nEnemies' status:")
    for enemy in enemies:
        print(f"{enemy.name} - HP: {enemy.actual_hp}, Mana: {enemy.actual_mana}")


def generate_boss(players, enemies):
    """Spawn a boss enemy scaled to player levels."""
    boss_names = ["Goblin King", "Dragon Lord", "Necromancer", "Dark Knight"]
    boss = Player(random.choice(boss_names), is_bot=True)
    print(f"\n⚠ A wild {boss.name} has appeared! ⚠")
    
    avg_level = sum(p.level for p in players) // len(players)
    boss.level = avg_level
    boss.ability_selector(6)
    for player in players:
        player.ability_selector(3)
    boss.print_stats()

    enemies.append(boss)
    players.append(boss)


def generate_random_event_player(player):
    """Trigger a random beneficial event for a player."""
    if not player:
        return

    events = {
        "gain_experience": "You gained some experience!",
        "learn_skill": "You learned a new skill!",
        "level_up": "You leveled up!"
    }

    print(f"{player.name} is trying to trigger a random event...")
    if random.randint(1, 10) <= 1:  # 10% chance for testing
        event_type = random.choice(list(events.keys()))
        print(f"{player.name} {events[event_type]}")

        if event_type == "gain_experience":
            xp_gain = random.randint(10, 50)
            player.xp += xp_gain
            print(f"(+{xp_gain} XP)")
        elif event_type == "learn_skill":
            player.select_boost(is_bot=True)
        elif event_type == "level_up":
            player.level += 1
    else:
        print("Nothing happened.")


def enemy_attack(enemy, players, enemies ,event_cooldown, is_boss=False):
    """Handle enemy AI attack logic."""
    ability = random.choice(enemy.abilities)

    if ability.type in {"damage", "effect"}:
        targets = [p for p in players if p != enemy and p.actual_hp > 0]
        if targets:
            target = random.choice(targets)
            print(f"{enemy.name} is targeting {target.name} with {ability.name}")
            hits = enemy.check_double_hit(ability)
            if hits > 1:
                enemy.use_ability(ability.name, False ,target)
                for _ in range(hits):
                    print(f"{enemy.name} landed a double hit on {target.name} with {ability.name}!")
                    enemy.use_ability(ability.name, True ,target)
            else:
                enemy.use_ability(ability.name, False ,target)
    elif ability.type == "event" and event_cooldown == 0:
        print(f"{enemy.name} triggered an event!")
        event_cooldown = 5
        generate_boss(players, enemies)
        enemy.remove_ability(ability.name)
    elif ability.type == "event" and event_cooldown > 0:
        print(f"{enemy.name} tried to trigger an event but failed due to cooldown.")
    elif ability.type == "heal" and is_boss:
        print(f"{enemy.name} tried to heal but failed, taking self-damage.")
        enemy.receive_damage(
            ability.damage*100,
            random.choice(["fire", "ice", "earth", "water"]),
            None
        )
    else:
        enemy.use_ability(ability.name)


# -----------------------
# Main Game Loop
# -----------------------


def main():
    boss_names = {"Goblin King", "Dragon Lord", "Necromancer", "Dark Knight"}
    rounds = 3
    event_cooldown = 5
    conn = try_connection()
    init_data(conn)
    players = get_players(conn)
    if players:
        print("Existing players:")
        for name, level in players:
            print(f"- {name} (Lv.{level})")
    print("'x' to exit.")
    player_name = input("Enter your name: ")
    if player_name == "x":
        return
    player = load_player(conn, player_name)

    if player:
        print(f"Loaded existing player: {player.name} (Level {player.level})")
        player.ability_selector(rounds)
    else:
        print("Creating new player...")
        player = Player(player_name, is_bot=False)
        player.ability_selector(rounds)
        save_player(conn, player)

    # Enemies setup
    num_enemies = int(input("How many enemies do you want to fight? "))
    enemies = [Player(f"Enemy{i+1}", is_bot=True) for i in range(num_enemies)]
    for enemy in enemies:
        enemy.ability_selector(rounds)

    all_players = [player] + enemies

    # Game loop
    while player.actual_hp > 0 and any(e.actual_hp > 0 for e in enemies):
        # Status effects
        player.check_effects()
        for enemy in enemies:
            enemy.check_effects()

        # Player turn
        print("\nYour turn!")
        print("Your abilities:", [a.name for a in player.abilities])
        ability_name = input(f"{player.name}, choose an ability: ").strip()

        selected_ability = next((a for a in player.abilities if a.name == ability_name), None)
        if not selected_ability:
            print("Invalid ability name.")
        else:
            if selected_ability.type in {"damage", "effect"} or selected_ability.element == "poison":
                target = choose_target(enemies)
                if target:
                    hits = player.check_double_hit(selected_ability)
                    if hits > 1:
                        player.use_ability(ability_name, False ,target)
                        for _ in range(hits):
                            print(f"{player.name} landed a double hit on {target.name} with {selected_ability.name}!")
                            player.use_ability(ability_name, True ,target)
                    else:
                        player.use_ability(ability_name, False ,target)
            elif selected_ability.type == "event" and event_cooldown == 0:
                print(f"{player.name} triggered an event!")
                generate_boss(all_players, enemies)
                player.remove_ability(ability_name)
                event_cooldown = 5
            elif selected_ability.type == "event" and event_cooldown > 0:
                print(f"{enemy.name} tried to trigger an event but failed due to cooldown.")
            else:
                player.use_ability(ability_name)

        # Enemies turn
        for enemy in enemies[:]:  
            if enemy.actual_hp <= 0:
                continue
            if enemy.name in boss_names:
                print(f"{enemy.name} is preparing for a powerful attack!")
                for _ in range(2):
                    enemy_attack(enemy, all_players, enemies,event_cooldown, is_boss=True)
            else:
                enemy_attack(enemy, all_players, enemies,event_cooldown)

        
        # Win/Loss conditions
        if player.actual_hp <= 0:
            print("Game Over! You have been defeated.")
            player.level = max(1, int(player.level * 0.5))
            save_player(conn, player)
            main()
        if all(e.actual_hp <= 0 for e in enemies):
            print("Victory! All enemies defeated.")
            main()
        # Level up checks
        player.check_level_up()
        for enemy in enemies[:]:
            enemy.check_level_up()
            if enemy.actual_hp <= 0:
                print(f"{enemy.name} has been defeated!")
                enemies.remove(enemy)
                all_players.remove(enemy)

        # Status display
        print_status(player, enemies)

        # Event cooldown management
        if event_cooldown > 0:
            event_cooldown -= 1

        # Regen phase
        regen(player)
        save_player(conn, player)




if __name__ == "__main__":
    main()

    # Notes for myself:
    # - Finally improved code legibility and structure in main, need to do the same in player.py.
    # - Need to make it DRY by refactoring common logic.
    # - Consider adding more enemy types and abilities.
    # - Implement more complex enemy AI strategies.
    # - Add more random events and player interactions.
    # - The project is still in early stages, so expect bugs and incomplete features.
    # - The project is going pretty well, but there's always room for improvement. :D
