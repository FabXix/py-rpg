import random

from skills import Skills


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
        self.active_effects = {"heal": (0,0), "poison": (0 , 0)} # heal: (dmg, turns), poison: (dmg, turns)
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
                    choices = random.sample(Skills, 2)
                    print("Choose an ability to learn:")
                    for stat in choices:
                        print(f"{stat.name}: {stat.description} (Mana Cost: {stat.mana_cost}, Damage: {stat.damage}, Element: {stat.element})")
                    choice = None
                    ability_names = [a.name for a in choices]
                    while choice not in ability_names:
                        choice = input("Type the name of the ability you want to learn: ").strip()
                        if choice not in ability_names:
                            print("Type the exact name of the ability")
                    ability = next((a for a in Skills if a.name == choice), None)
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
                    ability = random.choice(Skills)
                    self.abilities.append(ability)
                    print(f"{self.name} learned {ability.name}!")           

    # I'll change this so that the player can use also abilities that can heal or buff
    # but for now, it will only use abilities that deal damage
    def use_ability(self, ability_name):
        ability = next((a for a in self.abilities if a.name == ability_name), None)
        if ability and self.atual_mana >= ability.mana_cost and ability.type == "damage":
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
        elif ability and self.atual_mana >= ability.mana_cost and ability.type == "heal":
            self.atual_mana -= ability.mana_cost
            heal_amount = ability.damage    # Assuming damage is used for healing amount
            self.atual_hp += heal_amount
            if self.atual_hp > self.hp:
                self.atual_hp = self.hp
            print(f"{self.name} used {ability.name} and healed {heal_amount} HP!")
            return 0, None  
        elif ability and self.atual_mana >= ability.mana_cost and ability.type == "buff":
            self.atual_mana -= ability.mana_cost
            if ability.element == "shield":
                self.earth_res += ability.damage
                self.fire_res += ability.damage
                self.water_res += ability.damage
                self.ice_res += ability.damage  
                print(f"{self.name} used {ability.name} and gained a shield of {ability.damage}!")
            elif ability.element == "mana":
                self.atual_mana += ability.damage
                if self.atual_mana > self.mana:
                    self.atual_mana = self.mana
            print(f"{self.name} used {ability.name} and gained {ability.damage} mana!")
            return 0, None
        elif ability and self.atual_mana >= ability.mana_cost and ability.type == "effect":
            if ability.element == "poison":
                poison_damage = ability.damage
                self.active_effects["poison"] = (poison_damage, 3)
                self.atual_mana -= ability.mana_cost
                print(f"{self.name} used {ability.name} and poisoned the enemy for {poison_damage} damage over 3 turns!")
                return "poison", poison_damage
    
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
    def check_effects(self):
        if "heal" in self.active_effects and self.active_effects["heal"][1] > 0:
            heal_amount, turns = self.active_effects["heal"]
            self.atual_hp += heal_amount
            if self.atual_hp > self.hp:
                self.atual_hp = self.hp
            self.active_effects["heal"] = (heal_amount, turns - 1)
            print(f"{self.name} healed for {heal_amount} HP. Current HP: {self.atual_hp}")
        if "poison" in self.active_effects and self.active_effects["poison"][1] > 0:
            poison_damage, turns = self.active_effects["poison"]
            self.atual_hp -= poison_damage
            if self.atual_hp < 0:
                self.atual_hp = 0
            self.active_effects["poison"] = (poison_damage, turns - 1)
            print(f"{self.name} took {poison_damage} poison damage. Current HP: {self.atual_hp}")

