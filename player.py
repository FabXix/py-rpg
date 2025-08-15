import random

from skills import Skills
boost_dict = {
            "Vitality": "vit",
            "Intelligence": "int",
            "Dexterity": "dex",
            "Luck": "luck",
            }

class Player:
    def __init__(self, name, is_bot=False):
        self.abilities = []
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.name = name
        self.vit = 5
        self.int = 5
        self.dex = 5
        self.luck = 0.1
        self.hp = 100 + self.vit * 10
        self.mana = 50 + self.int * 5
        self.actual_hp = self.hp
        self.actual_mana = self.mana
        self.ice_res = 0
        self.fire_res = 0
        self.water_res = 0
        self.earth_res = 0
        self.ice_dmg = 1
        self.fire_dmg = 1
        self.water_dmg = 1
        self.earth_dmg = 1
        self.hp_regen = self.vit * 0.5
        self.mana_regen = self.int * 0.5
        self.is_bot = is_bot
        self.active_effects = {"heal": (0,0), "poison": (0 , 0)} # heal: (dmg, turns), poison: (dmg, turns)
        self.inmunities = {"fire": 0, "ice": 0, "water": 0, "earth": 0}
    def recalculate_stats(self):
      self.hp = 100 + self.vit * 10
      self.mana = 50 + self.int * 5
      self.hp_regen = self.vit *0.5
      self.mana_regen = self.int * 0.5
      self.ice_res = self.vit * 0.1
      self.fire_res = self.vit * 0.1
      self.water_res = self.vit * 0.1
      self.earth_res = self.vit * 0.1
      self.ice_dmg = 1 + (self.dex * 0.05)
      self.fire_dmg = 1 + (self.dex * 0.05)
      self.water_dmg = 1 + (self.dex * 0.05)
      self.earth_dmg = 1 + (self.dex * 0.05)
        
    def ability_selector(self, rounds):
        if not self.is_bot:
            while rounds > 0:
                if rounds%2 == 0:
                    self.select_boost()
                else:
                    choices = random.sample(Skills, 3)
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
            self.print_stats()
        else:
            while rounds > 0:
                if rounds % 2 == 0:
                    self.select_boost()
                else:
                    ability = random.choice(Skills)
                    self.abilities.append(ability)
                    print(f"{self.name} learned {ability.name}!")
                rounds -= 1


    def use_ability(self, ability_name, double_hit=False ,target=None):
        ability = next((a for a in self.abilities if a.name == ability_name), None)
        
        if not ability or (self.actual_mana < ability.mana_cost and double_hit == False):
            print(f"{self.name} cannot use {ability_name}. Not enough mana or ability not found.")
            return
        if double_hit == False:
            self.actual_mana -= ability.mana_cost
        print(f"{self.name} used {ability.name}!")

        if ability.type == "damage" and target:
            base_damage = ability.damage
            if ability.element == "ice":
                base_damage *= self.ice_dmg
            elif ability.element == "fire":
                base_damage *= self.fire_dmg
            elif ability.element == "water":
                base_damage *= self.water_dmg
            elif ability.element == "earth":
                base_damage *= self.earth_dmg
            target.receive_damage(base_damage, ability.element, self)

        elif ability.type == "heal":
            heal_amount = ability.damage
            self.actual_hp += heal_amount
            if self.actual_hp > self.hp:
                self.actual_hp = self.hp
            print(f"{self.name} healed for {heal_amount} HP. Current HP: {self.actual_hp}")

        elif ability.type == "buff":
            if ability.element == "shield":
                self.earth_res += ability.damage
                self.fire_res += ability.damage
                self.water_res += ability.damage
                self.ice_res += ability.damage  
                print(f"{self.name} gained a shield of {ability.damage} to all resistances.")
            elif ability.element == "mana":
                self.actual_mana += ability.damage
                if self.actual_mana > self.mana:
                    self.actual_mana = self.mana
                print(f"{self.name} recovered {ability.damage} mana. Current mana: {self.actual_mana}")

        elif ability.type == "effect":
            if ability.element == "poison" and target:
                poison_damage = ability.damage
                target.active_effects["poison"] = (poison_damage, 3)
                print(f"{self.name} poisoned {target.name} for {poison_damage} over 3 turns.")
            elif ability.element == "heal":
                hot_amount = ability.damage
                self.active_effects["heal"] = (hot_amount, 3)
                print(f"{self.name} will heal {hot_amount} over 3 turns.")

        else:
            print(f"{self.name} used {ability.name}, but nothing happened.")
    
    def check_effects(self):
        if "heal" in self.active_effects and self.active_effects["heal"][1] > 0 and self.actual_hp < self.hp:
            heal_amount, turns = self.active_effects["heal"]
            self.actual_hp += heal_amount
            if self.actual_hp > self.hp:
                self.actual_hp = self.hp
            self.active_effects["heal"] = (heal_amount, turns - 1)
            print(f"{self.name} healed for {heal_amount} HP. Current HP: {self.actual_hp}")
        if "poison" in self.active_effects and self.active_effects["poison"][1] > 0:
            poison_damage, turns = self.active_effects["poison"]
            self.actual_hp -= poison_damage
            if self.actual_hp < 0:
                self.actual_hp = 0
            self.active_effects["poison"] = (poison_damage, turns - 1)
            print(f"{self.name} took {poison_damage} poison damage. Current HP: {self.actual_hp}")

    def receive_damage(self, damage, element, damager):
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
        self.actual_hp -= damage
        if self.actual_hp < 0:
            self.actual_hp = 0
        print(f"{self.name} received {damage} {element} damage. Current HP: {self.actual_hp}")
        if damager:
            damager.xp += int(damage) 
            damager.check_hit_luck(damage)

        
        if self.actual_hp <= 0:
            if damager:
                print(f"{self.name} has been defeated by {damager.name}!")
                self.give_random_skill(damager, 3)
            else:
                print(f"{self.name} has been defeated!!")
        return damage

    def check_level_up(self):
        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.xp = 0
        self.xp_to_next_level = int(self.xp_to_next_level * 1.1)
        self.vit += 5
        self.int += 5
        self.dex += 5
        self.luck += 0.5
        self.level += 1
        print(f"{self.name} leveled up! Now at level {self.level}.")
        self.recalculate_stats()
        
    def select_boost(self, is_bot=False):
        if is_bot or self.is_bot:
            attr_name = random.choice(list(boost_dict.values()))
            boost_value = random.randint(0+self.level, 9+self.level)
            setattr(self, attr_name, getattr(self, attr_name) + boost_value)
            if attr_name == "luck":
                boost_value = round(boost_value * 0.1, 2)
            print(f"{self.name} boosted {attr_name} by {boost_value}!")
        else:
            choices = random.sample(list(boost_dict.keys()), 2)
            options = {choices[0]: random.randint(1, 10), choices[1]: random.randint(1, 10)}
            for key in options:
                if key == "Luck":
                    options[key] = round(options[key] * 0.1, 2)       
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
        self.recalculate_stats()

    def remove_ability(self, ability_name):
        ability = next((a for a in self.abilities if a.name == ability_name), None)
        if ability:
            self.abilities.remove(ability)
            print(f"{self.name} removed {ability_name} from abilities.")
        else:
            print(f"{self.name} does not have {ability_name} in abilities.")
    
    def give_random_skill(self, damager, num_skills):
        for _ in range(num_skills):
            ability = random.choice(Skills)
            damager.abilities.append(ability)
            print(f"{damager.name} learned {ability.name}!")  
    
    def check_hit_luck(self, total_damage):
        hits = int(total_damage // 10)
        for _ in range(hits):
            if random.random() < self.luck:
                self.give_random_skill(self, 1)

    def check_double_hit(self,  ability):
        if self.mana < ability.mana_cost:
            return 0 
        hits = int(ability.damage // 10)
        landed = 1
        for _ in range(hits):
            if random.random() < self.dex * 0.1:
                landed += 1
        return landed
                
    
    def print_stats(self):
        print(f"\n{self.name} stats:")
        print(f"Vit: {self.vit}, Int: {self.int}, Dex: {self.dex}, Luck: {self.luck}")
        print(f"Hp: {self.hp}, Mana: {self.mana}")
        print(f"Abilities: {[ability.name for ability in self.abilities]}")
    
