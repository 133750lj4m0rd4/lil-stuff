class figure:
    def __init__(self,is_white:bool,type:chr,position:tuple[int]):
        self.is_white = is_white
        self.type = type
        self.position = position


class board():
    def __init__(self):
        self.figures = {
            figure(True,'R',(0,0)),
            figure(True,'k',(0,1)),
            figure(True,'b',(0,2)),
            figure(True,'Q',(0,3)),
            figure(True,'K',(0,4)),
            figure(True,'b',(0,5)),
            figure(True,'k',(0,6)),
            figure(True,'R',(0,7)),

            figure(True,'p',(1,0)),
            figure(True,'p',(1,1)),
            figure(True,'p',(1,2)),
            figure(True,'p',(1,3)),
            figure(True,'p',(1,4)),
            figure(True,'p',(1,5)),
            figure(True,'p',(1,6)),
            figure(True,'p',(1,7)),
            
            figure(False,'R',(7,0)),
            figure(False,'k',(7,1)),
            figure(False,'b',(7,2)),
            figure(False,'Q',(7,3)),
            figure(False,'K',(7,4)),
            figure(False,'b',(7,5)),
            figure(False,'k',(7,6)),
            figure(False,'R',(7,7)),

            figure(False,'p',(6,0)),
            figure(False,'p',(6,1)),
            figure(False,'p',(6,2)),
            figure(False,'p',(6,3)),
            figure(False,'p',(6,4)),
            figure(False,'p',(6,5)),
            figure(False,'p',(6,6)),
            figure(False,'p',(6,7)),
        }
        self.board = []
        self.update_board()
    
    def update_board(self):
        self.board = [
            [' ',' ',' ',' ',' ',' ',' ',' ',],

            [' ',' ',' ',' ',' ',' ',' ',' ',],

            [' ',' ',' ',' ',' ',' ',' ',' ',],
            
            [' ',' ',' ',' ',' ',' ',' ',' ',],
            
            [' ',' ',' ',' ',' ',' ',' ',' ',],
            
            [' ',' ',' ',' ',' ',' ',' ',' ',],
            
            [' ',' ',' ',' ',' ',' ',' ',' ',],
            
            [' ',' ',' ',' ',' ',' ',' ',' ',],
        ]
        for figure in self.figures:
            self.board[figure.position[0]][figure.position[1]] = figure.type

    def render_board(self):
        print("\n+"+("-----"+"+")*8,end="")
        is_odd = False
        for line in self.board:
            is_odd = not is_odd
            print("\n|", end="")
            for j in range(4):
                print("     "+"|"+"....."+"|" if is_odd else "....."+"|"+"     "+"|",end="")
            print("\n|", end="")
            for cell in line:
                print(f"  {cell}  "+"|" if is_odd else f"..{cell if cell != ' ' else '.'}.."+"|",end="")
                is_odd = not is_odd
            print("\n|", end="")
            for j in range(4):
                print("     "+"|"+"....."+"|" if is_odd else "....."+"|"+"     "+"|",end="")
            print("\n+"+("-----"+"+")*8,end="")

board().render_board()