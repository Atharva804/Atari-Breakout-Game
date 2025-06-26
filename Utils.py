import Constants
import pygame_gui
import pygame
import sys
import sqlite3 # Database Module 
from user import User
import random
import re
from gameinit import GameInit


def get_color(hit_points):
    if hit_points == 1:
        return Constants.RED
    elif hit_points == 2:
        return Constants.YELLOW
    elif hit_points == 3:
        return Constants.GREEN
    elif hit_points == 4:
        return Constants.ORANGE
    else:
        return Constants.BLUE

#change
# function to check is user has an account
def enter_user():
       
        pygame.init()
        gameInit = GameInit()
        final_text= ""
        
        Text_input_yes = pygame_gui.elements.UITextEntryLine(relative_rect= pygame.Rect((120, 145), (400, 50)), manager=gameInit.Manager, object_id="#confirmation")
        while True:
            UI_refresh_rate = gameInit.CLOCK.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#confirmation":
                    Text_input_yes = pygame_gui.elements.UITextEntryLine.kill(self=Text_input_yes)
                    final_text = event.text
                gameInit.Manager.process_events(event)

            gameInit.Manager.update(UI_refresh_rate)
            # gameInit.SCREEN.fill("white")
            img = pygame.image.load(Constants.BACK).convert()
            gameInit.SCREEN.blit(img, (0, 0))
            font = pygame.font.Font(Constants.FONT, 38)
            text_heading = font.render("Do you have an account? (yes/no/exit)", True, Constants.BLACK)
            text_position = text_heading.get_rect(center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 - 150))
            gameInit.SCREEN.blit(text_heading, text_position)
            gameInit.Manager.draw_ui(gameInit.SCREEN)
            pygame.display.update()

            if final_text == "yes" or final_text == "YES":
                current_user = login_user()
                if current_user is not None:
                    pygame.quit()
                    return current_user
                else:
                    print("Invalid login. Please try again.")
            elif final_text == "no" or final_text == "NO":
                register_user()
                final_text = ""
                Text_input_yes = pygame_gui.elements.UITextEntryLine(relative_rect= pygame.Rect((120, 145), (400, 50)), manager=gameInit.Manager, object_id="#confirmation")
            elif final_text == "exit" or final_text == "EXIT":
                pygame.quit()
                sys.exit()
            else: # reconsider this condition
                # print("Please enter 'yes', 'no', or 'exit'.")
                if(final_text != ""):
                    final_text = ""
                    Text_input_yes = pygame_gui.elements.UITextEntryLine(relative_rect= pygame.Rect((120, 145), (400, 50)), manager=gameInit.Manager, object_id="#confirmation")
            
#change
# function to create an account
def register_user():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    status = "reg"

    print("register user")

    username = take_input("name", status)
    password = take_input("pass", status)
    email = take_input("email", status)

    # Password and email validation
    while True:
        if (len(password) < 8 or
            not re.search("[a-z]", password) or
            not re.search("[A-Z]", password) or
            not re.search("[0-9]", password) or
            not re.search("[!£$%&*@?><\"]", password)):
            print("Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a symbol (!, £, $, %, &, *, @, ?, <, >, \").")
            password = take_input("pass", status)
        elif not ("@" in email and email.endswith(".com")):
            print("Invalid email. Please make sure that it contains '@' and ends with '.com' ")
            email = take_input("email", status)
        else:
            break
    # Insert user data into the database
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        update_user_stats(0,0,0,username)
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")
    except Exception as e:
        print(f"An exception occurred while connecting to db: {e}")
    finally:
            conn.close()
#change
#function to take input from the screen           
def take_input(label, Status):
    gameInit = GameInit()
    if label == "name":
        if Status == "reg":
            input_name = gameInit.display_box("#name", "Create username")
        elif Status == "Login":
            input_name = gameInit.display_box("#name", "Enter username")
    elif label == "pass":
        if Status == "reg":
            input_pass = gameInit.display_box("#pass", "Create password (8 characters long, includes \n  uppercase, lowercase, number, and symbol)")
        elif Status == "Login":
            input_pass = gameInit.display_box("#pass", "Enter password")
    elif label == "email":
        input_email = gameInit.display_box("#email", "Enter your email")

    while True:
        UI_refresh_rate = gameInit.CLOCK.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#name":
                input_name = pygame_gui.elements.UITextEntryLine.kill(self=input_name)
                return event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#pass":
                input_pass = pygame_gui.elements.UITextEntryLine.kill(self=input_pass)
                return event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#email":
                input_email = pygame_gui.elements.UITextEntryLine.kill(self=input_email)
                return event.text
            gameInit.Manager.process_events(event)
        gameInit.Manager.update(UI_refresh_rate)
        gameInit.Manager.draw_ui(gameInit.SCREEN)
        pygame.display.update()

#change
# check if login details enterd by user is correct
def login_user():
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        status = "Login"

        print("login user")

        username = take_input("name", status)
        password = take_input("pass", status)

        # username = input("Enter username: ")
        # password = input("Enter password: ")

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result and result[0] == password:
            print("Login successful!")
            user = User(username)
            return user
        else:
            print("Login failed!")
            return None

    except sqlite3.Error as error:
        print("An error occurred:", error)
    except Exception as e:
        print(f"An exception occurred while connecting to db: {e}")

    finally:
        conn.close()

