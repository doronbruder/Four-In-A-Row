from itertools import groupby, chain


class Game:
    """This class creates an object of the type "Game" which responsible for the logic of four in a row game"""
    COLS = 7
    ROWS = 6
    REQUIRED_TO_WIN = 4
    COLORS = ['blue','red']
    NONE = " _ "


    def __init__(self):
        """Create a new game."""
        self.cols = self.COLS
        self.rows = self.ROWS
        self.win = self.REQUIRED_TO_WIN
        self.board = [[self.NONE] * self.rows for _ in range(self.cols)]
        self.curr_turn = 0
        self.player_1_coor = []
        self.player_2_coor = []

    def make_move(self, column):
        """This method put a disc in the chosen column"""
        current_color = self.COLORS[self.curr_turn]
        self.curr_turn = (self.curr_turn+1) % 2
        c = self.board[column]
        if c[0] != self.NONE:
            raise Exception('“Illegal move.”')
        elif self.checkForWin():
            raise Exception(''"Illegal move."'')
        i = -1
        while c[i] != self.NONE:
            i -= 1
        c[i] = current_color
        self.checkForWin()

    def get_winner(self):
        """Get the winner on the current board."""
        lines = (self.board,  # columns
                 zip(*self.board),  # rows
                 self.diagonalsPos(),  # positive diagonals
                 self.diagonalsNeg()  # negative diagonals
                 )
        for line in chain(*lines):
            line = list(line)
            for color, group in groupby(line):
                if color != self.NONE and len(list(group)) >= self.win:
                    if color == 'blue':
                        return 1
                    elif color == 'red':
                        return 2

        for line in chain(*lines):
            for item in line :
                if item==self.NONE:
                    return None
        return 0

    def find_diags(self):
        """This method looks for all winning positions in the diagonals"""
        diagonals_finders=[self.find_left_down(),self.find_left_up(),self.find_right_down(),self.find_right_up()]
        for finder in diagonals_finders:
            if finder!=None:
                return finder

    def win_cor(self):
        """This method returns the first winning positions it finds"""
        win_cors=[self.find_diags(),self.find_vertical(),self.find_horizonatl()]
        for win_cor in win_cors:
            if win_cor != None:
                return win_cor
        return False

    def find_left_up(self):
        """This method looks for left up winning positions in the diagonals"""
        color = self.COLORS[(self.curr_turn - 1) % 2]
        for col in range(self.rows):
            for row in range(self.cols):
                if self.board[row][col] == color:
                    if row + 3 < 7 and col + 3 < 6:
                        # Make sure we wont  get out of board
                        if self.board[row + 1][col + 1] == color and\
                                self.board[row + 2][col + 2] == color and \
                                self.board[row + 3][col + 3] == color:
                            # Looking for left to right upping diagonals first order
                            win_cor = [[row, col], [row + 1, col + 1],
                                       [row + 2, col + 2], [row + 3, col + 3]]
                            return win_cor
    def find_right_up(self):
        """This method looks for right up winning positions in the diagonals"""
        color = self.COLORS[(self.curr_turn - 1) % 2]
        for col in range(self.rows):
            for row in range(self.cols):
                if self.board[row][col] == color:
                    if row - 3 >= 0 and col - 3 >= 0:
                        # Make sure we wont  get out of board
                        if self.board[row - 1][col - 1] == color \
                                and self.board[row - 2][col - 2] == color and \
                                self.board[row - 3][col - 3] == color:
                            # Looking for right to left upping diagonals
                            win_cor = [[row, col], [row - 1, col - 1],
                                       [row - 2, col - 2], [row - 3, col - 3]]
                            return win_cor

    def find_right_down(self):
        """This method looks for right down winning positions in the diagonals"""
        color = self.COLORS[(self.curr_turn - 1) % 2]
        for col in range(self.rows):
            for row in range(self.cols):
                if self.board[row][col] == color:
                    if 0 <= row - 3 and col + 3 < 6:
                        # Make sure we wont  get out of board
                        if self.board[row - 1][col + 1] == color and\
                                self.board[row - 2][col + 2] == color and \
                                self.board[row - 3][col + 3] == color:
                            # Looking for right to left downing diagonals f
                            win_cor = [[row, col], [row - 1, col + 1],
                                       [row - 2, col + 2], [row - 3, col + 3]]
                            return win_cor

    def find_left_down(self):
        """This method looks for left down winning positions in the diagonals"""
        color = self.COLORS[(self.curr_turn - 1) % 2]
        for col in range(self.rows):
            for row in range(self.cols):
                if self.board[row][col]==color:
                    if row + 3 < 7 and col - 3 >= 0:
                        # Make sure we wont  get out of board
                        if self.board[row + 1][col - 1] == color and\
                                self.board[row + 2][col - 2] == color and \
                                self.board[row + 3][col - 3] == color:
                            # Looking for left to right  downing diagonals
                            win_cor = [[row, col], [row + 1, col - 1],
                                       [row + 2, col - 2], [row + 3, col - 3]]
                            return win_cor

    def find_horizonatl(self):
        """This method looks for winning positions in the columns"""
        color = self.COLORS[(self.curr_turn - 1) % 2]
        for col in range(self.rows):
            for row in range(self.cols):
                if self.board[row][col] == color:
                    if col+3 < 6:
                        # Make sure we wont get  out of board
                        if (self.board[row][col+1]==color) and\
                                (self.board[row][col+2]==color)\
                                and (self.board[row][col+3]==color):
                            # Looking for horizontal win
                            win_cor = [[row, col], [row, col + 1],
                                       [row, col + 2], [row, col + 3]]
                            return win_cor
                    if col - 3 >= 0:
                        # Make sure we wont  get out of board
                        if self.board[row][col-1]==color and\
                                self.board[row][col-2]==color\
                                and self.board[row][col-3] == color:
                            # Looking for opposite order horizontal-win
                            win_cor = [[row, col], [row, col - 1],
                                       [row, col-2], [row, col-3]]
                            return win_cor

    def find_vertical(self):
        """This method looks for winning positions in the rows"""
        color = self.COLORS[(self.curr_turn - 1) % 2]
        for col in range(self.rows):
            for row in range(self.cols):
                if self.board[row][col] == color:
                    if row + 3 < 7:
                        # Make sure we wont  get out of board
                        if self.board[row + 1][col] == color and\
                                self.board[row + 2][col] == color and \
                                self.board[row + 3][col] == color:
                            # Looking for vertical-win
                            win_cor = [[row, col], [row + 1, col],
                                       [row + 2, col], [row + 3, col]]
                            return win_cor
                    if row - 3 >= 0:
                        # Make sure we wont  get out of board
                        if self.board[row - 1][col] == color and \
                                self.board[row - 2][col] == color and \
                                self.board[row - 3][col] == color:
                            # Looking for opposite order vertical win
                            win_cor = [[row, col], [row - 1, col],
                                       [row - 2, col], [row - 3, col]]
                            return win_cor

    def checkForWin(self):
        """Check the current board for a winner."""
        w = self.get_winner()
        if w:
            return True
        return False

    def get_player_at(self, row, col):
        """"Returns the location of a player who places in (col,row)"""
        if self.board[col][row]=='blue':
            return 1
        elif self.board[col][row]=='red':
            return 2


    def get_current_player(self):
        """This method return the player current turn"""
        if self.curr_turn%2==0:
            return 1
        else:
            return 2

    def diagonalsPos(self):
        """Get positive diagonals, going from bottom-left to top-right."""
        matrix=self.board
        cols=self.COLS
        rows=self.ROWS
        for di in ([(j, i - j) for j in range(rows)] for i in range(rows + cols - 1)):
            yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]

    def diagonalsNeg(self):
        """Get negative diagonals, going from top-left to bottom-right."""
        matrix = self.board
        cols = self.COLS
        rows = self.ROWS
        for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
            yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]
