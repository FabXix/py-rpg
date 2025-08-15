class Skill:
    def __init__(self, name, description, mana_cost, damage, element,type="damage"):
        self.name = name
        self.type = type
        self.description = description
        self.mana_cost = mana_cost
        self.damage = damage
        self.element = element
        
Skills = [
    Skill("Fireball", "A fiery ball of destruction", 10, 20, "fire", "damage"),
    Skill("Ice Shard", "A sharp shard of ice", 8, 15, "ice", "damage"),
    Skill("Earthquake", "A tremor that shakes the ground", 12, 25, "earth","damage"),
    Skill("Water Splash", "A splash of water that soaks the enemy", 5, 10, "water","damage"),
    Skill ("Healing Light", "A warm light that heals wounds", 15, 20, "light", "heal"),
    Skill ("Mana Boost", "A surge of mana that replenishes energy", 0, 20, "mana", "mana"),
    Skill("Poison Cloud", "A toxic cloud that poisons enemies", 15, 10, "poison", "effect"),
    Skill("Healing Clockwork", "A mechanical device that heals over time", 20, 5, "heal", "effect"),
    Skill("Event Trigger", "Triggers a random event", 0, 0, "event", "event"),
]
