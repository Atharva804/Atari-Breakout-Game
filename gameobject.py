#Parent class for all the objects used in the game
'''By creating a common base class with generic methods like draw and move, you allow for a consistent
 interface across different types of game objects. Subclasses (specific types of game objects) can then 
 provide their own implementations for these methods, tailoring the behavior to the needs of that specific game object.'''

class GameObject:
    def draw():
        pass

    def move():
        pass