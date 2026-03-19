class Board:
    def __init__(self):
        """Initialisiert ein leeres 9x9-Sudoku-Board.

        Das Board wird als Matrix gespeichert: grid[row][col].
        Leere Felder haben den Wert 0.
        """
        self.grid = [[0 for j in range(9)] for i in range(9)]

    def __str__(self) -> str:
        """Gibt eine formatierte Textdarstellung des Boards zurück."""
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

    def __repr__(self) -> str:
        """Gibt eine kompakte Darstellung des Boards zurück."""
        return f"board({self.grid})"

    def add_value(self, row: int, col: int, value: int) -> None:
        """Setzt einen Wert in eine bestimmte Zelle.

        Args:
            row: Zeilenindex von 0 bis 8.
            col: Spaltenindex von 0 bis 8.
            value: Zellwert von 0 bis 9 (0 steht für leer).

        Raises:
            ValueError: Wenn Koordinaten oder Wert außerhalb der erlaubten Bereiche liegen.
        """
        # Validiere row, col sind im gültigen Bereich (0-8)
        if row < 0 or row >= 9 or col < 0 or col >= 9:
            raise ValueError(
                f"Ungültige Koordinaten: row={row}, col={col}. Muss zwischen 0-8 liegen."
            )
        # Validiere value ist zwischen 0-9
        if not isinstance(value, int) or value < 0 or value > 9:
            raise ValueError(
                f"Ungültiger Wert: {value}. Muss zwischen 0-9 liegen und integer sein."
            )
        self.grid[row][col] = value

    def get_col(self, col: int) -> list[int]:
        """Gibt die Werte einer Spalte als Liste zurück.

        Args:
            col: Spaltenindex von 0 bis 8.

        Raises:
            ValueError: Wenn der Spaltenindex ungültig ist.
        """
        if col < 0 or col >= 9:
            raise ValueError(f"Ungültige Spalte: col={col}. Muss zwischen 0-8 liegen.")

        column = []
        for i, row in enumerate(self.grid):
            column.append(row[col])
        return column

    def get_row(self, row: int) -> list[int]:
        """Gibt die Werte einer Zeile als Liste zurück.

        Args:
            row: Zeilenindex von 0 bis 8.

        Raises:
            ValueError: Wenn der Zeilenindex ungültig ist.
        """
        if row < 0 or row >= 9:
            raise ValueError(f"Ungültige Zeile: row={row}. Muss zwischen 0-8 liegen.")

        return self.grid[row]

    # def is_valid_move(self, row: int, col: int, value: int) -> bool:
    #     """Prüft, ob ein Wert an einer Position regelkonform gesetzt ist

    #     Ein Zug ist nur dann gültig, wenn der Wert noch nicht in derselben
    #     Zeile, Spalte oder im selben 3x3-Block vorkommt.

    #     Args:
    #         row: Zeilenindex von 0 bis 8.
    #         col: Spaltenindex von 0 bis 8.
    #         value: Zu prüfender Wert von 1 bis 9.

    #     Raises:
    #         ValueError: Wenn Koordinaten oder Wert ungültig sind.
    #     """
    #     if row < 0 or row >= 9 or col < 0 or col >= 9:
    #         raise ValueError(f"Ungültige Koordinaten: row={row}, col={col}")
    #     if not isinstance(value, int) or value < 1 or value > 9:
    #         raise ValueError(f"Ungültiger Wert: {value}. Nur Werte 1-9 erlaubt.")

    #     # Wert darf nicht schon in gleicher Zelle sein
    #     if self.grid[row][col] != 0 and self.grid[row][col] != value:
    #         return False
    #     # Wert darf nicht schon in gleicher Reihe sein
    #     if value in self.get_row(row):
    #         return False
    #     # Wert darf nicht schon in gleicher Spalte sein
    #     if value in self.get_col(col):
    #         return False
    #     # Wert darf nicht schon im Block sein
    #     if value in self.get_block(row, col):
    #         return False
    #     return True

    def get_block(self, row: int, col: int) -> list[int]:
        """Gibt den 3x3-Block einer Position als flache Liste zurück.

        Args:
            row: Zeilenindex von 0 bis 8.
            col: Spaltenindex von 0 bis 8.

        Raises:
            ValueError: Wenn Koordinaten ungültig sind.
        """
        if row < 0 or row >= 9 or col < 0 or col >= 9:
            raise ValueError(f"Ungültige Koordinaten: row={row}, col={col}")

        # Finde zunächst obere linke Ecke des Blocks
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        current_block = []  # Liste, die die Werte des Blocks enthält
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                current_block.append(self.grid[r][c])
        return current_block

    def is_solved(
        self, typ: str, row: int | None = None, col: int | None = None
    ) -> bool:
        """Prüft, ob eine Zeile, Spalte oder ein Block vollständig gelöst ist.

        Args:
            typ: Art der Prüfung: "block", "row" oder "col".
            row: Zeilenindex für "row" oder "block".
            col: Spaltenindex für "col" oder "block".

        Returns:
            True, wenn der gewählte Bereich die Zahlen 1-9 genau einmal enthält,
            sonst False.
        """
        if typ not in ("block", "row", "col"):
            raise ValueError(
                f"Ungültiger Typ: {typ}. Muss 'block', 'row' oder 'col' sein."
            )
        if typ == "block":
            if row is None or col is None:
                raise ValueError("Für 'block' müssen row und col angegeben werden.")
            check = self.get_block(row, col)

            # ueberprüfe, ob alle Werte zwischen 1-9 liegen (kein 0)
            invalid = next((x for x in check if x < 1 or x > 9), None)
            if invalid is not None:
                raise ValueError(
                    f"Ungültiger Wert {invalid} im Block: {self.get_block(row, col)}"
                )
            if len(set(check)) != 9:
                return False
            else:
                if 0 in check:
                    return False
                else:
                    return True
        elif typ == "row":
            if row is None:
                raise ValueError("Für 'row' muss ein Zeilenindex angegeben werden.")
            check = self.get_row(row)
            invalid = next((x for x in check if x < 1 or x > 9), None)
            if any(x < 1 or x > 9 for x in check):
                raise ValueError(f"Ungültige Werte {invalid} in der Zeile {row}")
            if len(set(check)) != 9:
                return False
            else:
                if 0 in check:
                    return False
                else:
                    return True
        elif typ == "col":
            if col is None:
                raise ValueError("Für 'col' muss ein Spaltenindex angegeben werden.")
            check = self.get_col(col)
            invalid = next((x for x in check if x < 1 or x > 9), None)
            if invalid is not None:
                raise ValueError(f"Ungültiger Wert {invalid} in der Spalte: {col}")

            if len(set(check)) != 9:
                return False
            else:
                if 0 in check:
                    return False
                else:
                    return True


if __name__ == "__main__":
    brett = Board()
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
