import time
from turtle import Screen

from Day_20_21.scoreboard import Scoreboard
from food import Food

from Day_20_21.snake import Snake

screen = Screen()

screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

screen.update()
game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)

    snake.move()
    # collision with food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    #         DETECT COLLISION WITH WALL
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        scoreboard.reset()
        snake.reset()
# Detect collision with tail
for segment in snake.segments:
    if segment == snake.head:
        pass

    elif snake.head.distance(segment) < 10:
        scoreboard.reset()
        snake.reset()

screen.exitonclick()
