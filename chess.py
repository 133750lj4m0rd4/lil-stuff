#======================EXTERNAL MOVES INFO=======================
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

#======================HANDY LAMBDAS=======================
#TODO maybe rework this part idk
border_check = lambda pos: pos[0] >= 0 and pos[0] <= 7 and pos[1] >= 0 and pos[1] <= 7
do_move = lambda pos,move: (pos[0]+move[0], pos[1]+move[1])
nums_to_letters = ['h','g','f','e','d','c','b','a']
convert_to_chess_notation = lambda pos: f"{nums_to_letters[pos[1]]}{-pos[0]+8}"

#======================FIGURE CLASS=======================
class figure:
    def __init__(self,is_white:bool,p_type:chr,position:tuple[int]):
        self.is_white = is_white
        self.type = p_type
        self.position = position
    
    def posible_moves(self):
        match self.type:
            case 'p':
                return pawn_moves(self)
    
    def __repr__(self):
        return("b"*(not self.is_white) + "w"*self.is_white + self.type + f" {convert_to_chess_notation(self.position)}")
    
    __str__ = __repr__

#======================BOARD CLASS=======================
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
            
            figure(True,'R',(7,0)),
            figure(True,'k',(7,1)),
            figure(True,'b',(7,2)),
            figure(True,'Q',(7,3)),
            figure(True,'K',(7,4)),
            figure(True,'b',(7,5)),
            figure(True,'k',(7,6)),
            figure(True,'R',(7,7)),
        }
        for i in range(8):
            self.figures.add(figure(True,'p',(6,i)))
            self.figures.add(figure(False,'p',(1,i)))
            #pass
        self.board = []
        self.update_board()
        self.check_posible_moves()
    
    def update_board(self):
        self.board = [['  ' for _ in range(8)] for _ in range(8)]
        for figure in self.figures:
            self.board[figure.position[0]][figure.position[1]] = 'w' + figure.type if figure.is_white else 'b' + figure.type

    def render_board(self):
        out = ""
        out += "\n+"+("------"+"+")*8
        is_odd = False
        for line in self.board:
            is_odd = not is_odd
            out += "\n|"
            for j in range(4):
                out += "      "+"|"+"......"+"|" if is_odd else "......"+"|"+"      "+"|"
            out += "\n|"
            for cell in line:
                out += f"  {cell}  "+"|" if is_odd else f"..{cell if cell != '  ' else '..'}.."+"|"
                is_odd = not is_odd
            out += "\n|"
            for j in range(4):
                out += "      "+"|"+"......"+"|" if is_odd else "......"+"|"+"      "+"|"
            out += "\n+"+("------"+"+")*8
        print(out)
    
    def check_posible_moves(self):
        self.posible_moves = [[],[]]
        #TODO decompose this shit. it's stinks
        for piece in self.figures:
            match piece.type:
                case "p": #TODO add capture logic
                    moves_to_check = map(lambda move: do_move(piece.position,move),pawn_moves(piece))
                    for move in moves_to_check:
                        if not border_check(move):
                            continue
                        if any(map(lambda _piece: _piece.position == move and _piece.is_white == piece.is_white, self.figures)):
                            continue
                        self.posible_moves[piece.is_white].append((piece,move))
                case "k":
                    moves_to_check = map(lambda move: do_move(piece.position,move),knight_moves)
                    for move in moves_to_check:
                        if not border_check(move):
                            continue
                        if any(map(lambda _piece: _piece.position == move and _piece.is_white == piece.is_white, self.figures)):
                            continue
                        self.posible_moves[piece.is_white].append((piece,move))
                case "b":
                    pass #TODO add logik and stuff
                case "R":
                    pass #TODO add logik and stuff
                case "Q":
                    pass #TODO add logik and stuff
                case "K":
                    moves_to_check = map(lambda move: do_move(piece.position,move),queen_moves[0])
                    for move in moves_to_check:
                        if not border_check(move):
                            continue
                        if any(map(lambda _piece: _piece.position == move and _piece.is_white == piece.is_white, self.figures)):
                            continue
                        self.posible_moves[piece.is_white].append((piece,move))

    def print_moves(self):
        print("======white======")
        for move in self.posible_moves[1]:
            print(f"{move[0]} -> {convert_to_chess_notation(move[1])}")
        print("======black======")
        for move in self.posible_moves[0]:
            print(f"{move[0]} -> {convert_to_chess_notation(move[1])}")
                    
#======================GAME START=======================
b = board()
b.render_board()
b.print_moves()