import pygame
import pyganim as pyanim
import pygame_gui
import Constants
import Utils
import sys

from gameinit import GameInit
from brickclass import Brick
from customlevel import CustomLevel
from paddle import Paddle
from ball import Ball
from powerupbrick import PowerupBrick

#  BreakoutGame class with end menu functionality
class BreakoutGame:
    def __init__(self, current_user):
        pygame.init()
        gameInit = GameInit()
        self.screen = gameInit.SCREEN
        self.clock = gameInit.CLOCK
        self.player_mode = None
        self.paddle1 = None
        self.paddle2 = None
        self.ball1 = None
        self.ball2 = None
        self.cpu_speed = 6
        self.current_time = None
        self.elapsed_time = 0
        self.start_time = 0
        self.elapsed_time_two = 0
        self.start_time_two = 0
        # sounds
        self.fail_sound = pygame.mixer.Sound(Constants.FAIL)
        self.fail_sound.set_volume(0.2)
        self.music = pygame.mixer.Sound(Constants.MUSIC)
        self.music.set_volume(0.08)
        self.powerup_sound = pygame.mixer.Sound(Constants.POWERUP)
        self.powerup_sound.set_volume(0.2)
        self.music.play(loops = -1)

        self.paddle2_centery = Constants.WIDTH/2
        self.player_one = current_user
        self.player_one.player_id=1
        self.player_two = None
        self.bricks_broken_p1 = 0
        self.bricks_broken_p2 = 0
        self.powerups_p1 = 0
        self.powerups_p2 = 0
        self.levels = [
            {
                'bricks': [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ],
            },
            {
                'bricks': [
                    [1, 1, 1, 2, 2, 2, 2, 1, 1, 1],
                    [2, 1, 1, 2, 1, 1, 2, 2, 1, 2]
                ],
            },
            {
                'bricks': [
                    [2, 3, 2, 3, 2, 3, 2, 3, 2, 3],
                    [3, 4, 3, 4, 3, 4, 3, 4, 3, 4],
                    [4, 5, 4, 5, 4, 5, 4, 5, 4, 5],
                    [5, 1, 5, 1, 5, 1, 5, 1, 5, 1],
                    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
                ],
            }
            #  Add more levels as needed
        ]
        self.current_level = 0
        self.game_over = False
        self.bricks = []
        self.create_bricks()
        self.show_end_menu = False


        #  Load the heart image with a desired width and height
        HEART_WIDTH = 20  #  Adjust the width as needed
        HEART_HEIGHT = 20  #  Adjust the height as needed
        self.heart_image = pygame.image.load(Constants.HEART)
        self.heart_image = pygame.transform.scale(self.heart_image, (HEART_WIDTH, HEART_HEIGHT))
        self.heart_rect = self.heart_image.get_rect()

    # function to create normal or powerup bricks
    def create_bricks(self):
        bricks_config = self.levels[self.current_level]['bricks']
        powerup_brick_list = self.number_of_powerbricks()
        for row in range(len(bricks_config)):
            for col in range(Constants.BRICK_COLS):
                brick_x = col * (Constants.BRICK_WIDTH + Constants.BRICK_GAP)
                brick_y = Constants.TOP_GAP + row * (Constants.BRICK_HEIGHT + Constants.BRICK_GAP)
                hit_points = bricks_config[row][col]
                if hit_points != 0:
                    color = Utils.get_color(hit_points)
                    if ((row,col) in powerup_brick_list):
                        powerBrick =PowerupBrick(Brick(brick_x, brick_y, hit_points, color))
                        powerBrick.powerUpStatus = True 
                        self.bricks.append(powerBrick)
                    else:
                        self.bricks.append(Brick(brick_x, brick_y, hit_points, color))

    #function to randomly choose and create a list of positions from list of bricks
    def number_of_powerbricks(self):
        bricks_config = self.levels[self.current_level]['bricks']
        rowLength = len(bricks_config)
        ColLength = Constants.BRICK_COLS
        total_bricks = rowLength*ColLength
        powerBricks_number = Utils.choose_random(total_bricks)
        result = []
        for i in range(powerBricks_number):
            rowRandom = Utils.choose_random(rowLength)
            columnRandom = Utils.choose_random(ColLength)
            position = (rowRandom,columnRandom)
            result.append(position)
        return result

    # handle actions when a key pressed
    def handle_events(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                Utils.update_user_stats(self.current_time,self.bricks_broken_p1,self.powerups_p1,self.player_one.username)
                if self.player_mode == "two":
                    Utils.update_user_stats(self.current_time,self.bricks_broken_p2,self.powerups_p2, self.player_two.username)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_over = True
                if self.player_mode is None:
                    if event.key == pygame.K_1:
                        self.player_mode = "single"
                        self.initialize_game()
                    elif event.key == pygame.K_2:
                        self.player_mode = "two"
                        self.initialize_game()
                    elif event.key == pygame.K_3:
                        self.player_mode = "three"
                        self.initialize_game()
                    elif event.key == pygame.K_4:
                        self.player_mode = "four"
                        self.initialize_game()
                    elif event.key == pygame.K_5:
                        self.player_mode = "five"
                        self.initialize_game()
                    elif event.key == pygame.K_6:
                        self.player_mode = "six"
                        self.initialize_game()
                    elif event.key == pygame.K_7:
                        self.player_mode = "seven"
                        self.initialize_game()
                    elif event.key == pygame.K_8:
                        self.player_mode = "eight"
                        self.initialize_game()
                elif self.player_mode == "single":
                    if event.key == pygame.K_LEFT:
                        self.paddle1.dx = -5
                    elif event.key == pygame.K_RIGHT:
                        self.paddle1.dx = 5
                    elif event.key == pygame.K_SPACE:
                        if self.ball1.dy == 0:
                            self.ball1.launch()
                elif self.player_mode == "two":
                    if event.key == pygame.K_LEFT:
                        self.paddle1.dx = -5
                    elif event.key == pygame.K_RIGHT:
                        self.paddle1.dx = 5
                    elif event.key == pygame.K_a:
                        self.paddle2.dx = -5
                    elif event.key == pygame.K_d:
                        self.paddle2.dx = 5
                    elif event.key == pygame.K_SPACE:
                        if self.ball1.dy == 0 and self.ball2.dy == 0:
                            self.ball1.launch()
                            self.ball2.launch()
                elif self.player_mode == "three":
                    if event.key == pygame.K_LEFT:
                        self.paddle1.dx = -5
                    elif event.key == pygame.K_RIGHT:
                        self.paddle1.dx = 5
                    elif event.key == pygame.K_SPACE:
                        if self.ball1.dy == 0 and self.ball2.dy == 0:
                            self.ball1.launch()
                            self.ball2.launch()                            
            elif event.type == pygame.KEYUP:
                if self.player_mode == "single":
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.paddle1.dx = 0
                elif self.player_mode == "two":
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.paddle1.dx = 0
                    elif event.key == pygame.K_a or event.key == pygame.K_d:
                        self.paddle2.dx = 0
                elif self.player_mode == "three":
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.paddle1.dx = 0
                    #  if self.paddle2.dx > self.ball2.dx or self.paddle2.dx < self.ball2.dx:
                    #      self.paddle2.dx = 0

    # Function to move paddle 2 with AI
    def animate_cpu(self):
        if self.player_mode == "three":  # "Two Players with AI"
            ball = self.ball2

            # Calculate the future position of the ball
            ball_future_x = self.predict_ball_future_x(ball)
            
            # Find the center of the paddle
            paddle_center_x = self.paddle2.x + self.paddle2.width / 2
            
            # Calculate the distance between the future ball position and the paddle center
            error_distance = ball_future_x - paddle_center_x
            
            # Apply a proportional control to determine the movement speed
            # The constant factor (e.g., 0.1) can be adjusted for smoother or faster response
            self.cpu_speed = error_distance * 0.1
            
            # Clamp the speed to avoid too fast movement
            max_speed = 4  # Max speed limit
            self.cpu_speed = max(min(self.cpu_speed, max_speed), -max_speed)
            
            # Update paddle position
            self.paddle2.x += self.cpu_speed
            self.paddle2.x = max(min(self.paddle2.x, Constants.WIDTH - self.paddle2.width), 0)


    def predict_ball_future_x(self, ball):
        # Physics prediction logic as before
        steps = (self.paddle2.y - ball.y) / ball.dy if ball.dy != 0 else 0
        future_x = ball.x + steps * ball.dx #Predicts the balls horizontal position - multiplies the number of steps by balls horizontral speed and adds this to the balls current x coordinate 
        #Assumption: Ball moves at constant horizontal speed and directly towards paddle without interferance 

        # Account for wall bounces
        """
        This loop adjusts the predicted future_x position if the calculation indicates the ball would "move" beyond the game area's 
        horizontal bounds (less than 0 or greater than Constants.WIDTH), simulating a bounce off the side walls.
        If future_x is less than 0 (indicating the ball has "moved" past the left boundary), 
        it negates future_x to simulate a bounce off the left wall.
        If future_x is greater than Constants.WIDTH (indicating the ball has "moved" past the right boundary),
         it calculates 2 * Constants.WIDTH- future_x to simulate a bounce off the right wall.
        This loop repeats until future_x is within the legal game area bounds, effectively simulating multiple wall bounces if necessary.

        """
        while future_x < 0 or future_x > Constants.WIDTH:
            if future_x < 0:
                future_x = -future_x
            elif future_x > Constants.WIDTH:
                future_x = 2 * Constants.WIDTH - future_x

        return future_x

            
    def initialize_game(self):
        try:
            Utils.reset_score(self.player_one.username)
            self.paddle1 = Paddle(Constants.WIDTH // 4, Constants.WHITE)
            self.ball1 = Ball(self.paddle1, Constants.WHITE)
            if self.player_mode == "two":
                self.player_two = Utils.enter_user()
                #change
                if self.player_two:
                    self.player_two.player_id=2
                    pygame.init()
                    gameInit = GameInit()
                    self.screen = gameInit.SCREEN
                    self.clock = gameInit.CLOCK
                    self.music.play(loops = -1)        
                    Utils.reset_score(self.player_two.username)
                    self.paddle2 = Paddle(3 * Constants.WIDTH // 4 - Constants.PADDLE_WIDTH, Constants.RED)
                    self.ball2 = Ball(self.paddle2, Constants.RED)
                else:
                    print("Player 2 login failed. Please try again")
            if self.player_mode == "three":
                self.paddle2 = Paddle(3 * Constants.WIDTH // 4 - Constants.PADDLE_WIDTH, Constants.RED)
                self.ball2 = Ball(self.paddle2, Constants.RED)
            elif self.player_mode == "four":
                self.draw()
            elif self.player_mode == "five":
                self.draw()
            elif self.player_mode == "six":
                self.draw()
                customLevel = CustomLevel()
                new_level_dict = customLevel.create_custom_level()
                self.levels.append(new_level_dict)
            elif self.player_mode == "seven":
                Utils.update_user_stats(self.current_time,self.bricks_broken_p1,self.powerups_p1,self.player_one.username)
                if self.player_mode == "two":
                    Utils.update_user_stats(self.current_time,self.bricks_broken_p2,self.powerups_p2,self.player_two.username)
                pygame.quit()
                exit()
            elif self.player_mode == "eight":
                self.draw()
            self.bricks = []
            self.create_bricks()
        except Exception as e:
            print(f"An exception occurred in initialize_game method: {e}")



    #function to update the state once a move is made
    def update(self):
        if not self.game_over:
            self.paddle1.move()
            if self.ball1.dy == 0:
                self.ball1.x = self.paddle1.x + self.paddle1.width // 2
            self.ball1.move()
            self.ball1.check_boundary_collision()
            self.ball1.check_paddle_collision(self.paddle1)
            for brick in self.bricks:
                result = self.ball1.check_brick_collision(brick)
                if (result == True):
                    self.bricks_broken_p1 += 1
                    if isinstance(brick, PowerupBrick):
                            self.powerups_p1 += 1
                            res_img = brick.activate_powerup(breakout = self, userobj = self.player_one)
                            animObj = pyanim.PygAnimation([(res_img, 3000)])
                            animObj.play()
                            animObj.blit(self.screen, (280, 200))
                            if res_img == Constants.PADDLEPU:
                                self.start_time = pygame.time.get_ticks()
                                self.elapsed_time = 0
                            pygame.display.update()
                            pygame.time.delay(1000)
                            self.powerup_sound.play()
                    else:
                        Utils.update_score(self.player_one.username, brick.hit_points)

            self.bricks = [brick for brick in self.bricks if not brick.destroyed]
            if self.player_mode == "two": # If gamemode is selected as number 2
                self.paddle2.move()
                if self.ball2.dy == 0:
                    self.ball2.x = self.paddle2.x + self.paddle2.width // 2
                self.ball2.move()
                self.ball2.check_boundary_collision()
                self.ball2.check_paddle_collision(self.paddle2)
                for brick in self.bricks:
                    resultp2 = self.ball2.check_brick_collision(brick)
                    if (resultp2 == True):
                        self.bricks_broken_p2 +=1
                        if isinstance(brick, PowerupBrick):
                                self.powerups_p2 += 1
                                res_img_two = brick.activate_powerup(breakout = self, userobj = self.player_two)
                                animObj = pyanim.PygAnimation([(res_img_two, 3000)])
                                animObj.play()
                                animObj.blit(self.screen, (230, 130))
                                if res_img_two == Constants.PADDLEPU:
                                    self.start_time_two = pygame.time.get_ticks()
                                    self.elapsed_time_tstart_time_two = 0
                                pygame.display.update()
                                pygame.time.delay(1000)
                                self.powerup_sound.play()
                        else:
                            Utils.update_score(self.player_two.username, brick.hit_points)
                self.bricks = [brick for brick in self.bricks if not brick.destroyed]

            if self.player_mode == "three": # If gamemode is selected as number 3
                self.paddle2.move()
                if self.ball2.dy == 0:
                    self.ball2.x = self.paddle2.x + self.paddle2.width // 2
                self.ball2.move()
                self.ball2.check_boundary_collision()
                self.ball2.check_paddle_collision(self.paddle2)
                for brick in self.bricks:
                    self.ball2.check_brick_collision(brick)
                self.bricks = [brick for brick in self.bricks if not brick.destroyed]


            #  Check if all bricks are destroyed
            if not self.bricks:
                self.next_level()


            #  Update player lives when balls go out
            if self.ball1.y > Constants.HEIGHT:
                if self.player_mode == "single":
                    self.ball1_reset()
                    self.fail_sound.play()
                    self.paddle1.lives -= 1
                    if self.paddle1.lives == 0:
                        self.game_over = True
                elif self.player_mode == "two":
                    self.ball1_reset()
                    self.fail_sound.play()
                    self.paddle1.lives -= 1
                elif self.player_mode == "three":
                    self.ball1_reset()
                    self.paddle1.lives -= 1
                    self.ball2_reset()
                    self.fail_sound.play()
                    self.paddle2.lives -= 1


            if self.player_mode == "two" and self.ball2.y > Constants.HEIGHT:
                self.ball2_reset()
                self.paddle2.lives -= 1

            #  Check if both players have run out of lives
            if self.paddle1.lives <= 0 and (self.player_mode != "two" or self.paddle2.lives <= 0):
                self.game_over = True


            #  Check if the current level is greater than or equal to the number of levels
            if self.current_level >= len(self.levels):
                self.game_over = True     
        

    def ball1_reset(self):
        self.ball1.__init__(self.paddle1, Constants.WHITE)
        #  [Method code remains unchanged]


    def ball2_reset(self):
        self.ball2.__init__(self.paddle2, Constants.RED)
        #  [Method code remains unchanged]

    # function to display text on screen
    def draw(self):
        tFont = pygame.font.Font(Constants.FONT, 52)
        img = pygame.image.load(Constants.BACK).convert()
        self.screen.blit(img, (0, 0))
        if self.player_mode == "single":
            self.paddle1.draw(self.screen)
            self.ball1.draw(self.screen)
        if self.player_mode == "two":
            self.paddle1.draw(self.screen)
            self.ball1.draw(self.screen)
            self.paddle2.draw(self.screen)
            self.ball2.draw(self.screen)
        elif self.player_mode == "three":
            self.paddle1.draw(self.screen)
            self.ball1.draw(self.screen)
            self.paddle2.draw(self.screen)
            self.ball2.draw(self.screen)
        elif self.player_mode == "four":
            text_best_score = tFont.render("Best Score: " + str(Utils.get_best_score(self.player_one.username)), True, Constants.WHITE)
            self.screen.blit(text_best_score, (Constants.HEIGHT // 2 - 100, Constants.WIDTH // 2 - 100))
        elif self.player_mode == "five":
            text_leadH = tFont.render("Leaderboard", True, Constants.WHITE)            
            text_lead = Utils.get_leaderboard()
            self.screen.blit(text_leadH, (Constants.WIDTH // 2 - 125, Constants.HEIGHT // 2 - 225))
            y = 100
            for rank, (player, score) in enumerate(text_lead, start=1):
                text = tFont.render(f'{rank}. {player}: {score}', True, Constants.WHITE)
                self.screen.blit(text, (Constants.WIDTH // 2 - text.get_width() // 2, y))
                y += 60
        elif self.player_mode == "eight":
            text_statsH = tFont.render("User Stats", True, Constants.WHITE)            
            stats = Utils.get_user_statistics(self.player_one.username) 
            self.screen.blit(text_statsH, (Constants.WIDTH // 2 - 125, Constants.HEIGHT // 2 - 225))
            time = stats[0]
            bricks_broken = stats[1]
            powerup_collected = stats[2]
            text_time = tFont.render(f'Total Time: {time} mins', True, Constants.WHITE)
            text_bricks = tFont.render(f'Bricks Broken: {bricks_broken}', True, Constants.WHITE)
            text_power = tFont.render(f'Power Up Collected: {powerup_collected}', True, Constants.WHITE)
            self.screen.blit(text_time, (Constants.WIDTH // 2 - text_time.get_width() // 2, 100))
            self.screen.blit(text_bricks, (Constants.WIDTH // 2 - text_bricks.get_width() // 2, 170))
            self.screen.blit(text_power, (Constants.WIDTH // 2 - text_power.get_width() // 2, 240))
        elif self.player_mode == "six":
            text_custom = tFont.render("Enter Config in Console", True, Constants.WHITE)
            self.screen.blit(text_custom, (100, Constants.HEIGHT // 2 - 225))
        for brick in self.bricks:
            brick.draw(self.screen)
        if self.player_mode is None:
            self.draw_menu()
        elif self.player_mode == "single" or self.player_mode == "three":
            font = pygame.font.Font(Constants.FONT, 28)
            text_level = font.render("Level: " + str(self.current_level + 1), True, Constants.WHITE)
            text_score = font.render("Score: " + str(Utils.get_score(self.player_one.username)), True, Constants.WHITE)
            text_bestScore = font.render("Best Score: " + str(Utils.get_best_score(self.player_one.username)), True, Constants.WHITE)

            for i in range(self.paddle1.lives):
                x = 10 + i * (self.heart_rect.width + 5)
                y = 5
                self.screen.blit(self.heart_image, (x, y))

            if self.player_mode == "three":
                #  Display player 3's lives as heart images
                for i in range(self.paddle2.lives):
                    x = 10 + i * (self.heart_rect.width + 5)
                    y = 30
                    self.screen.blit(self.heart_image, (x, y))

            self.screen.blit(text_level, (10, 45))
            self.screen.blit(text_score, (500, 10))
            self.screen.blit(text_bestScore, (430, 40))
        elif self.player_mode == "two":
            font = pygame.font.Font(Constants.FONT, 28)
            text_level = font.render("Level: " + str(self.current_level + 1), True, Constants.WHITE)
            text_score = font.render("Score 1: " + str(Utils.get_score(self.player_one.username)), True, Constants.WHITE)
            text_bestScore = font.render("Best Score 1: " + str(Utils.get_best_score(self.player_one.username)), True, Constants.WHITE)
            text_score_two = font.render("Score 2: " + str(Utils.get_score(self.player_two.username)), True, Constants.RED)
            text_bestScore_two = font.render("Best Score 2: " + str(Utils.get_best_score(self.player_two.username)), True, Constants.RED)


            #  Display player 1's lives as heart images
            for i in range(self.paddle1.lives):
                x = 10 + i * (self.heart_rect.width + 5)
                y = 5
                self.screen.blit(self.heart_image, (x, y))


            if self.player_mode == "two":
                #  Display player 2's lives as heart images
                for i in range(self.paddle2.lives):
                    x = 10 + i * (self.heart_rect.width + 5)
                    y = 30
                    self.screen.blit(self.heart_image, (x, y))

            if self.player_mode == "three":
                #  Display player 3's lives as heart images
                for i in range(self.paddle2.lives):
                    x = 10 + i * (self.heart_rect.width + 5)
                    y = 30
                    self.screen.blit(self.heart_image, (x, y))


            self.screen.blit(text_level, (10, 45))
            self.screen.blit(text_score, (500, 10))
            self.screen.blit(text_bestScore, (443, 40))
            self.screen.blit(text_score_two, (300, 10))
            self.screen.blit(text_bestScore_two, (243, 40))
        pygame.display.update()



    # Function to display start menu
    def draw_menu(self):
        start_img = pygame.image.load(Constants.BACK).convert()
        self.screen.blit(start_img, (0, 0))
        font = pygame.font.Font(Constants.FONT, 42)
        text_title = font.render("Atari Breakout", True, Constants.BLACK)
        text_single = font.render("1 - Single Player", True, Constants.BLACK)
        text_two = font.render("2 - Two Players", True, Constants.BLACK)
        text_twoAI = font.render("3 - Two Players with AI", True, Constants.BLACK)
        text_best = font.render("4 - Best Score", True, Constants.BLACK)
        text_lead = font.render("5 - Leaderboard", True, Constants.BLACK)
        text_custom_level = font.render("6 - Custom level", True, Constants.BLACK)
        text_quit = font.render("7 - Quit", True, Constants.BLACK)
        text_user_stats = font.render("8 - User Stats", True, Constants.BLACK)

        text_position = text_title.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 8 - 30))
        self.screen.blit(text_title, text_position)
        text_position = text_single.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 8 + 50))
        self.screen.blit(text_single, text_position)
        text_position = text_two.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 8 + 100))
        self.screen.blit(text_two, text_position)
        text_position = text_twoAI.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 8 + 150))
        self.screen.blit(text_twoAI, text_position)
        text_position = text_best.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 8 + 200))
        self.screen.blit(text_best, text_position)
        text_position = text_lead.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 8 + 250))
        self.screen.blit(text_lead, text_position)
        text_position = text_custom_level.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 8 + 300))
        self.screen.blit(text_custom_level, text_position)
        text_position = text_quit.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 8 + 350))
        self.screen.blit(text_quit, text_position)
        text_position = text_user_stats.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 8 + 400))
        self.screen.blit(text_user_stats, text_position)


    def next_level(self):
        self.current_level += 1
        Utils.update_best_level(self.player_one.username,self.current_level)
        if self.player_mode=="two":
            Utils.update_best_level(self.player_two.username,self.current_level)
        if self.current_level >= len(self.levels):
            #  All levels completed, reset the game
            self.reset()
        else:
            self.reset_level()


    def reset_level(self):
        #  Store the remaining lives in variables before resetting
        remaining_lives_p1 = self.paddle1.lives
        remaining_lives_p2 = self.paddle2.lives if self.player_mode == "two" or self.player_mode == "three" else None


        #  Reset the paddles and balls
        self.paddle1.reset()
        self.ball1_reset()
        if self.player_mode == "two":
            self.paddle2.reset()
            self.ball2_reset()
        elif self.player_mode == "three":
            self.paddle2.reset()
            self.ball2_reset()


        #  Restore the remaining lives
        self.paddle1.lives = remaining_lives_p1
        if self.player_mode == "two":
            self.paddle2.lives = remaining_lives_p2
        elif self.player_mode == "three":
            self.paddle2.lives = remaining_lives_p2


        #  Create new bricks for the level
        self.bricks = []
        self.create_bricks()
        


    def reset(self):
        self.player_mode = None
        self.current_level = 0 
        self.game_over = False
        self.bricks = []
        self.initialize_game()
        

    # function to display end menu
    def draw_end_menu(self):
        if self.player_mode != "two":
            end_img = pygame.image.load(Constants.BACK).convert()
            self.screen.blit(end_img, (0, 0))
            font = pygame.font.Font(Constants.FONT, 42)
            text_thank_you = font.render("Thank You for Playing!", True, Constants.BLACK)
            text_quit = font.render("Q - Quit", True, Constants.BLACK)
            text_play_again = font.render("P - Play Again", True, Constants.BLACK)
            text_score_end = font.render("Score: " + str(Utils.get_score(self.player_one.username)), True, Constants.BLACK)
            text_bestScore_end = font.render("Best Score: " + str(Utils.get_best_score(self.player_one.username)), True, Constants.BLACK)


            text_position = text_thank_you.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 5 + 35))
            self.screen.blit(text_thank_you, text_position)
            text_position = text_quit.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 5 + 95))
            self.screen.blit(text_quit, text_position)
            text_position = text_play_again.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 5 + 155))
            self.screen.blit(text_play_again, text_position)
            text_position = text_score_end.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 5 + 205))
            self.screen.blit(text_score_end, text_position)
            text_position = text_bestScore_end.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 5 + 255))
            self.screen.blit(text_bestScore_end, text_position)

        if self.player_mode == "two":
            end_img = pygame.image.load(Constants.BACK).convert()
            self.screen.blit(end_img, (0, 0))
            font = pygame.font.Font(Constants.FONT, 42)
            text_thank_you = font.render("Thank You for Playing!", True, Constants.BLACK)
            text_quit = font.render("Q - Quit", True, Constants.BLACK)
            text_play_again = font.render("P - Play Again", True, Constants.BLACK)
            text_score_end = font.render("Score 1: " + str(Utils.get_score(self.player_one.username)), True, Constants.BLACK)
            text_bestScore_end = font.render("Best Score 1: " + str(Utils.get_best_score(self.player_one.username)), True, Constants.BLACK)
            text_score_end_two = font.render("Score 2: " + str(Utils.get_score(self.player_two.username)), True, Constants.BLACK)
            text_bestScore_end_two = font.render("Best Score 2: " + str(Utils.get_best_score(self.player_two.username)), True, Constants.BLACK)
            
            text_position = text_thank_you.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 7 + 35))
            self.screen.blit(text_thank_you, text_position)
            text_position = text_quit.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 7 + 95))
            self.screen.blit(text_quit, text_position)
            text_position = text_play_again.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 7 + 155))
            self.screen.blit(text_play_again, text_position)
            text_position = text_score_end.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 7 + 205))
            self.screen.blit(text_score_end, text_position)
            text_position = text_bestScore_end.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 7 + 255))
            self.screen.blit(text_bestScore_end, text_position)
            text_position = text_score_end_two.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 7 + 305))
            self.screen.blit(text_score_end_two, text_position)
            text_position = text_bestScore_end_two.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 7 + 355))
            self.screen.blit(text_bestScore_end_two, text_position)

    # function which handles keypressed on end screen
    def handle_end_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  #  Quit
                    Utils.update_user_stats(self.current_time,self.bricks_broken_p1,self.powerups_p1)
                    if self.player_mode == "two":
                        Utils.update_user_stats(self.current_time,self.bricks_broken_p2,self.powerups_p2)
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_p:  #  Play Again
                    self.reset()
                    self.game_over = False

    # main running game loop
    def run(self):
        try:
            running = True
            while running:
                self.current_time = pygame.time.get_ticks()
                self.elapsed_time = self.current_time - self.start_time
                if self.elapsed_time >= Constants.DURATION:
                    self.paddle1.width = Constants.PADDLE_WIDTH
                if self.player_mode == "two" :
                    self.elapsed_time_two = self.current_time - self.start_time_two
                    if self.elapsed_time_two >= Constants.DURATION:
                        self.paddle2.width = Constants.PADDLE_WIDTH
                self.handle_events()
                self.update()
                if self.player_mode == "three":
                    self.animate_cpu() # calls the AI function
                if self.game_over:
                    self.draw_end_menu()
                    #  Process end menu events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:  #  Quit
                                Utils.update_user_stats(self.current_time,self.bricks_broken_p1,self.powerups_p1,self.player_one.username)
                                if self.player_mode == "two":
                                    Utils.update_user_stats(self.current_time,self.bricks_broken_p2,self.powerups_p2, self.player_two.username)
                                running = False
                            elif event.key == pygame.K_p:  #  Play Again
                                self.reset()
                                self.game_over = False
                else:
                    self.draw()
                self.clock.tick(Constants.FPS)
                pygame.display.update()  #  Ensure display is updated
        except Exception as e:
            print(f"An exception occurred in run method: {e}")
    pygame.quit()