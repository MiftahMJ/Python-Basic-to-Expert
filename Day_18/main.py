import random
import turtle as Turtle

# Set up the turtle
timmy_the_turtle = Turtle
timmy_the_turtle.shape("turtle")
timmy_the_turtle.pensize(1)
timmy_the_turtle.speed("fastest")


# # Define colors and directions
# colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan", "magenta"]
# directions = [0, 90, 180, 270]

#
# Function to generate random color
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    random_c = (r, g, b)
    return random_c  # Return a tuple of integers (r, g, b)

    # Main drawing loop
    # for _ in range(200):
    #     timmy_the_turtle.color(random.choice(colors))
    #     timmy_the_turtle.forward(30)
    #     timmy_the_turtle.right(random.choice(directions))


timmy_the_turtle.circle(100)
timmy_the_turtle.color(random_color())

screen = timmy_the_turtle.Screen()
screen.exitonclick()

# timmy_the_turtle.forward(100)
# timmy_the_turtle.left(98)
# timmy_the_turtle.forward(100)
# timmy_the_turtle.left(98)
# timmy_the_turtle.forward(100)
# timmy_the_turtle.left(98)
# timmy_the_turtle.forward(100)
# for _ in range(15):
#     timmy_the_turtle.forward(10)
#     timmy_the_turtle.penup()
#     timmy_the_turtle.forward(10)
#     timmy_the_turtle.pendown()


# def draw_shape(num_sides):
#     angle = 360 / num_sides
#
#     for _ in range(num_sides):
#         timmy_the_turtle.forward(100)
#         timmy_the_turtle.right(angle)
#
#
# # Call the draw_shape function for shapes with sides ranging from 3 to 9
# for shape_side_n in range(3, 10):
#     timmy_the_turtle.color(choice(colors))
#     draw_shape(shape_side_n)
# Set the color mode to 255
