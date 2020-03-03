from typing import List

from src.FrameModel.Object import Object
from src.Grid.Grid import Grid

import numpy as np

from src.Types import Row


class FrameModel:
    def __init__(
        self,
        number_of_rows: int,
        number_of_columns: int,
        background_colour: int,
        objects: List[Object],
        agents: List = []
    ):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.background_colour = background_colour
        self.objects = objects
        self.agents = agents

    @staticmethod
    def create_from_grid(grid: Grid) -> "FrameModel":
        return FrameModel(
            grid.number_of_rows,
            grid.number_of_columns,
            grid.background_colour,
            grid.parse_objects(),
            []
        )

    def to_grid(self) -> Grid:
        empty_grid: List[Row] = np.full(
            [
                self.number_of_rows,
                self.number_of_columns,
            ],
            self.background_colour
        ).tolist()
        object_depths = []  # todo: take object depth into account

        grid = empty_grid
        for obj in self.objects:
            absolute_positions = Object.convert_to_absolute_positions(obj.top_left_offset, obj.relative_positions)
            for absolute_position in absolute_positions:
                grid[absolute_position[1]][absolute_position[0]] = obj.colour  # todo: use grid.set_colour
        return Grid(grid)

    def __repr__(self):
        return f"(Frame)"
