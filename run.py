""" Import Section """

# import random module
import random

# import curses module
import curses

# import time module
import time

# Imports gspread function for logging username and logging scores
import gspread
from google.oauth2.service_account import Credentials

# Scope Code to call Google Drive
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Scope for Data Handling - From Code Institute - Love Sandwiches Walkthrough
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('speed_snake_scores')

scorelog = SHEET.worksheet('scorelog')

data = scorelog.get_all_values()

# print(data)


# Function to allow user to enter a username
def enter_username():
    """
    Prompt Player to enter username to start game
    Max length 15 Characters
    """
    while True:
        username = input("Please enter your name: \n")
        if len(username) <= 15:
            return("Welcome", username, "!")
            break
        else:
            print("Username too long - Max 15 Characters")
        continue


enter_username()


# Variables to initialize Gameplay
curses.initscr()
h = 24
w = 80
win = curses.newwin(h, w, 0, 0)
win.keypad(1)
curses.curs_set(0)
score = 0

# Variables to Set Snake and Food Start positions
snake_head = [10, 15]
body_position = [[15, 10], [14, 10], [13, 10]]
food_position = [20, 20]

# Show the Food on screen
win.addch(food_position[0], food_position[1], curses.ACS_BULLET)

# 
prev_button_direction = 1
button_direction = 1
key = curses.KEY_RIGHT


# Function to display score on top bar
def display_score(win, score):
    h, w = newwin.getmaxyx()
    score = 0
    win.addstr(0, 0, "Score: " + str(score))

display_score()

# Function to add to score when snake eats the food
def get_food(score):
    food_position = [random.randint(1, h-2), random.randint(1, w-2)]
    score += 10
    return food_position, score


# Functions to end game when Snake hits wall or itself
def hit_wall(snake_head):
    """
    If statement if snake head collides with a boundary wall
    """
    if snake_head[0] >= h-1 or snake_head[0] <= 0 or snake_head[1] >= w-1 or snake_head[1] <= 0:
        return 1
    else:
        return 0


def hit_self(body_position):
    """
    If statement for when snake collides with own body
    """
    snake_head = body_position[0]
    if snake_head in body_position[1:]:
        return 1
    else:
        return 0


# Set gameplay border an keyboard inputs
a = []
while True:
    win.border(0)
    win.timeout(100)
    next_key = win.getch()
    """
    variable to get user input from a keyboard
    """
    if next_key == -1:
        key = key
    else:
        key = next_key


# Define  Keyboard inputs to move Snake around the screen
    if key == curses.KEY_LEFT and prev_button_direction != 1:
        button_direction = 0
    elif key == curses.KEY_RIGHT and prev_button_direction != 0:
        button_direction = 1
    elif key == curses.KEY_UP and prev_button_direction != 2:
        button_direction = 3
    elif key == curses.KEY_DOWN and prev_button_direction != 3:
        button_direction = 2
    else:
        pass

    prev_button_direction = button_direction

    if button_direction == 1:
        snake_head[1] += 1
    elif button_direction == 0:
        snake_head[1] -= 1
    elif button_direction == 2:
        snake_head[0] += 1
    elif button_direction == 3:
        snake_head[0] -= 1

    # Increase the Snakes Body length when the food is ate
    if snake_head == food_position:
        food_position, score = get_food(score)
        body_position.insert(0, list(snake_head))
        a.append(food_position)
        win.addch(food_position[0], food_position[1], curses.ACS_BULLET)

    else:
        body_position.insert(0, list(snake_head))
        last = body_position.pop()
        win.addch(last[0], last[1], ' ')

    # Display snake on screen
    win.addch(body_position[0][0], body_position[0][1], '#')

    # If Statement When Snake hits a wall or its own body activate Game Over
    if hit_wall(snake_head) == 1 or hit_self(body_position) == 1:
        break
   
# Display Player Score at Game Over Screen
(curses.initscr()).addstr(10, 20, "Congratulations you scored:" + str(score) + "points!")
(curses.initscr()).refresh()
time.sleep(2)
# Close the Game Window
curses.endwin()
print(a)
print(w, h)