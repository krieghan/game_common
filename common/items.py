from BaseGameEntity import Item

class Clothing(Item):
    def __init__(self, name, value=0, weight=5, appearance=0, warmth=0, defense=0, durability=25, quantity=1, onEquip=None, onDeequip=None, manager=None, world=None):
        Item.__init__(self, name, value, weight, manager, durability, world=world)
        
        self.attributes['appearance'] = appearance
        self.attributes['warmth'] = warmth
        self.attributes['defense'] = defense

class Food(Item):
    def __init__(self, name, value=0, weight=5, satisfaction=1, taste=1, quantity=1, onEat=None, world=None, manager=None, durability=25):
        Item.__init__(self, name, value, weight, world=world, manager=manager, durability=durability)
        self.attributes['satisfaction'] = satisfaction
        self.attributes['taste'] = taste
        self.onEat = onEat

class Weapon(Item):
    def __init__(self, name, value=0, weight=5, damage=1, quantity=1, onHit=None, onEquip=None, onDeequip=None, world=None, manager=None, durability=25):
        Item.__init__(self, name, value, weight, world=world, manager=manager, durability=durability)
        self.attributes['damage'] = damage
        self.onHit=onHit
        self.onEquip=onEquip
        self.onDeequip=onDeequip
