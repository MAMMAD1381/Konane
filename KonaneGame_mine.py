from PlayKonane import PlayKonane
from Tile import Tile


class KonaneGame_mine:
    def __init__(self):
        NotImplemented

    def initialize_board(self, board_size):
        board = []
        tile = Tile(2, 0, 0, 0)
        for i in range(board_size):
            row_gui = []
            for j in range(board_size):
                row_gui.append(tile)
                tile = Tile(3 - tile.piece, tile.outline, i, j + 1)
            board.append(row_gui)
            if board_size % 2 == 0:
                tile = Tile(3 - tile.piece, tile.outline, i + 1, 0)

        return board

    def generate_all_possible_moves(self, board, player):
        """
        Generates and returns all legal moves for the given player using the
        current board configuration.
        """
        if board.is_opening_move():
            if player == Tile.P_Black:
                return self.generate_first_moves(board)
            else:
                return self.generate_second_moves(board)
        else:
            moves = []
            rd = [-1, 0, 1, 0]
            cd = [0, 1, 0, -1]
            for r in range(board.size):
                for c in range(board.size):
                    if board.game_board[r][c].piece == player:
                        for i in range(len(rd)):
                            moves += self.check(board, r, c, rd[i], cd[i], 1,
                                                self.opponent(player))
            return moves

    def generate_first_moves(self, board):
        """
        Returns the special cases for the first move of the game.
        """
        moves = []
        moves.append([0] * 4)
        moves.append([board.size - 1] * 4)
        moves.append([board.size // 2] * 4)
        moves.append([(board.size // 2) - 1] * 4)
        return moves

    def generate_second_moves(self, board):
        """
        Returns the special cases for the second move of the game, based
        on where the first move occurred.
        """
        moves = []
        if board.game_board[0][0].piece == Tile.P_NONE:
            moves.append([0, 1] * 2)
            moves.append([1, 0] * 2)
            return moves
        elif board.game_board[board.size - 1][board.size - 1].piece == Tile.P_NONE:
            moves.append([board.size - 1, board.size - 2] * 2)
            moves.append([board.size - 2, board.size - 1] * 2)
            return moves
        elif board.game_board[board.size // 2 - 1][board.size // 2 - 1].piece == Tile.P_NONE:
            pos = board.size // 2 - 1
        else:
            pos = board.size // 2
        moves.append([pos, pos - 1] * 2)
        moves.append([pos + 1, pos] * 2)
        moves.append([pos, pos + 1] * 2)
        moves.append([pos - 1, pos] * 2)
        return moves

    def check(self, board, r, c, rd, cd, factor, opponent):
        """
        Checks whether a jump is possible starting at (r,c) and going in the
        direction determined by the row delta (rd), and the column delta (cd).
        The factor is used to recursively check for multiple jumps in the same
        direction.  Returns all possible jumps in the given direction.
        """
        if board.contains(r + factor * rd, c + factor * cd, opponent) and \
                board.contains(r + (factor + 1) * rd, c + (factor + 1) * cd, Tile.P_NONE):
            return [[r, c, r + (factor + 1) * rd, c + (factor + 1) * cd]] + \
                self.check(board, r, c, rd, cd, factor + 2, opponent)
        else:
            return []

    def get_moves_at_tile(self, board, tile, player):
        moves = self.generate_all_possible_moves(board, player)
        valid_moves_at_tile = []
        # print(moves)
        for move in moves:
            if move[0] == tile.row and move[1] == tile.col:
                valid_tile = board.game_board[move[2]][move[3]]
                valid_moves_at_tile.append(valid_tile)
        return valid_moves_at_tile

    def find_winner(self, board, color):
        valid_moves = self.generate_all_possible_moves(board, color)

        if valid_moves == []:
            winner = (Tile.P_Black if color == Tile.P_White else Tile.P_White)
            return winner

    def check_terminal(self, board, color):

        valid_moves = self.generate_all_possible_moves(board, color)
        return True if valid_moves == [] else False

    def opponent(self, tile):
        """
        Given a player symbol, returns the opponent's symbol, 'B' for black,
        or 'W' for white.  (3 - color)
        """
        return Tile.P_Black if tile == Tile.P_White else Tile.P_White

    def evaluate(self, board, color, terminal_value=0):

        value = 0
        #### given evaluate function:
        # valid_moves_color = self.generate_all_possible_moves(board, color)
        # valid_moves_opponent = self.generate_all_possible_moves(board, self.opponent(color))
        #
        # value += (10 * len(valid_moves_color))
        # value -= (10 * len(valid_moves_opponent))

        #### my evaluate function:
        value += terminal_value
        black = 0
        white = 0
        for row in board.game_board:  # calculating number of black and white pieces in board
            for tile in row:
                if tile.piece == 1:
                    white += 1
                elif tile.piece == 2:
                    black += 1

        if black == 0 and white == 0:  # game is finished
            return 0
        if (black == 0 and white > 0 and color == 1) or (
                white == 0 and black > 0 and color == 2):  # opponent has no tiles left
            return 1000

        difference = abs(black - white)

        if (color == 1 and white > black) or (color == 2 and black > white):
            value += difference * 2

        if (white >= black and color == 1) or (white <= black and color == 2):  # white turn and more tiles than black
            value += (10 * difference)
        else:
            value -= (10 * difference)

        black_possible_moves = len(self.generate_all_possible_moves(board, 2))
        white_possible_moves = len(self.generate_all_possible_moves(board, 1))

        difference_possible_moves = abs(black_possible_moves - white_possible_moves)

        if (color == 1 and white_possible_moves > black_possible_moves) or (
                color == 2 and white_possible_moves < black_possible_moves):
            value += (10 * difference_possible_moves)

        black_corner = 0
        white_corner = 0
        row_counter = 0
        col_counter = 0
        for row in board.game_board:
            for tile in row:
                if row_counter == 0 and col_counter == 0:
                    if tile.piece == 1:
                        white_corner += 1
                    elif tile.piece == 2:
                        black_corner += 1
                if row_counter == 0 and col_counter == 5:
                    if tile.piece == 1:
                        white_corner += 1
                    elif tile.piece == 2:
                        black_corner += 1
                if row_counter == 5 and col_counter == 0:
                    if tile.piece == 1:
                        white_corner += 1
                    elif tile.piece == 2:
                        black_corner += 1
                if row_counter == 5 and col_counter == 5:
                    if tile.piece == 1:
                        white_corner += 1
                    elif tile.piece == 2:
                        black_corner += 1
                col_counter += 1
            row_counter += 1
        difference_corners = abs(black_corner - white_corner)
        if (black_corner > white_corner and color == 2) or (black_corner < white_corner and color == 1):
            value += (20 * difference_corners)

        return value