def update_score(user,score):
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO scores (username, score, best_score) VALUES (?, 0, 0)", (user,))
        cursor.execute("SELECT score FROM scores WHERE username = ?", (user,))
        result = cursor.fetchone()
       
        new_score = result[0] + score
       

        # Update the score for the specified user
        cursor.execute('''
                        UPDATE scores
                        SET score = ?
                        WHERE username = ?
                    ''', (new_score, user))
        
        # updating the best score
        cursor.execute("SELECT best_score FROM scores WHERE username = ?", (user,))
        result = cursor.fetchone()
        
        bestScore = result[0]
        if new_score > bestScore:
            bestScore = new_score
            cursor.execute("UPDATE scores SET best_score = ? WHERE username = ?", (bestScore, user))

        conn.commit()
    
    except sqlite3.Error as e:
        # Handle SQLite-specific exceptions
        print("SQLite error:", e)

    except Exception as e:
        # Handle general exceptions
        print("An error occurred:", e)

    finally:
        # Ensure that the connection is closed, whether an exception occurred or not
        if conn:
            conn.close()


def reset_score(user):
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO scores (username, score, best_score) VALUES (?, 0, 0)", (user,))
        # Reset the score for the specified user to 0
        cursor.execute("UPDATE scores SET score = ? WHERE username = ?", (0, user))
        conn.commit()
    
    except sqlite3.Error as e:
        # Handle SQLite-specific exceptions
        print("SQLite error:", e)

    except Exception as e:
        # Handle general exceptions
        print("An error occurred:", e)

    finally:
        # Ensure that the connection is closed, whether an exception occurred or not
        if conn:
            conn.close()

# function to return score values shown on different screens
def get_score(user):
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()

        # Reset the score for the specified user to 0
        cursor.execute("SELECT score FROM scores WHERE username = ?", (user,))
        result = cursor.fetchone()
        conn.commit()
    
        return result[0]
    except sqlite3.Error as e:
        # Handle SQLite-specific exceptions
        print("SQLite error:", e)

    except Exception as e:
        # Handle general exceptions
        print("An error occurred:", e)

    finally:
        # Ensure that the connection is closed, whether an exception occurred or not
        if conn:
            conn.close()

# function to return best score values to shown on different screens
def get_best_score(user):
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()

        # Reset the score for the specified user to 0
        cursor.execute("SELECT best_score FROM scores WHERE username = ?", (user,))
        result = cursor.fetchone()
        conn.commit()
    
        return result[0]
    except sqlite3.Error as e:
        # Handle SQLite-specific exceptions
        print("SQLite error:", e)

    except Exception as e:
        # Handle general exceptions
        print("An error occurred:", e)

    finally:
        # Ensure that the connection is closed, whether an exception occurred or not
        if conn:
            conn.close()

# function to fetch and return leaderboard details
def get_leaderboard():
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()

        # Reset the score for the specified user to 0
        cursor.execute("SELECT username,best_score FROM scores ORDER BY best_score DESC")
        result = cursor.fetchall()
        # result is  list of tuples.
        conn.commit()

        return result
    except sqlite3.Error as e:
        # Handle SQLite-specific exceptions
        print("SQLite error:", e)

    except Exception as e:
        # Handle general exceptions
        print("An error occurred:", e)

    finally:
        # Ensure that the connection is closed, whether an exception occurred or not
        if conn:
            conn.close()
    
def choose_random(num):
    return random.randint(0,num-1)

# Function to update best level of a user
def update_best_level(user,level):
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO levels (username, level, best_level) VALUES (?, 0, 0)", (user,))
        cursor.execute("SELECT best_level from LEVELS where username =?" , (user,))
        result = cursor.fetchone()

        bestLevel = result[0]
        if(level > bestLevel):
            cursor.execute("UPDATE levels SET best_level = ? WHERE username = ?", (level, user))

        conn.commit()
    
    except sqlite3.Error as e:
        # Handle SQLite-specific exceptions
        print("SQLite error:", e)

    except Exception as e:
        # Handle general exceptions
        print("An error occurred:", e)

    finally:
        # Ensure that the connection is closed, whether an exception occurred or not
        if conn:
            conn.close()

# function which updates user statistics
def update_user_stats(time, bricksBroken, powerups,user):
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO statistics (username, total_time, bricks_broken, powerup_collected) VALUES (?,0, 0, 0)", (user,))
        cursor.execute("SELECT total_time, bricks_broken, powerup_collected from statistics where username =?" , (user,))
        result = cursor.fetchone()

        
        total_min =  round(time / (1000 * 60),2)
        total_time= result[0] + total_min
        bricks_broken = result[1] + bricksBroken
        powerup_collected = result[2] + powerups

        cursor.execute("UPDATE statistics SET total_time = ?,bricks_broken= ? , powerup_collected=? WHERE username = ?", (total_time,bricks_broken, powerup_collected, user))
        

        conn.commit()
    
    except sqlite3.Error as e:
        # Handle SQLite-specific exceptions
        print("SQLite error:", e)

    except Exception as e:
        # Handle general exceptions
        print("An error occurred:", e)

    finally:
        # Ensure that the connection is closed, whether an exception occurred or not
        if conn:
            conn.close()

# returns user stats to display on screen
def get_user_statistics(user):
    try:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()

        cursor.execute("SELECT total_time, bricks_broken, powerup_collected from statistics where username =?" , (user,))
        result = cursor.fetchone()
        # result is  list of tuples.
        conn.commit()
        return result
    except sqlite3.Error as e:
        # Handle SQLite-specific exceptions
        print("SQLite error:", e)

    except Exception as e:
        # Handle general exceptions
        print("An error occurred:", e)

    finally:
        # Ensure that the connection is closed, whether an exception occurred or not
        if conn:
            conn.close()