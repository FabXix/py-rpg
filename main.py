import random

from skills import Skill as Ability
from player import Player



player_name = input("Enter your name: ")
player = Player(player_name, is_bot=False)
player.ability_selector(3)

num_enemies = int(input("How many enemies do you want to fight? "))
enemies = [Player(f"Enemy{i+1}", is_bot=True) for i in range(num_enemies)]
for enemy in enemies:
    enemy.ability_selector(3)
while player.atual_hp > 0 and any(enemy.atual_hp > 0 for enemy in enemies):
    for enemy in enemies:
        enemy.check_effects()
    player.check_effects()

    print("\nYour turn!")

    print("Your abilities:", [a.name for a in player.abilities])
    ability_name = input(f"{player.name}, choose an ability to use: ")
    if ability_name in [ability.name for ability in player.abilities]:
        damage, element = player.use_ability(ability_name)
        if damage > 0:            
            alive_enemies = [enemy for enemy in enemies if enemy.atual_hp > 0]
            for idx, enemy in enumerate(alive_enemies):
                print(f"{idx+1}: {enemy.name} (HP: {enemy.atual_hp})")
            target_idx = int(input("Choose enemy number to attack: ")) - 1
            target_enemy = alive_enemies[target_idx]
            target_enemy.receive_damage(damage, element)
    else:
        print(f"Ability {ability_name} not found or not learned yet.")
    player.atual_mana += player.mana_regen
    player.atual_hp += player.hp_regen
    if player.atual_mana > player.mana:
        player.atual_mana = player.mana
    if player.atual_hp > player.hp:
        player.atual_hp = player.hp
    print(f"{player.name} - HP: {player.atual_hp}, Mana: {player.atual_mana}")
    
    print("\nEnemies' status:")
    for enemy in enemies:
        print(f"{enemy.name} - HP: {enemy.atual_hp}, Mana: {enemy.atual_mana}")
    for enemy in enemies:
        enemy.check_effects()
        if enemy.atual_hp > 0:
            if player.atual_hp <= 0:
                break
            if enemy.abilities:
                ability = random.choice(enemy.abilities)
                possible_targets = [e for e in enemies if e.atual_hp > 0 and e != enemy]
                if possible_targets:
                    target = min(possible_targets, key=lambda e: e.atual_hp)
                else:
                    target = player
                damage, element = enemy.use_ability(ability.name)
                target.receive_damage(damage, element)

    if player.atual_hp <= 0:
        print("Game Over! You have been defeated.")
        break
    if all(enemy.atual_hp <= 0 for enemy in enemies):
        print("Victory! All enemies defeated.")
        break