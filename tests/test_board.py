import sys
from pathlib import Path

import pytest

# Ensure project root is importable when pytest is started from tests/ or elsewhere.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from board import Board


def test_board_validity_simple_positive():
    brett = Board()
    valid_board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 3, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    for r in range(9):
        for c in range(9):
            brett.add_value(r, c, valid_board[r][c])

    failed_rows = [r for r in range(9) if not brett.is_solved("row", row=r)]
    failed_cols = [c for c in range(9) if not brett.is_solved("col", col=c)]

    assert failed_rows, f"Fehlerhafte Zeilen: {failed_rows}"
    assert failed_cols, f"Fehlerhafte Spalten: {failed_cols}"


def test_board_validity_simple_negative():
    brett = Board()
    # Erstellen eines ungültigen Boards mit einem Fehler in der Zeile 7 (doppelte 3), aber 9x9
    invalid_board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 3, 4, 1, 9, 6, "X", "X"],
        [3, "X", "X", "X", "X", "X", "X", "X", "X"],
    ]

    with pytest.raises(ValueError, match="Ungültiger Wert"):
        for r in range(9):
            for c in range(9):
                brett.add_value(r, c, invalid_board[r][c])


def test_is_solved_row_raises_on_invalid_row_values():
    brett = Board()
    # 0 ist in is_solved("row") als ungültiger Wert definiert und soll ValueError werfen.
    brett.add_value(0, 0, 0)

    with pytest.raises(ValueError, match="Ungültige Werte"):
        brett.is_solved("row", row=0)


def test_is_solved_block_raises_on_invalid_block_values():
    brett = Board()
    # 0 ist in is_solved("block") als ungültiger Wert definiert und soll ValueError werfen.
    brett.add_value(0, 0, 0)

    with pytest.raises(ValueError, match="Ungültiger Wert"):
        brett.is_solved("block", row=0, col=0)


def test_is_solved_col_raises_on_invalid_col_values():
    brett = Board()
    # 0 ist in is_solved("col") als ungültiger Wert definiert und soll ValueError werfen.
    brett.add_value(0, 0, 0)

    with pytest.raises(ValueError, match="Ungültiger Wert"):
        brett.is_solved("col", col=0)


def test_is_solved_block_raises_on_missing_row_col():
    brett = Board()
    with pytest.raises(
        ValueError,
        match="Für 'block' müssen row und col angegeben werden.",
    ):
        brett.is_solved("block")


def test_is_solved_row_raises_on_missing_row():
    brett = Board()
    with pytest.raises(
        ValueError, match="Für 'row' muss ein Zeilenindex angegeben werden."
    ):
        brett.is_solved("row")


def test_is_solved_col_raises_on_missing_col():
    brett = Board()
    with pytest.raises(
        ValueError, match="Für 'col' muss ein Spaltenindex angegeben werden."
    ):
        brett.is_solved("col")


def test_is_solved_invalid_type():
    brett = Board()
    with pytest.raises(
        ValueError,
        match="Ungültiger Typ: invalid. Muss 'block', 'row' oder 'col' sein.",
    ):
        brett.is_solved("invalid")


def test_is_solved_block_with_invalid_block():
    brett = Board()
    # Erstelle ein 9x9  board mit zwei 5 im Block (0,0) und ansonsten gültigen Werten
    invalid_block_board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 5, 3, 4, 2, 5, 6, 7],  # Fehler: 5 doppelt im Block
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 3, 4, 1, 9, 6, 7, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    for r in range(9):
        for c in range(9):
            brett.add_value(r, c, invalid_block_board[r][c])
    assert not brett.is_solved("block", row=0, col=0)
