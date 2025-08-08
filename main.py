import random
from skills import Skill as Ability
from player import Player

def choose_target(enemies):
    alive_enemies = [enemy for enemy in enemies if enemy.atual_hp > 0]
    for idx, enemy in enumerate(alive_enemies):
        print(f"{idx+1}: {enemy.name} (HP: {enemy.atual_hp})")
    while True:
        try:
            choice = int(input("Choose enemy number to attack: ")) - 1
            if 0 <= choice < len(alive_enemies):
                return alive_enemies[choice]
        except ValueError:
            pass
        print("Invalid choice. Try again.")

def regen(player):
    player.atual_mana = min(player.mana, player.atual_mana + player.mana_regen)
    player.atual_hp = min(player.hp, player.atual_hp + player.hp_regen)

def print_status(player, enemies):
    print(f"\n{player.name} - HP: {player.atual_hp}, Mana: {player.atual_mana}")
    print("\nEnemies' status:")
    for enemy in enemies:
        print(f"{enemy.name} - HP: {enemy.atual_hp}, Mana: {enemy.atual_mana}")

def main():
    rounds = 3
    player_name = input("Enter your name: ")
    player = Player(player_name, is_bot=False)
    player.ability_selector(rounds)

    num_enemies = int(input("How many enemies do you want to fight? "))
    enemies = [Player(f"Enemy{i+1}", is_bot=True) for i in range(num_enemies)]
    for enemy in enemies:
        enemy.ability_selector(rounds)

    while player.atual_hp > 0 and any(enemy.atual_hp > 0 for enemy in enemies):
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
            else:
                player.use_ability(ability_name)
        else:
            print(f"Ability {ability_name} not found or not learned yet.")

        regen(player)

        print_status(player, enemies)

        for enemy in enemies:
            enemy.check_effects()
            if enemy.atual_hp <= 0:
                continue
            if player.atual_hp <= 0:
                break
            if enemy.abilities:
                ability = random.choice(enemy.abilities)
                if ability.type in ["damage", "effect"]:
                    target = random.choice([player] + [e for e in enemies if e != enemy])
                    print(f"{enemy.name} is targeting {target.name} with {ability.name}")
                    enemy.use_ability(ability.name, target)
                else:
                    enemy.use_ability(ability.name)

        if player.atual_hp <= 0:
            print("Game Over! You have been defeated.")
            break
        if all(enemy.atual_hp <= 0 for enemy in enemies):
            print("Victory! All enemies defeated.")
            break

if __name__ == "__main__":
    main()
