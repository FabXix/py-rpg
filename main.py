import random

class Player:
    def __init__(self, name, is_bot=False):
        self.abilities = []
        self.name = name
        self.vit = 5
        self.int = 5
        self.dex = 5
        self.hp = 100 + self.vit * 10
        self.mana = 50 + self.int * 5
        self.ice_res = 0
        self.fire_res = 0
        self.water_res = 0
        self.earth_res = 0
        self.ice_dmg = 1
        self.fire_dmg = 1
        self.water_dmg = 1
        self.earth_dmg = 1
        self.is_bot = is_bot
    def recalculate_stats(self):
      self.hp = 100 + self.vit * 10
      self.mana = 50 + self.int * 5
        
    def ability_selector(self, rounds):
        boost_dict = {
            "Vitality": "vit",
            "Intelligence": "int",
            "Dexterity": "dex"
        }

        while rounds > 0:
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
            rounds -= 1
        self.recalculate_stats()
        print(f"\nFinal stats:")
        print(f"Vit: {self.vit}, Int: {self.int}, Dex: {self.dex}")
        print(f"Hp: {self.hp}, Mana: {self.mana}")


player_name = input("Enter your name: ")
player = Player(player_name)
player.ability_selector(3)