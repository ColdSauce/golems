class MovableCharacter:
    def move(self,speed = 2):
        direction = self.current_direction
        if direction == Direction.UP:
            self.y -= speed
        elif direction == Direction.RIGHT:
            self.x += speed
        elif direction == Direction.DOWN:
            self.y += speed
        elif direction == Direction.LEFT:
            self.x -= speed


    def change_direction(self, direction, override_opt = False):
        # Optimization
        if not override_opt and self.current_direction == direction:
            return
        self.current_direction = direction
        name = self.directional_sprites[direction]
        self.sprite = self.load_function(name)

    def __init__(self, name, load_function, directional_sprites,x=200,y=400, gold=0):
        self.moving = False
        self.load_function = load_function
        self.directional_sprites = directional_sprites
        self.x = x
        self.y = y
        self.name = name
        self.gold = gold
        self.current_direction = Direction.UP
        
class MainPlayer(MovableCharacter):
    pass

class EnemyPlayer(MovableCharacter):
    pass

class Direction:
    UP    = 0
    RIGHT = 1
    DOWN  = 2
    LEFT  = 3

class Element:
    NEUTRAL = 0
    FIRE    = 1
    NATURE  = 2
    WATER   = 3

class GenericBot:
    def __init__(self, name, image, speed=0, health=100,mana=100,element=Element.FIRE,spell_xp=dict(),list_of_spells=[]):
        self.name = name
        self.sprite = sprite 
        self.speed = speed
        self.health = health
        self.mana = mana
        self.element = element
        self.spell_xp = spell_xp
        self.list_of_spells = list_of_spells

class Spells:
    def __init__(self, name, mana_cost=25, attack_power=5,multiplier=dict(),accuracy=0.5):
        self.name = name
        self.mana_cost = mana_cost
        self.attack_power = attack_power
        self.multiplier = multiplier
        self.accuracy = accuracy
