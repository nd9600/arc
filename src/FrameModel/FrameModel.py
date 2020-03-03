from typing import List

from src.FrameModel.Object import Object
from src.Grid.Grid import Grid


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
        return Grid(

        )

    def __repr__(self):
        return f"(Frame)"
