from typing import Callable

#======================EXTERNAL MOVES INFO=======================

bishop_offsets = [((i,i),(-i,i),(i,-i),(-i,-i),) for i in range(1,7)]
bishop_offsets = tuple(bishop_offsets)

rook_offsets = [((i,0),(-i,0),(0,i),(0,-i),) for i in range(1,7)]
rook_offsets = tuple(rook_offsets)

king_offsets = ((1,0),(-1,0),(0,1),(0,-1),
              (-1,1),(1,-1),(1,1),(-1,-1),)

knight_offsets = ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1),)

#======================HANDY LAMBDAS=======================
#TODO maybe rework this part idk
is_on_board: Callable[[tuple], bool] = lambda pos: pos[0] >= 0 and pos[0] <= 7 and pos[1] >= 0 and pos[1] <= 7
do_move: Callable[[tuple, tuple], tuple] = lambda pos,move: (pos[0]+move[0], pos[1]+move[1])
files = ['a','b','c','d','e','f','g','h']
format_position_to_chess_notation: Callable[[tuple], str] = lambda pos: f"{files[pos[1]]}{-pos[0]+8}"

#======================PIECE CLASS=======================
class Piece:
    def __init__(self,is_white:bool,p_type:chr,position:tuple[int]):
        self.is_white = is_white
        self.type = p_type
        self.position = position
    
    def __repr__(self):
        return("b"*(not self.is_white) + "w"*self.is_white + self.type + f" {format_position_to_chess_notation(self.position)}")
    
    __str__ = __repr__

