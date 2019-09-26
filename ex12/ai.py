import random


class AI:
    """
    this class create object from type AI that include:
    game - the current game
    player - the player num (1 or 2)
    the function can return the next column to put oval if the gui
     will require it
    """

    def __init__(self, game, player):
        self.__cur_game = game
        self.__cell_list = []
        self.__player = player
        self.__second_player = (player + 1) % 2

        self.WIN__DIC = {"DOWN_LEFT": [], "DOWN_RIGHT": [], "HORIZONTAL": [], "VERTICAL": []}

    def look_for_row(self, column):
        """this function receives a column and checks if there's an
        empty cell in that column"""
        for row in range(1, self.__cur_game.ROWS + 1):
            if self.__cur_game.get_player_at(self.__cur_game.ROWS - row, column) is None:
                return self.__cur_game.ROWS - row

    def find_legal_move(self, timeout=None):
        """this function looking for valid column to play
        and return her"""
        if self.__cur_game.get_winner() is not None:
            raise Exception("No possible AI moves.")
        col = random.randint(0, 6)
        row = self.look_for_row(col)
        expirence = [col]
        while row is None and len(expirence) < 7:
            col = random.randint(0, 6)
            row = self.look_for_row(col)
            expirence.append(col)
        if row is None:
            return
        return col

    def get_last_found_move(self):
        pass
