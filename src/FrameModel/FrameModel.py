from typing import List

import numpy as np

from collections import defaultdict

from src.FrameModel.Object import Object
from src.Grid.Grid import Grid

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
        # noinspection PyTypeChecker
        empty_grid_array: List[Row] = np.full(
            [
                self.number_of_rows,
                self.number_of_columns,
            ],
            self.background_colour
        ).tolist()

        # find lowest depth, then colour all objects that have that depth, then all objects for depth above, etc.
        objects_by_depth = defaultdict(list)
        for obj in self.objects:
            objects_by_depth[obj.depth].append(obj)

        ascending_depths = list(objects_by_depth.keys())
        ascending_depths.sort()

        grid = Grid(empty_grid_array)
        for lowest_depth in ascending_depths:
            objects_for_this_depth = objects_by_depth[lowest_depth]
            for obj in objects_for_this_depth:
                absolute_positions = Object.convert_to_absolute_positions(obj.top_left_offset, obj.relative_positions)
                for absolute_position in absolute_positions:
                    grid.set_colour(absolute_position[0], absolute_position[1], obj.colour)
        return grid

    def __repr__(self):
        return f"(Frame)"
