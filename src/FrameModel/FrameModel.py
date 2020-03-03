from typing import List

from src.FrameModel.Object import Object
from src.Grid import Grid


class Frame:
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
    def createFromGrid(grid: Grid) -> "Frame":
        return Frame(
            grid.number_of_rows,
            grid.number_of_columns,
            grid.background_colour,
            grid.parse_objects(),
            []
        )

    def __repr__(self):
        return f"(Frame)"
