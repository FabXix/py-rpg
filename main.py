import random

class Ability:
    def __init__(self, name, description, mana_cost, damage, element):
        self.name = name
        self.description = description
        self.mana_cost = mana_cost
        self.damage = damage
        self.element = element

Abilitys = [
    Ability("Fireball", "A fiery ball of destruction", 10, 20, "fire"),
    Ability("Ice Shard", "A sharp shard of ice", 8, 15, "ice"),
    Ability("Earthquake", "A tremor that shakes the ground", 12, 25, "earth"),
    Ability("Water Splash", "A splash of water that soaks the enemy", 5, 10, "water")
]

class Player:
    def __init__(self, name, is_bot=False):
        self.abilities = []
        self.name = name
        self.vit = 5
        self.int = 5
        self.dex = 5
        self.hp = 100 + self.vit * 10
        self.mana = 50 + self.int * 5
        self.atual_hp = self.hp
        self.atual_mana = self.mana
        self.ice_res = 0
        self.fire_res = 0
        self.water_res = 0
        self.earth_res = 0
        self.ice_dmg = 1
        self.fire_dmg = 1
        self.water_dmg = 1
        self.earth_dmg = 1
        self.mana_regen = 1
        self.hp_regen = 1
        self.is_bot = is_bot
    def recalculate_stats(self):
      self.hp = 100 + self.vit * 10
      self.mana = 50 + self.int * 5
      self.hp_regen = self.vit * 0.1
      self.mana_regen = self.int * 0.1
      self.atual_hp = self.hp
      self.atual_mana = self.mana
      self.ice_res = self.vit * 0.1
      self.fire_res = self.vit * 0.1
      self.water_res = self.vit * 0.1
      self.earth_res = self.vit * 0.1
      self.ice_dmg = 1 + (self.dex * 0.05)
      self.fire_dmg = 1 + (self.dex * 0.05)
      self.water_dmg = 1 + (self.dex * 0.05)
      self.earth_dmg = 1 + (self.dex * 0.05)
        
    def ability_selector(self, rounds):
        boost_dict = {
            "Vitality": "vit",
            "Intelligence": "int",
            "Dexterity": "dex"
        }
        if not self.is_bot:
            while rounds > 0:
                if rounds%2 == 0:
                    choices = random.sample(list(boost_dict.keys()), 2)
                    options = {choices[0]: random.randint(1, 10), choices[1]: random.randint(1, 10)}

                    print("Choose what to boost:")
                    for stat, value in options.items():
                        print(f"{stat}: +{value}")

                    choice = None
                    while choice not in options:
                        choice = input("Type your choice: ").strip().title()
                        if choice not in options:
                            print("Type the exact name of the option")

                    attr_name = boost_dict[choice]
                    setattr(self, attr_name, getattr(self, attr_name) + options[choice])

                    print(f"{choice} increased by {options[choice]}!")
                else:
                    choices = random.sample(Abilitys, 2)
                    print("Choose an ability to learn:")
                    for stat in choices:
                        print(f"{stat.name}: {stat.description} (Mana Cost: {stat.mana_cost}, Damage: {stat.damage}, Element: {stat.element})")
                    choice = None
                    ability_names = [a.name for a in choices]
                    while choice not in ability_names:
                        choice = input("Type the name of the ability you want to learn: ").strip()
                        if choice not in ability_names:
                            print("Type the exact name of the ability")
                    ability = next((a for a in Abilitys if a.name == choice), None)
                    if ability:
                        self.abilities.append(ability)
                        print(f"You learned {ability.name}!")
                    else:
                        print("Invalid ability choice.")
                rounds -= 1
            self.recalculate_stats()
            print(f"\nFinal stats:")
            print(f"Vit: {self.vit}, Int: {self.int}, Dex: {self.dex}")
            print(f"Hp: {self.hp}, Mana: {self.mana}")
            print(f"Abilities: {[ability.name for ability in self.abilities]}")
        else:
            for _ in range(rounds):
                if random.choice([True, False]):
                    attr_name = random.choice(list(boost_dict.values()))
                    boost_value = random.randint(1, 10)
                    setattr(self, attr_name, getattr(self, attr_name) + boost_value)
                    print(f"{self.name} boosted {attr_name} by {boost_value}!")
                else:
                    ability = random.choice(Abilitys)
                    self.abilities.append(ability)
                    print(f"{self.name} learned {ability.name}!")           
                    
    # I'll chane this so that the player can use also abilities that can heal or buff
    # but for now, it will only use abilities that deal damage
    def use_ability(self, ability_name):
        ability = next((a for a in self.abilities if a.name == ability_name), None)
        if ability and self.atual_mana >= ability.mana_cost:
            self.atual_mana -= ability.mana_cost
            print(f"{self.name} used {ability.name}!")
            if ability.element == "ice":
                ability.damage *= self.ice_dmg
            elif ability.element == "fire":
                ability.damage *= self.fire_dmg
            elif ability.element == "water":
                ability.damage *= self.water_dmg
            elif ability.element == "earth":
                ability.damage *= self.earth_dmg
            print(f"Damage: {ability.damage}, Element: {ability.element}")
            return ability.damage, ability.element
        else:
            print(f"{self.name} cannot use {ability_name}. Not enough mana or ability not found.")
            return 0, None
        
    def receive_damage(self, damage, element):
        if element == "ice":
            damage -= self.ice_res
        elif element == "fire":
            damage -= self.fire_res
        elif element == "water":
            damage -= self.water_res    
        elif element == "earth":
            damage -= self.earth_res
        if damage < 0:
            damage = 0
        self.atual_hp -= damage
        if self.atual_hp < 0:
            self.atual_hp = 0
        print(f"{self.name} received {damage} damage. Current HP: {self.atual_hp}")
        if self.atual_hp <= 0:
            print(f"{self.name} has been defeated!")



player_name = input("Enter your name: ")
player = Player(player_name, is_bot=False)

player.ability_selector(3)

num_enemies = int(input("How many enemies do you want to fight? "))
enemies = [Player(f"Enemy{i+1}", is_bot=True) for i in range(num_enemies)]
for enemy in enemies:
    enemy.ability_selector(3)
while player.atual_hp > 0 and any(enemy.atual_hp > 0 for enemy in enemies):
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