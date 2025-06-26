import pygame
import pygame_gui
import Constants

#change
class GameInit:
    def __init__(self):
        self.SCREEN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.Manager = pygame_gui.UIManager((Constants.WIDTH, Constants.HEIGHT))
        self.Text_input_yes = None
        pygame.display.set_caption("Atari Breakout")
    


    def display_box(self,objectId,heading):
        # self.SCREEN.fill("white")
        img = pygame.image.load(Constants.BACK).convert()
        self.SCREEN.blit(img, (0, 0))
        Text_input_name = pygame_gui.elements.UITextEntryLine(relative_rect= pygame.Rect((120, 145), (400, 50)), manager=self.Manager, object_id= objectId)
        font = pygame.font.Font(Constants.FONT, 28)
        text_heading = font.render(heading, True, Constants.BLACK)
        text_position = text_heading.get_rect(center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 - 150))
        self.SCREEN.blit(text_heading, text_position)
        return Text_input_name

