class board:
    def __init__(self):
        """
        Erstelle ein board
        grid[row][col]
        """
        self.grid = [[0 for j in range(9)] for i in range(9)]

    def add_value(self, row, col, value):
        """
        Füge in Zeile row und spalte col einen Wert value ein.
        """
        if type(value) != int or value < 0 or value > 9:
            raise ValueError("Ungültiger Wert: " + str(value))
        self.grid[row][col] = value

    def get_col(self, col):
        column = []
        for i, row in enumerate(self.grid):
            column.append(row[col])
        return column

    def get_row(self, row):
        return self.grid[row]

    def get_block(self, row, col):
        """
        Gibt den gesamten Block zurück, anhand der Koordinaten im Grid
        :row: Zeile
        :col: Spalte
        """
        # Finde zunächst obere linke Ecke des Blocks
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        current_block = []  # Liste, die die Werte des Blocks enthält
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                current_block.append(self.grid[r][c])
        return current_block

    def __str__(self):
        output = ""
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                output += str(val) + " "
                # Trenner einfuegen
                if (j + 1) % 3 == 0 and j != 8:
                    output += " | "
            output += "\n"
            # Trenner einfuegen
            if (i + 1) % 3 == 0 and i != 8:
                output += "-------+--------+------- \n"
        return output

    def is_solved(self, typ: str, row=None, col=None):
        """
        :typ: definiert ob Block, Reihe oder Spalte [block, row, col]
        :i: Welche row
        :j: welche col
        """

        if typ == "block":
            check = self.get_block(row, col)
            # ueberprüfe, ob alle Werte von 1-9 vorhanden sind
            if any(x < 0 and x > 10 for x in check):
                raise ValueError("Ungültige Werte im Block")
            if len(set(check)) != 9:
                return False
            else:
                if 0 in check:
                    return False
                else:
                    return True
        elif typ == "row":
            check = self.get_row(row)
            if len(set(check)) != 9:
                return False
            else:
                if 0 in check:
                    return False
                else:
                    return True
        elif typ == "col":
            check = self.get_col(col)
            if len(set(check)) != 9:
                return False
            else:
                if 0 in check:
                    return False
                else:
                    return True


if __name__ == "__main__":
    brett = board()
    brett.add_value(2, 2, 5)
    brett.add_value(7, 2, 4)
    brett.add_value(0, 0, 5)
    brett.add_value(0, 1, 3)
    brett.add_value(1, 0, 6)
    brett.add_value(1, 3, 1)
    brett.add_value(1, 4, 9)
    brett.add_value(1, 5, 5)
    brett.add_value(2, 1, 9)
    brett.add_value(2, 2, 8)

    print(brett)
    print(brett.get_col(2))
    print(brett.get_row(7))
    print(brett.get_block(1, 1))
