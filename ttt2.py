import turtle

class play_feild:
    def __init__(self):
        self.grid = [
            [0,0,0],
            [0,0,0],
            [0,0,0],
        ]
        self.crosses = ['.','\\','/','X',]
        self.previous_move = (4,4)
        self.pointer = (1,1)
    
    def render(self):
        for line in self.grid:
            print(f" {self.crosses[line[0]]} | {self.crosses[line[1]]} | {self.crosses[line[2]]}")
            if (not self.grid[2] is line):
                print("---+---+---")

    def turtle_render(self):
        pass

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
        while(True):
            print("p1 move")
            self.render()
            while (True):
                x = int(input("x:")) - 1
                y = int(input("y:")) - 1
                if (self.move(1,(x,y)) == 0):
                    break
                else:
                    print("don't >:^(")
            
            if (self.vin_check()): 
                print("p1 vins")
                break

            print("p2 move")
            self.render()
            while (True):
                x = int(input("x:")) - 1
                y = int(input("y:")) - 1
                if (self.move(2,(x,y)) == 0):
                    break
                else:
                    print("don't >:^(")
                        
            if (self.vin_check()): 
                print("p2 vins")
                break

game = play_feild()
game.game_loop()