from __future__ import annotations
from typing import Iterable, Sequence
import numpy as np

class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid = np.ndarray((9, 9))

        i = 0
        for puzzle_row in puzzle:        
            self._grid[i] = list(puzzle_row)
            i += 1

        self._grid = self._grid.astype('int')

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y][x] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        return self._grid[y][x]

    def options_at(self, x: int, y: int) -> Sequence[int]:
        """Returns all possible values (options) at x,y."""
        options = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        # Remove all values from the row
        for value in self.row_values(y):
            if value in options:
                options.remove(value)

        # Remove all values from the column
        for value in self.column_values(x):
            if value in options:
                options.remove(value)

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        for value in self.block_values(block_index):
            if value in options:
                options.remove(value)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        zeros = np.where(self._grid == 0)

        if len(zeros[0] > 0):
            next_y = zeros[0][0]
            next_x = zeros[1][0]

        return next_x, next_y

    def row_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th row."""
        return self._grid[i]

    def column_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th column."""
        return self._grid[:,i]

    def block_values(self, i: int) -> Sequence[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        return self._grid[y_start:(y_start+3), x_start:(x_start+3)].flatten()

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        for i in range(9):
            column_values = self.column_values(i)
            row_values = self.row_values(i)
            block_values = self.block_values(i)

            for j in range(9):
                if column_values[j] not in values:
                    return False
                if row_values[j] not in values:
                    return False
                if block_values[j] not in values:
                    return False

        return True

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            for number in row:
                representation += str(number)
                
            representation += "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
