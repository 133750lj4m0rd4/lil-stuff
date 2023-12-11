import turtle

colors = [
    (1,0,0),
    (1,0.5,0),
    (1,1,0),
    (0,1,0),
    (0,0.75,0.75),
    (0,0,1),
    (0.75,0,0.75),
]
step = 35
cycles = 11
angle = 180/cycles
squares = 51

turtle.bgcolor(0,0,0)
turtle.pensize(1)
turtle.speed(0)
turtle.tracer(0)
turtle.penup()

for i in range(cycles):
    turtle.color(colors[i%7])

    turtle.backward(step*squares/2)
    turtle.right(90)
    turtle.backward(step*squares/2)
    turtle.left(90)

    for i in range(int(-squares/2),int(squares/2)+(squares%2)+1):
        turtle.pendown()
        turtle.forward(step*squares)
        turtle.penup()
        turtle.backward(step*squares)
        turtle.right(90)
        turtle.forward(step)
        turtle.left(90)
        turtle.update()

    turtle.setpos(0,0)
    turtle.right(angle)

turtle.setpos(-10000,-10000)

while True: turtle.update()