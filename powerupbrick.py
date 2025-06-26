import Constants
import Utils
import random
from brickclass import Brick
from user import User


#child class to Brick class
class PowerupBrick(Brick):
    def __init__(self, brick):
        super().__init__(brick.x, brick.y,brick.hit_points, brick.color)
        self.powerupType = Constants.POWERUP_TYPES
  
    # Powerup functions
    def score_boost(self,userobj):
        Utils.update_score(userobj.username, 9)

    def increase_paddle_length(self,breakout,userobj):
        if userobj.player_id==1:
            breakout.paddle1.width = Constants.POWERUP_PADDLE_WIDTH
        else:
            breakout.paddle2.width = Constants.POWERUP_PADDLE_WIDTH

    def increase_lives(self,breakout, userobj):
        if userobj.player_id==1:
            breakout.paddle1.lives +=1
        else:
            breakout.paddle2.lives +=1

    #method to select a powerup randomly
    def activate_powerup(self,breakout = object, userobj = User):
        Utils.update_score(userobj.username,1)
        powerup_types = Constants.POWERUP_TYPES
        random_number = random.randint(0,len(powerup_types)-1)

        if(powerup_types[random_number] == "Paddle"):
            self.increase_paddle_length(breakout,userobj)
            return "images/paddlef.png"
        elif(powerup_types[random_number] == "Lives"):
            self.increase_lives(breakout,userobj)
            return "images/livesf.png"
        else:
            self.score_boost(userobj)
            return "images/scoref.png"