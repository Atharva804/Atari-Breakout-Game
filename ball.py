import Constants
import random
import pygame
import Utils
from gameobject import GameObject

# Ball class
class Ball(GameObject):
    def __init__(self, paddle, color):
        super().__init__()
        self.paddle = paddle
        self.x = paddle.x + paddle.width // 2
        self.y = paddle.y - Constants.BALL_RADIUS - 1
        self.dx = 0
        self.dy = 0
        self.color = color
        self.impact_sound = pygame.mixer.Sound('sounds/impact.wav')
        self.impact_sound.set_volume(0.2)
    
    def launch(self):
        self.dx = random.choice([-2, 2])
        self.dy = -2


    def move(self):
        self.x += self.dx
        self.y += self.dy


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), Constants.BALL_RADIUS)


    def check_boundary_collision(self):
        if self.x <= Constants.BALL_RADIUS or self.x >= Constants.WIDTH - Constants.BALL_RADIUS:
            self.dx *= -1
        if self.y <= Constants.BALL_RADIUS:
            self.dy *= -1


    def check_paddle_collision(self, paddle):
        if self.y + Constants.BALL_RADIUS >= paddle.y and self.x >= paddle.x and self.x <= paddle.x + paddle.width:
            self.dy *= -1


    def check_brick_collision(self, brick):
        if not brick.destroyed:
            brick_rect = pygame.Rect(brick.x, brick.y, brick.width, brick.height)
            ball_rect = pygame.Rect(self.x - Constants.BALL_RADIUS, self.y - Constants.BALL_RADIUS, 2 * Constants.BALL_RADIUS, 2 * Constants.BALL_RADIUS)


            if brick_rect.colliderect(ball_rect):
                # Determine collision side
                if abs(brick_rect.top - ball_rect.bottom) < Constants.BALL_RADIUS and self.dy > 0:
                    # Ball hits bottom of the brick
                    self.dy *= -1
                elif abs(brick_rect.bottom - ball_rect.top) < Constants.BALL_RADIUS and self.dy < 0:
                    # Ball hits top of the brick
                    self.dy *= -1
                elif abs(brick_rect.left - ball_rect.right) < Constants.BALL_RADIUS and self.dx > 0:
                    # Ball hits right side of the brick
                    self.dx *= -1
                elif abs(brick_rect.right - ball_rect.left) < Constants.BALL_RADIUS and self.dx < 0:
                    # Ball hits left side of the brick
                    self.dx *= -1


                # Reduce hit points or destroy the brick
                if brick.hit_points > 1:
                    brick.hit_points -= 1
                    brick.color = Utils.get_color(brick.hit_points)
                else:
                    brick.destroyed = True
                    self.impact_sound.play()
        return brick.destroyed