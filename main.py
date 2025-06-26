
import DbHelper
import Utils
from breakoutgame import BreakoutGame



def main():
    DbHelper.setup_database()
    current_user = Utils.enter_user()
            
    game = BreakoutGame(current_user)
    game.initialize_game()
    game.run()


if __name__ == "__main__":
    main()



