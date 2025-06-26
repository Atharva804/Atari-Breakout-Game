import Constants
import pygame
from gameobject import GameObject

# Paddle class
class Paddle(GameObject):
    def __init__(self, x, color):
        super().__init__()
        self.width = Constants.PADDLE_WIDTH
        self.height = Constants.PADDLE_HEIGHT
        self.x = x
        self.y = Constants.HEIGHT - self.height
        self.dx = 0
        self.color = color
        self.lives = Constants.LIVES


    def move(self):
        self.x += self.dx
        if self.x < 0:
            self.x = 0
        if self.x > Constants.WIDTH - self.width:
            self.x = Constants.WIDTH - self.width


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


    def reset(self):
        self.x = (Constants.WIDTH - self.width) // 2
        self.y = Constants.HEIGHT - self.height
        self.dx = 0