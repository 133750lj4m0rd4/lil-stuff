import turtle
from random import randint
from time import sleep

colors = (
    (0,0.5,0.5),
    (0.5,0,0.5),
    (0.75,0.5,0),
)

turtle.bgcolor(0,0,0)
turtle.color(1,1,1)
turtle.pensize(1)
turtle.ht()
turtle.delay(0)
turtle.penup()
turtle.tracer(0)

def draw_cube(step:int):
    #turtle.tracer(0)
    turtle.setheading(30)
    turtle.pendown()
    for i in range(3):
        turtle.fillcolor(colors[i])
        turtle.begin_fill()
        turtle.forward(step)
        turtle.left(120)
        turtle.forward(step)
        turtle.left(60)
        turtle.forward(step)
        turtle.left(120)
        turtle.forward(step)
        turtle.right(60)
        turtle.end_fill()
        #turtle.update()
    turtle.penup()
    #turtle.tracer(1)
    #sleep(1/5)

def my_logo(step:int):
    dent = (step/10)+1.5

    turtle.setheading(-90)
    turtle.forward(step * 1.5)

    draw_cube(step-dent)

    turtle.setheading(90)
    turtle.forward(step)

    draw_cube(step-dent)

    turtle.setheading(30)
    turtle.forward(step)
    turtle.setheading(90)
    turtle.forward(step)

    draw_cube(step-dent)

    turtle.setheading(180)
    turtle.right(30)
    turtle.forward(step)
    turtle.left(60)
    turtle.forward(step)

    draw_cube(step-dent)

    turtle.setheading(-30)
    turtle.forward(step)

    draw_cube(step-dent)

    turtle.setheading(-30)
    turtle.forward(step)

    draw_cube(step-dent)

    turtle.setheading(180)
    turtle.right(30)
    turtle.forward(step)
    turtle.left(60)
    turtle.forward(step)

    draw_cube(step-dent)

    turtle.setheading(30)
    turtle.forward(step)
    turtle.setheading(90)
    turtle.forward(step)

    draw_cube(step-dent)



while True:
    l = 700

    for i in range(165):
        turtle.setpos(0,0)
        my_logo(l)
        l *= 0.98
        #if i%3 == 0: turtle.update()
        turtle.update()

    for i in range(200):
        turtle.setpos(randint(-700,700),randint(-350,350))
        my_logo(l)
        turtle.update()
    
    sleep(1)
    turtle.clear()
    turtle.update()
    sleep(0.5)
    turtle.bgcolor(1,1,1)
    turtle.update()
    sleep(0.15)
    turtle.bgcolor(0,0,0)
    sleep(0.1)
    turtle.update()