#======================BOARD CLASS=======================
class Board():
    def __init__(self):
        self.pieces = {
            Piece(False,'R',(0,0)),
            Piece(False,'k',(0,1)),
            Piece(False,'b',(0,2)),
            Piece(False,'Q',(0,3)),
            Piece(False,'K',(0,4)),
            Piece(False,'b',(0,5)),
            Piece(False,'k',(0,6)),
            Piece(False,'R',(0,7)),
            
            Piece(True,'R',(7,0)),
            Piece(True,'k',(7,1)),
            Piece(True,'b',(7,2)),
            Piece(True,'Q',(7,3)),
            Piece(True,'K',(7,4)),
            Piece(True,'b',(7,5)),
            Piece(True,'k',(7,6)),
            Piece(True,'R',(7,7)),
        }
        for i in range(8):
            self.pieces.add(Piece(True,'p',(6,i)))
            self.pieces.add(Piece(False,'p',(1,i)))
            pass
        self.Board = []

        self.last_move = None

        self.b_occupied = set()
        self.w_occupied = set()
        self.occupied = set()
        
        self.update_Board()
        self.find_occupied()
        self.all_possible_moves()
    
    def find_occupied(self):
        un_ifyer = [self.b_occupied,self.w_occupied]
        for piece in self.pieces:
            un_ifyer[piece.is_white].add(piece.position)
        self.occupied.update(self.w_occupied)
        self.occupied.update(self.b_occupied)

    def update_Board(self):
        self.Board = [['  ' for _ in range(8)] for _ in range(8)]
        for piece in self.pieces:
            self.Board[piece.position[0]][piece.position[1]] = 'w' + piece.type if piece.is_white else 'b' + piece.type

    def render_Board(self):
        out = "\n  |"
        for letter in files:
            out += f"  {letter}   "+"|"    
        out += "\n--+"+("------"+"+")*8
        is_odd = False
        for i,line in enumerate(self.Board):
            is_odd = not is_odd
            out += "\n  |"
            for j in range(4):
                out += "      "+"|"+"......"+"|" if is_odd else "......"+"|"+"      "+"|"
            out += f"\n{8 - i} |"
            for cell in line:
                out += f"  {cell}  "+"|" if is_odd else f"..{cell if cell != '  ' else '..'}.."+"|"
                is_odd = not is_odd
            out += "\n  |"
            for j in range(4):
                out += "      "+"|"+"......"+"|" if is_odd else "......"+"|"+"      "+"|"
            out += "\n--+"+("------"+"+")*8
        print(out)
    
    def pawn_check(self,piece: Piece): #TODO maybe improve later
        captures = {1:((-1,1),(-1,-1)),0:((1,1),(1,-1))}
        un_ifyer = [self.b_occupied,self.w_occupied]
        for move in map(lambda move: do_move(piece.position,move),captures[piece.is_white]):
            if (move in un_ifyer[not piece.is_white]):
                self.posible_moves[piece.is_white].append((piece,move))
        
        move = do_move(piece.position,(1+(-2*piece.is_white),0))
        if (move in self.occupied or not is_on_board(move)):
            return
        self.posible_moves[piece.is_white].append((piece,move))
        
        move = do_move(piece.position,(2+(-4*piece.is_white),0))
        if (move in self.occupied or piece.position[0] != [1,6][piece.is_white]):
            return
        self.posible_moves[piece.is_white].append((piece,move))

    def knight_check(self,piece: Piece):
        moves_to_check = map(lambda move: do_move(piece.position,move),knight_offsets)
        un_ifyer = [self.b_occupied,self.w_occupied]
        for move in moves_to_check:
            if not is_on_board(move):
                continue
            if (move in un_ifyer[piece.is_white]):
                continue
            self.posible_moves[piece.is_white].append((piece,move))
    
    def farseeing_piece_check(self,piece: Piece, type: str):
        blocked_directions = [False,False,False,False]
        moves = bishop_offsets if type == "b" else rook_offsets
        un_ifyer = [self.b_occupied,self.w_occupied]
        for bracket in moves:
            for i,move in enumerate(bracket):
                move = do_move(piece.position,move)
                if blocked_directions[i]:
                    continue
                if not is_on_board(move):
                    blocked_directions[i] = True
                    continue
                if (move in self.occupied): 
                    blocked_directions[i] = True
                    if (move in un_ifyer[piece.is_white]):
                        continue
                self.posible_moves[piece.is_white].append((piece,move))
            if all(blocked_directions): return

    def bishop_check(self,piece: Piece):
        self.farseeing_piece_check(piece,"b")

    def rook_check(self,piece: Piece):
        self.farseeing_piece_check(piece,"R")
    
    def queen_check(self,piece: Piece):
        self.farseeing_piece_check(piece,"b")
        self.farseeing_piece_check(piece,"R")

    def king_check(self, piece: Piece, check_check = False):
        moves_to_check = map(lambda move: do_move(piece.position,move),king_offsets)
        for move in moves_to_check:
            if not is_on_board(move):
                continue
            if (move not in self.occupied):
                self.posible_moves[piece.is_white].append((piece,move))

    def all_possible_moves(self):
        #TODO add un pasant and castling check
        # also add check and checkmate stuff, but it's not as important
        self.posible_moves = [[],[]]
        for piece in self.pieces:
            match piece.type: #TODO match case stuff still look stinky. maybe rewrite later
                case "p": 
                    self.pawn_check(piece)
                case "k":
                    self.knight_check(piece)
                case "b":
                    self.bishop_check(piece)
                case "R":
                    self.rook_check(piece)
                case "Q":
                    self.queen_check(piece)
                case "K":
                    self.king_check(piece)
    
    def make_move(self,move):#TODO add last move interaction for future un passant logic
        piece = move[0]
        move = move[1]
        un_ifyer:list[set,set] = [self.b_occupied,self.w_occupied]

        if move in un_ifyer[not piece.is_white]:
            self.pieces.discard(list(filter(lambda p: p.position == move,self.pieces))[0])
            un_ifyer[not piece.is_white].remove(move)
        
        self.occupied.remove(piece.position)
        un_ifyer[piece.is_white].remove(piece.position)
        piece.position = move
        un_ifyer[piece.is_white].add(piece.position)
        self.occupied.add(piece.position)
        
        self.update_Board()
        self.all_possible_moves()

    def move_choise(self,moves):
        def invalid_input():
            print("invalid input!")
            return self.move_choise(moves)
        
        for i,move in enumerate(moves):
            print(f"{i}){move[0]} -> {format_position_to_chess_notation(move[1])}", end = '\t')
            if i%3 == 2: print()

        choise_type = input("\nyou want to choose an index or a piece type? (i/pt):")
        match choise_type:
            case 'i':
                try: self.make_move(moves[int(input("input index:"))])
                except: invalid_input()
            case 'pt':
                piece_type = input("piece_type:")
                if piece_type not in ['p','k','b','R','Q','K',]: invalid_input()
                return self.move_choise(list(filter(lambda e: e[0].type == piece_type,moves)))
            case _:
                invalid_input()

    def gameplay_loop(self):
        while True:
            for whiteness in [1,0]:
                self.render_Board()
                print("======white======" if whiteness else "======black======")
                self.move_choise(self.posible_moves[whiteness])

    def print_moves(self):
        print("======white======")
        for move in sorted(self.posible_moves[1],key = lambda el: el[0].type):
            print(f"{move[0]} -> {format_position_to_chess_notation(move[1])}")
        print("======black======")
        for move in sorted(self.posible_moves[0],key = lambda el: el[0].type):
            print(f"{move[0]} -> {format_position_to_chess_notation(move[1])}")
                    
#======================GAME START=======================
b = Board()
b.gameplay_loop()