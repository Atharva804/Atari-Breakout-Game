import Constants
import pygame
from gameobject import GameObject


# Brick class
class Brick(GameObject):
    def __init__(self, x, y, hit_points, color):
        super().__init__()
        self.width = Constants.BRICK_WIDTH
        self.height = Constants.BRICK_HEIGHT
        self.x = x
        self.y = y
        self.hit_points = hit_points
        self.color = color
        self.destroyed = False
        self.powerUpStatus = False


    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
