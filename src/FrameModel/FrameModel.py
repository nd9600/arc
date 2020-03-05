from collections import defaultdict
from typing import List, Dict, Union

import numpy as np

import src.Runtime.ObjectRuntime
from src.FrameModel.Object import Object
from src.Grid.Grid import Grid
from src.Types import Row, ObjectId, ObjectKind


class FrameModel:
    def __init__(
        self,
        number_of_rows: int,
        number_of_columns: int,
        background_colour: int,
        objects: Union[List[Object], Dict[int, Object]],
        agents: List = []
    ):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.background_colour = background_colour
        self.objects = {obj.id: obj for obj in objects} if (isinstance(objects, list)) else objects
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
        # noinspection PyTypeChecker
        objects_by_depth: Dict[int, List[Object]] = defaultdict(list)
        for obj in self.objects.values():
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

    def group_same_objects(self) -> Dict[ObjectKind, List[ObjectId]]:
        grouped_objects: Dict[ObjectKind, List[ObjectId]] = defaultdict(list)

        ungrouped_objects = list(self.objects.values())
        obj_a_index = 0
        while True:
            # we don't need to explicitly compare the last object,
            # it'll have already been compared to every other object
            current_object_is_last_object = (
                obj_a_index > 0  # it always needs to group the first object
                and obj_a_index >= len(ungrouped_objects) - 1
            )
            if current_object_is_last_object:
                break

            obj_a = ungrouped_objects[obj_a_index]

            # if an object is already been grouped, any other objects it's the same as will have been grouped too,
            # so we don't need to compare it
            if obj_a.id in grouped_objects.values():
                obj_a_index = obj_a_index + 1
                continue

            obj_kind = obj_a.get_object_kind()
            grouped_objects[obj_kind].append(obj_a.id)

            for obj_b_index in range(obj_a_index + 1, len(ungrouped_objects)):
                obj_b = ungrouped_objects[obj_b_index]
                if src.Runtime.ObjectRuntime.objects_are_the_same(obj_a, obj_b):
                    grouped_objects[obj_kind].append(obj_b.id)
            obj_a_index = obj_a_index + 1
        return dict(grouped_objects)

    def __repr__(self):
        return f"(Frame)"
