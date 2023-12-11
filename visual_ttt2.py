import turtle
import time

def half_X(player,cell_size):
    pos = turtle.position()

    lenght = ((cell_size**2)*2)**0.5
    if player == 2: turtle.forward(cell_size)
    turtle.right(45)    if player == 1 else turtle.right(45+90)
    turtle.color(1,0,0) if player == 1 else turtle.color(0.5,0.5,1)

    turtle.forward(lenght/7)
    turtle.pendown()
    turtle.forward(lenght*5/7)
    turtle.penup()
    turtle.forward(lenght/7)

    turtle.setpos(pos)
    turtle.setheading(0)

class play_feild:
    def __init__(self):
        self.grid = [
            [0,0,0],
            [0,0,0],
            [0,0,0],
        ]
        self.crosses = ['.','/','\\','X',]
        self.previous_move = (4,4)
        self.pointer = (1,1)
        self.size = 400
    
    def render(self):
        for line in self.grid:
            print(f" {self.crosses[line[0]]} | {self.crosses[line[1]]} | {self.crosses[line[2]]}")
            if (not self.grid[2] is line):
                print("---+---+---")

    def turtle_render_prep(self):
        turtle.bgcolor(0,0,0)
        turtle.color(1,1,1)
        turtle.pensize(3)
        turtle.penup()
        turtle.setpos(-(self.size/2),(self.size/2))
        turtle.setheading(-90)

        for i in range(4):
            turtle.left(90)
            turtle.pendown()
            turtle.forward(self.size)
            turtle.backward(self.size)
            turtle.setheading(-90)
            turtle.penup()
            turtle.forward(self.size/3)

        turtle.setpos(-(self.size/2),(self.size/2))
        turtle.setheading(0)

        for i in range(4):
            turtle.right(90)
            turtle.pendown()
            turtle.forward(self.size)
            turtle.backward(self.size)
            turtle.setheading(0)
            turtle.penup()
            turtle.forward(self.size/3)
        
        turtle.setpos(-(self.size/2),(self.size/2))

    def move(self,player,xy):
        if self.previous_move == xy: 
            return(1)
        if self.grid[xy[0]][xy[1]] == player or self.grid[xy[0]][xy[1]] == 3: 
            return(1)
        self.grid[xy[0]][xy[1]] += player
        self.previous_move = xy
        return(0)
    
    def vin_check(self):
        for i in range(3):
            if (self.grid[i][0] == 3 and 
                self.grid[i][1] == 3 and 
                self.grid[i][2] == 3):
                return(1)
            if (self.grid[0][i] == 3 and 
                self.grid[1][i] == 3 and 
                self.grid[2][i] == 3):
                return(1)
        if (self.grid[0][0] == 3 and 
            self.grid[1][1] == 3 and 
            self.grid[2][2] == 3):
            return(1)
        if (self.grid[2][0] == 3 and 
            self.grid[1][1] == 3 and 
            self.grid[0][2] == 3):
            return(1)
        return(0)

    def game_loop(self):
        game.turtle_render_prep()
        while(not self.vin_check()):
            for i in range(1,3):
                print(f"p{i} move")
                self.render()
                while (True):
                    x = int(input("line:")) - 1
                    y = int(input("column:")) - 1
                    if (self.move(i,(x,y)) == 0):                    
                        turtle.setpos((-self.size/2) + self.size*y/3,
                                      (self.size/2) - self.size*x/3)
                        half_X(i,self.size/3)
                        break
                    else:
                        print("don't >:^(")
                
                if (self.vin_check()): 
                    print(f"p{i} vins")
                    break
        time.sleep(10)

game = play_feild()
game.game_loop()