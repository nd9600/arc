from typing import List, Tuple
from matplotlib import colors

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  # noqa

from Objects import Object  # noqa

colour_map = colors.ListedColormap(
    ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00', '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25']
)
norm = colors.Normalize(vmin = 0, vmax = 9)

class Grid:
    def __init__(self, grid: List, title: str = ""):
        self.grid = grid
        self.number_of_rows = 1 + len(self.grid)
        self.number_of_columns = 1 + len(self.grid[0])

        self.title = title

        self.objects: List["Object"] = self.parse_objects()

    def plot(self, axes = None) -> None:
        axes_not_passed_in = axes is None
        if axes_not_passed_in:
            fig, axes = plt.subplots(1, 1)

        axes.imshow(self.grid, cmap = colour_map, norm = norm)
        axes.grid(True, which = 'both', color = 'lightgrey', linewidth = 0.5)
        axes.set_yticks([x - 0.5 for x in range(self.number_of_rows)])
        axes.set_xticks([x - 0.5 for x in range(self.number_of_columns)])
        axes.set_xticklabels([])
        axes.set_yticklabels([])
        if len(self.title) > 0:
            axes.set_title(self.title)

        if axes_not_passed_in:
            plt.tight_layout()
            plt.show()

    def get_neighbourhood(self, row: int, column: int) -> List[Tuple[int, int]]:
        row_positions = [
            x
            for x in [row - 1, row, row + 1]
            if (0 <= x <= self.number_of_columns)
        ]
        column_positions = [
            y
            for y in [column - 1, column, column + 1]
            if (0 <= y <= self.number_of_rows)
        ]

        neighbourhood = [
            (x, y)
            for x in row_positions
            for y in column_positions
            if (
                (x, y) != (row, column)
            )
        ]

        return neighbourhood

    def parse_objects(self) -> List["Object"]:
        objects = []

        print(self.grid)
        for rowN, row in enumerate(self.grid):
            for colN, square in enumerate(row):
                neighbourhood = self.get_neighbourhood(rowN, colN)
                print(f"{rowN},{colN}: square {square}, neighbourhood: {neighbourhood}")

        return objects
