pawn_moves_stuff = {
    #(is_white,on_first_rank):(vec,vec)
    (True,True):((-1,0),(-2,0)),
    (True,False):((-1,0),),
    (False,True):((1,0),(2,0)),
    (False,False):((1,0),),
    #to un-ify code
    "ranks":(1,6,)
}

pawn_moves = lambda figure: pawn_moves_stuff[
        (figure.is_white,
         figure.position[0] == pawn_moves_stuff["ranks"][figure.is_white])
    ]

bishop_moves = [((i,i),(-i,i),(i,-i),(-i,-i),) for i in range(1,8)]
bishop_moves = tuple(bishop_moves)

rook_moves = [((i,0),(-i,0),(0,i),(0,-i),) for i in range(1,8)]
rook_moves = tuple(rook_moves)

queen_moves = list()
for i in range(7):
    queen_moves.append(list(rook_moves[i]))
    queen_moves[i].extend(bishop_moves[i])
    queen_moves[i] = tuple(queen_moves[i])
queen_moves = tuple(queen_moves)

knight_moves = [(1,2),(2,1)]
knight_moves.extend(map(lambda a: (-a[0],a[1]),knight_moves[0:len(knight_moves)]))
knight_moves.extend(map(lambda a: (a[0],-a[1]),knight_moves[0:len(knight_moves)]))
knight_moves = tuple(knight_moves)

border_check = lambda pos: pos[0] >= 0 and pos[0] <= 7 and pos[1] >= 0 and pos[1] <= 7
do_move = lambda pos,move: (pos[0]+move[0], pos[1]+move[1])

class figure:
    def __init__(self,is_white:bool,type:chr,position:tuple[int]):
        self.is_white = is_white
        self.type = type
        self.position = position
    
    def posible_moves(self):
        match self.type:
            case 'p':
                return pawn_moves(self)


class board():
    def __init__(self):
        self.figures = {
            figure(False,'R',(0,0)),
            figure(False,'k',(0,1)),
            figure(False,'b',(0,2)),
            figure(False,'Q',(0,3)),
            figure(False,'K',(0,4)),
            figure(False,'b',(0,5)),
            figure(False,'k',(0,6)),
            figure(False,'R',(0,7)),

            figure(False,'p',(1,0)),
            figure(False,'p',(1,1)),
            figure(False,'p',(1,2)),
            figure(False,'p',(1,3)),
            figure(False,'p',(1,4)),
            figure(False,'p',(1,5)),
            figure(False,'p',(1,6)),
            figure(False,'p',(1,7)),
            
            figure(True,'R',(7,0)),
            figure(True,'k',(7,1)),
            figure(True,'b',(7,2)),
            figure(True,'Q',(7,3)),
            figure(True,'K',(7,4)),
            figure(True,'b',(7,5)),
            figure(True,'k',(7,6)),
            figure(True,'R',(7,7)),

            figure(True,'p',(6,0)),
            figure(True,'p',(6,1)),
            figure(True,'p',(6,2)),
            figure(True,'p',(6,3)),
            figure(True,'p',(6,4)),
            figure(True,'p',(6,5)),
            figure(True,'p',(6,6)),
            figure(True,'p',(6,7)),
        }
        self.board = []
        self.update_board()
        self.check_posible_moves()
    
    def update_board(self):
        self.board = [
            ['  ','  ','  ','  ','  ','  ','  ','  ',],

            ['  ','  ','  ','  ','  ','  ','  ','  ',],

            ['  ','  ','  ','  ','  ','  ','  ','  ',],
            
            ['  ','  ','  ','  ','  ','  ','  ','  ',],
            
            ['  ','  ','  ','  ','  ','  ','  ','  ',],
            
            ['  ','  ','  ','  ','  ','  ','  ','  ',],
            
            ['  ','  ','  ','  ','  ','  ','  ','  ',],
            
            ['  ','  ','  ','  ','  ','  ','  ','  ',],
        ]
        for figure in self.figures:
            self.board[figure.position[0]][figure.position[1]] = 'w' + figure.type if figure.is_white else 'b' + figure.type

    def render_board(self):
        print("\n+"+("------"+"+")*8,end="")
        is_odd = False
        for line in self.board:
            is_odd = not is_odd
            print("\n|", end="")
            for j in range(4):
                print("      "+"|"+"......"+"|" if is_odd else "......"+"|"+"      "+"|",end="")
            print("\n|", end="")
            for cell in line:
                print(f"  {cell}  "+"|" if is_odd else f"..{cell if cell != '  ' else '..'}.."+"|",end="")
                is_odd = not is_odd
            print("\n|", end="")
            for j in range(4):
                print("      "+"|"+"......"+"|" if is_odd else "......"+"|"+"      "+"|",end="")
            print("\n+"+("------"+"+")*8,end="")
        print()
    
    def check_posible_moves(self):
        self.posible_moves = [[],[]]
        for piece in self.figures:
            match piece.type:
                case "p":
                    pass
                case "k":
                    moves_to_check = map(lambda move: do_move(piece.position,move),knight_moves)
                    for move in moves_to_check:
                        if not border_check(move): continue
                        if any(map(lambda _piece: _piece.position == move and _piece.is_white == piece.is_white, self.figures)): continue
                        self.posible_moves[piece.is_white].append(move)
                case "b":
                    pass
                case "R":
                    pass
                case "Q":
                    pass
                case "K":
                    moves_to_check = map(lambda move: do_move(piece.position,move),queen_moves[0])
                    for move in moves_to_check:
                        if not border_check(move): continue
                        if any(map(lambda _piece: _piece.position == move and _piece.is_white == piece.is_white, self.figures)): continue
                        self.posible_moves[piece.is_white].append(move)
                    

b = board()
b.render_board()
print(b.posible_moves)