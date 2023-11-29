class GameBoard:
    def __init__(self, rows=6, columns=7):
        """
        Alustaa GameBoard-olion.

        Args:
            :param rows: rivien lukumäärä laudalla
            :param columns: sarakkeiden lukumäärä laudalla
        """
        self.rows = rows
        self.columns = columns
        self.board = [[' ' for _ in range(columns)] for _ in range(rows)]

    def display_board(self):
        """
        Näyttää laudan nykyisen tilan.
        """
        for row in self.board:
            print("|".join(row))
            print("-" * (self.columns * 2 - 1))
        print(" ".join(str(i + 1) for i in range(self.columns)))

    def check_valid_move(self, column):
        """
        Tarkistaa onko siirto kelvollinen.

        Args:
            :param column: sarake, johon siirto halutaan

        Returns:
            bool: True, jos siirto kelvollinen, jos ei niin False
        """

        result = 1 <= column <= self.columns \
                 and self.board[0][column - 1] == ' '
        return result

    def make_move(self, column, symbol):
        """
        Tekee siirron annetussa sarakkeessa symbolilla.

        Args:
            :param column: sarake, johon siirto tehdään
            :param symbol: symboli, joka edustaa pelaajaa

        Returns:
            bool: True jos siirto onnistuu, muuten False
        """
        if self.check_valid_move(column):
            for i in range(self.rows - 1, -1, -1):
                if self.board[i][column - 1] == ' ':
                    self.board[i][column - 1] = symbol
                    return True
        return False

    def winner_check(self, symbol):
        """
        Tarkastaa onko symbolilla pelaava voittanut

        Args:
            :param symbol: symboli X tai O, joka edustaa pelaajaa

        Returns:
            bool: True, jos pelaaja on voittanut, muuten False
        """
        # horizontal check
        for row in self.board:
            if f"{symbol * 4}" in "".join(row):
                return True

        # vertical check
        for column in range(self.columns):
            if f"{symbol * 4}" in "".join((row[column] for row in self.board)):
                return True

        # diagonal check left->right
        for i in range(self.rows - 3):
            for j in range(self.columns - 3):
                if all(self.board[i + k][j + k] == symbol for k in range(4)):
                    return True

        # diagonal check right->left
        for i in range(3, self.rows):
            for j in range(self.columns - 3):
                if all(self.board[i - k][j + k] == symbol for k in range(4)):
                    return True

        return False

    def is_board_full(self):
        """
        Tarkistaa onko lauta täynnä

        Returns:
            bool: True jos lauta täynnä, muuten False
        """
        return all(cell != ' ' for row in self.board for cell in row)

    def make_copy(self): # tee laudan kopiointi
        pass
