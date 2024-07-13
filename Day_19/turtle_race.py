# import random
# from turtle import Turtle, Screen
# 
# is_race_on = False
# 
# screen = Screen()
# screen.setup(width=500, height=400)
# user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color:")
# colors = ["red", "green", "orange", "blue", "purple", "yellow"]
# y_positions = [-70, -40, -10, 20, 50, 80]  # Fixed the y_positions list
# all_turtles = []
# 
# for turtle_index in range(0, 6):
#     new_turtle = Turtle(shape="turtle")
#     new_turtle.color(colors[turtle_index])
#     new_turtle.penup()
#     new_turtle.goto(x=-230, y=y_positions[turtle_index])
#     all_turtles.append(new_turtle)
# 
# if user_bet:
#     is_race_on = True
# 
# while is_race_on:
#     for turtle in all_turtles:
#         if turtle.xcor() > 230:
#             is_race_on = False
#             winning_color = turtle.pencolor()
#             if winning_color == user_bet:
#                 print(f"You've won! The {winning_color} turtle is the winner!")
#             else:
#                 print(f"You've lost! The {winning_color} turtle is the winner!")
#         rand_distance = random.randint(0, 10)
#         turtle.forward(rand_distance)
# 
# screen.exitonclick()
# 

import random
from turtle import Turtle, Screen
import tkinter as tk

screen = Screen()
is_race_on = False
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color:")
# colors = ["red", "green", "orange", "blue", "purple", "yellow"]
# y_positions = [-70, -40, -10, 20, 50, 80]  # Fixed the y_positions list
# Initialize the list of turtles globally
all_turtles = []


# Function to start the race
def start_race():
    global is_race_on, all_turtles, user_bet

    # Setup turtle colors and y positions
    colored = [color_var[i].get() for all_turtles in range(6)]
    y_positions = [-70, -40, -10, 20, 50, 80]  # Fixed the y_positions list

    # Initialize turtles
    all_turtles = []
    for turtle_index in range(0, 6):
        new_turtle = Turtle(shape=shape_var[turtle_index].get())
        new_turtle.color(colors[turtle_index])
        new_turtle.penup()
        new_turtle.goto(x=-230, y=y_positions[turtle_index])
        all_turtles.append(new_turtle)

    if user_bet.get():
        is_race_on = True
        run_race()  # Start the race


# Function to run the race
def run_race():
    global is_race_on, all_turtles, user_bet

    while is_race_on:
        for turtle in all_turtles:
            if turtle.xcor() > 230:
                is_race_on = False
                winning_color = turtle.pencolor()
                if winning_color == user_bet.get():
                    print(f"You've won! The {winning_color} turtle is the winner!")
                else:
                    print(f"You've lost! The {winning_color} turtle is the winner!")
                break  # Exit the loop when race ends
            rand_distance = random.randint(0, 10)
            turtle.forward(rand_distance)

    # Reset the race flag
    is_race_on = False


# GUI Setup
root = tk.Tk()
root.title("Turtle Race Setup")

# Dropdown menus for shape and color selection
shapes = ['turtle', 'square', 'circle', 'triangle']  # Customize with desired shapes
colors = ['red', 'green', 'orange', 'blue', 'purple', 'yellow']  # Customize with desired colors

shape_var = []
color_var = []
for i in range(6):
    shape_var.append(tk.StringVar(root))
    shape_var[-1].set(shapes[0])  # Initial shape

    color_var.append(tk.StringVar(root))
    color_var[-1].set(colors[i % len(colors)])  # Initial color

    shape_menu = tk.OptionMenu(root, shape_var[-1], *shapes)
    shape_menu.grid(row=i, column=0)

    color_menu = tk.OptionMenu(root, color_var[-1], *colors)
    color_menu.grid(row=i, column=1)

# User bet input
user_bet = tk.StringVar(root)
tk.Entry(root, textvariable=user_bet).grid(row=6, column=0, columnspan=2)

# Start race button
start_button = tk.Button(root, text="Start Race", command=start_race)
start_button.grid(row=7, column=0, columnspan=2)

root.mainloop()
