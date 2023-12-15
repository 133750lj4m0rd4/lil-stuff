from typing import Callable

#======================EXTERNAL MOVES INFO=======================

bishop_moves = [((i,i),(-i,i),(i,-i),(-i,-i),) for i in range(1,8)]
bishop_moves = tuple(bishop_moves)

rook_moves = [((i,0),(-i,0),(0,i),(0,-i),) for i in range(1,8)]
rook_moves = tuple(rook_moves)

king_moves = ((1,0),(-1,0),(0,1),(0,-1),
              (-1,1),(1,-1),(1,1),(-1,-1),)

knight_moves = [(1,2),(2,1)]
knight_moves.extend(map(lambda a: (-a[0],a[1]),knight_moves[0:len(knight_moves)]))
knight_moves.extend(map(lambda a: (a[0],-a[1]),knight_moves[0:len(knight_moves)]))
knight_moves = tuple(knight_moves)

#======================HANDY LAMBDAS=======================
#TODO maybe rework this part idk
border_check: Callable[[tuple], bool] = lambda pos: pos[0] >= 0 and pos[0] <= 7 and pos[1] >= 0 and pos[1] <= 7
do_move: Callable[[tuple, tuple], tuple] = lambda pos,move: (pos[0]+move[0], pos[1]+move[1])
nums_to_letters = ['h','g','f','e','d','c','b','a']
convert_to_chess_notation: Callable[[tuple], str] = lambda pos: f"{nums_to_letters[pos[1]]}{-pos[0]+8}"

#======================FIGURE CLASS=======================
class figure:
    def __init__(self,is_white:bool,p_type:chr,position:tuple[int]):
        self.is_white = is_white
        self.type = p_type
        self.position = position

    
    def __repr__(self):
        return("b"*(not self.is_white) + "w"*self.is_white + self.type + f" {convert_to_chess_notation(self.position)}")
    
    __str__ = __repr__

#======================BOARD CLASS=======================
class board():
    def __init__(self):
        self.pieces = {
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
            self.pieces.add(figure(True,'p',(6,i)))
            self.pieces.add(figure(False,'p',(1,i)))
            pass
        self.board = []
        self.update_board()
        self.all_possible_moves()
    
    def update_board(self):
        self.board = [['  ' for _ in range(8)] for _ in range(8)]
        for figure in self.pieces:
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
    
    #TODO automatize and optimise some stuff bc those if-s smell
    def pawn_check(self,piece: figure): #TODO rewrite stuff to optimise all the 'if' stuff
        captures = {1:((-1,1),(-1,-1)),0:((1,1),(1,-1))}
        for move in map(lambda move: do_move(piece.position,move),captures[piece.is_white]):
            if any(map(lambda _piece: _piece.position == move and 
                       _piece.is_white != piece.is_white, self.pieces)):
                self.posible_moves[piece.is_white].append((piece,move))
        if any(map(
            lambda _piece: _piece.position == do_move(piece.position,(1+(-2*piece.is_white),0)), 
            self.pieces)):
            return
        
        self.posible_moves[piece.is_white].append((piece,do_move(piece.position,(1+(-2*piece.is_white),0))))
        if any(map(
            lambda _piece: _piece.position == do_move(piece.position,(2+(-4*piece.is_white),0)), 
            self.pieces)):
            return
        
        self.posible_moves[piece.is_white].append((piece,do_move(piece.position,(2+(-4*piece.is_white),0))))

    def knight_check(self,piece: figure):
        moves_to_check = map(lambda move: do_move(piece.position,move),knight_moves)
        for move in moves_to_check:
            if not border_check(move):
                continue
            if any(map(
                lambda _piece: _piece.position == move and _piece.is_white == piece.is_white, 
                self.pieces)):
                continue
            self.posible_moves[piece.is_white].append((piece,move))
    
    def farseeing_piece_check(self,piece: figure, type: str):
        blocked_directions = [False,False,False,False]
        moves = bishop_moves if type == "b" else rook_moves
        for bracket in moves:
            for i,move in enumerate(bracket):
                move = do_move(piece.position,move)
                if blocked_directions[i]:
                    continue
                if not border_check(move):
                    blocked_directions[i] = True
                    continue
                #this 'for' is more of an 'if', and will do 1 iteration MAX
                #i am sure that it can be writtenbetter, but i haven't imagined how
                for _piece in filter(lambda _piece: _piece.position == move,self.pieces):
                    blocked_directions[i] = True
                    if _piece.is_white != piece.is_white:
                        self.posible_moves[piece.is_white].append((piece,move))
                if not blocked_directions[i]:
                    self.posible_moves[piece.is_white].append((piece,move))
            if all(blocked_directions): return

    def bishop_check(self,piece: figure):
        self.farseeing_piece_check(piece,"b")

    def rook_check(self,piece: figure):
        self.farseeing_piece_check(piece,"R")
    
    def queen_check(self,piece: figure):
        self.farseeing_piece_check(piece,"b")
        self.farseeing_piece_check(piece,"R")

    def king_check(self, piece: figure, check_check = False):
        moves_to_check = map(lambda move: do_move(piece.position,move),king_moves)
        for move in moves_to_check:
            if not border_check(move):
                continue
            if any(map(
                lambda _piece: _piece.is_white == piece.is_white and _piece.position == move, 
                self.pieces)):
                continue
            self.posible_moves[piece.is_white].append((piece,move))

    def all_possible_moves(self):
        self.posible_moves = [[],[]]
        for piece in self.pieces:
            match piece.type: #TODO match case stuff still look stinky. maybe rewrite later
                case "p": 
                    self.pawn_check(piece)
                    #pass
                case "k":
                    self.knight_check(piece)
                    #pass
                case "b":
                    self.bishop_check(piece)
                    #pass
                case "R":
                    self.rook_check(piece)
                    #pass
                case "Q":
                    self.queen_check(piece)
                    #pass
                case "K":
                    self.king_check(piece)
                    #pass

    def print_moves(self):
        print("======white======")
        for move in sorted(list(self.posible_moves[1]),key = lambda el: el[0].type):
            print(f"{move[0]} -> {convert_to_chess_notation(move[1])}")
        print("======black======")
        for move in sorted(list(self.posible_moves[0]),key = lambda el: el[0].type):
            print(f"{move[0]} -> {convert_to_chess_notation(move[1])}")
                    
#======================GAME START=======================
b = board()
b.render_board()
b.print_moves()