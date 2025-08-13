import random
from skills import Skill as Ability
from player import Player

def choose_target(enemies):
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
    player.actual_mana = min(player.mana, player.actual_mana + player.mana_regen)
    player.actual_hp = min(player.hp, player.actual_hp + player.hp_regen)

def print_status(player, enemies):
    print(f"\n{player.name} - HP: {player.actual_hp}, Mana: {player.actual_mana}, XP: {player.xp}/{player.xp_to_next_level}, Level: {player.level}")
    print("\nEnemies' status:")
    for enemy in enemies:
        print(f"{enemy.name} - HP: {enemy.actual_hp}, Mana: {enemy.actual_mana}")

def generate_boss(players, enemie_list):
    boss_names = ["Goblin King", "Dragon Lord", "Necromancer", "Dark Knight"]
    boss = Player(random.choice(boss_names), is_bot=True)
    boss.level = 0
    print(f"A wild {boss.name} has appeared!")
    for player in players:
        boss.level_up()
    players.append(boss)
    enemie_list.append(boss)
    boss.ability_selector(6)
    for player in players:
        player.ability_selector(3)
    boss.print_stats()

def generate_random_event_player(player=None):
    events = {
        "gain_experience": "You gained some experience!",
        "learn_skill": "You learned a new skill!",
        "level_up": "You leveled up!",
    }
    print(f"{player.name} is trying to trigger a random event...")
    if player is None:
        return

    if random.randint(1, 10) <= 10:  # 100% chance for testing
        random_event = random.choice(list(events.keys()))
        event = events[random_event]
        if random_event == "gain_experience":
            xp_gain = random.randint(10, 50)
            player.xp += xp_gain
            print(f"{player.name} {event} (+{xp_gain} XP)")
        elif random_event == "learn_skill":
            player.select_boost(is_bot=True)
        elif random_event == "level_up":
            player.level += 1
            print(f"{player.name} {event} to Level {player.level}!")
    else:
        print(f"{player.name} tried to trigger an event but nothing happened.")
    
def enemy_attack(enemy, player, enemies, all_players, event_cooldown ,is_boss=False ):
    ability = random.choice(enemy.abilities)
    if ability.type in ["damage", "effect"]:
        target = random.choice([p for p in all_players if p != enemy]) 
        print(f"{enemy.name} is targeting {target.name} with {ability.name}")
        enemy.use_ability(ability.name, target)
    elif ability.type == "event" and event_cooldown == 0:
        print(f"{enemy.name} triggered an event!")
        generate_boss(all_players, enemies)
        enemy.remove_ability(ability.name)
    elif ability.type == "heal" and is_boss:
        print(f"{enemy.name} tried to heal but failed, applying damage to itself.")
        enemy.receive_damage(ability.damage, random.choice(["fire", "ice", "earth", "water"]), None)
    else:
        enemy.use_ability(ability.name)

def main():
    boss_names = ["Goblin King", "Dragon Lord", "Necromancer", "Dark Knight"]
    rounds = 3
    player_name = input("Enter your name: ")
    player = Player(player_name, is_bot=False)
    player.ability_selector(rounds)

    num_enemies = int(input("How many enemies do you want to fight? "))
    enemies = [Player(f"Enemy{i+1}", is_bot=True) for i in range(num_enemies)]
    all_players = [player] + enemies
    for enemy in enemies:
        enemy.ability_selector(rounds)
    event_cooldown = 0
    while player.actual_hp > 0 and any(enemy.actual_hp > 0 for enemy in enemies):

        player.check_effects()


        for enemy in enemies:
            enemy.check_effects()
        print("\nYour turn!")
        print("Your abilities:", [a.name for a in player.abilities])
        ability_name = input(f"{player.name}, choose an ability to use: ")

        selected_ability = next((a for a in player.abilities if a.name == ability_name), None)
        if selected_ability:
            if selected_ability.type == "damage" or (selected_ability.type == "effect" and selected_ability.element == "poison"):
                target = choose_target(enemies)
                player.use_ability(ability_name, target)

            elif selected_ability.type == "event" and event_cooldown == 0:
                print(f"{player.name} triggered an event!")
                generate_boss(all_players, enemies)
                player.remove_ability(ability_name)
                event_cooldown = 5
            else:
                player.use_ability(ability_name)
        else:
            print(f"{player.name} failed to cast an attack.")

        #Enemies turn

        for enemy in enemies:
            if enemy.name not in boss_names and enemy.actual_hp > 0:
                enemy_attack(enemy, player, enemies,all_players, event_cooldown)
            elif enemy.name in boss_names and enemy.actual_hp > 0:
                print(f"{enemy.name} is preparing for a powerful attack!")
                for _ in range(2):
                    enemy_attack(enemy, player, enemies, all_players, event_cooldown ,is_boss=True)

        for enemy in enemies:    
            if enemy.actual_hp <= 0:
                continue
            if player.actual_hp <= 0:
                break

        regen(player)
        if event_cooldown > 0:
            event_cooldown -= 1
        print_status(player, enemies)

        player.check_level_up()
        for enemy in enemies [:]:
            enemy.check_level_up()
            if enemy.actual_hp <= 0:
                print(f"{enemy.name} has been defeated!")
                enemies.remove(enemy)
                all_players.remove(enemy)
        if player.actual_hp <= 0:
            print("Game Over! You have been defeated.")
            break
        if all(enemy.actual_hp <= 0 for enemy in enemies):
            print("Victory! All enemies defeated.")
            break

if __name__ == "__main__":
    main()
