class Agent:
    MIN_VALUE = -1000000
    MAX_VALUE = 1000000

    def __init__(self, game, color, max_depth):
        self.game = game
        self.color = color
        self.max_depth = max_depth
        self.hashTable = {}  # hash table

    def do_min_max(self, current_board):
        # checking board in hash table
        board_str = self.board_to_str(current_board.game_board)
        if board_str in self.hashTable.keys():
            move = self.hashTable[board_str]
        else:
            move, value = self.max(current_board, self.color, 0)
            self.hashTable[board_str] = move
        # print('************************')
        return move

    def max(self, current_board, current_color, depth):

        if self.game.check_terminal(current_board, current_color) or depth == self.max_depth:
            return None, self.game.evaluate(current_board, current_color)

        all_possible_moves = self.game.generate_all_possible_moves(current_board, current_color)
        best_move = None
        min_value = self.MIN_VALUE
        for move in all_possible_moves:
            no_move, value = self.min(current_board.next_board(current_color, move),
                                      self.game.opponent(current_color),
                                      depth + 1)
            if value > min_value:
                min_value = value
                best_move = move
        return best_move, min_value

    def min(self, current_board, current_color, depth):
        if self.game.check_terminal(current_board, current_color) or depth == self.max_depth:
            return None, self.game.evaluate(current_board, current_color)

        all_possible_moves = self.game.generate_all_possible_moves(current_board, current_color)
        best_move = None
        max_value = self.MAX_VALUE
        for move in all_possible_moves:
            no_move, value = self.max(current_board.next_board(current_color, move),
                                      self.game.opponent(current_color),
                                      depth + 1)
            if value < max_value:
                max_value = value
                best_move = move
        return best_move, max_value

    def board_to_str(self, board):
        str = '#'
        for row in board:
            for tile in row:
                str += f'{tile.piece}'
                str += '#'
            str += '\n'
            str += '#'

        return str
