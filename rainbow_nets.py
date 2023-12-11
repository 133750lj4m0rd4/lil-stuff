import turtle

colors = [
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,0,1),
    (0,1,1),
]

turtle.bgcolor(0,0,0)
turtle.pensize(3)
turtle.speed(0)
turtle.penup()

for i in range(6):
    turtle.color(colors[i])

    turtle.backward(400)
    turtle.right(90)
    turtle.backward(400)
    turtle.left(90)

    for i in range(-16,17):
        turtle.pendown()
        turtle.forward(800)
        turtle.penup()
        turtle.backward(800)
        turtle.right(90)
        turtle.forward(25)
        turtle.left(90)

    turtle.setpos(0,0)
    turtle.right(30)

while True: turtle.update()