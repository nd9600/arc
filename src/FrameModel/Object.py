from typing import List, Tuple

from src.Types import AbsolutePosition, RelativePosition

colour_names = {
    0: "black",
    1: "dark blue",
    2: "red",
    3: "green",
    4: "yellow",
    5: "grey",
    6: "pink",
    7: "orange",
    8: "light blue",
    9: "purple",
}


class Object:
    def __init__(
        self,
        colour: int,
        top_left_offset: AbsolutePosition,
        relative_positions: List[RelativePosition],
        depth = 0
    ):
        assert(
            top_left_offset[0] >= 0
            and top_left_offset[1] >= 0
        )

        self.colour = colour
        self.top_left_offset = top_left_offset
        self.relative_positions: List[RelativePosition] = relative_positions
        self.depth = depth

    @staticmethod
    def create_with_absolute_positions(
        colour: int,
        absolute_positions: List[AbsolutePosition],
        depth = 0
    ):
        min_x_position = min(list(map(
            lambda pos: pos[0],
            absolute_positions
        )))
        min_y_position = min(list(map(
            lambda pos: pos[1],
            absolute_positions
        )))

        top_left_offset = (min_x_position, min_y_position)
        relative_positions: List[RelativePosition] = Object.convert_to_relative_positions(
            top_left_offset,
            absolute_positions
        )
        return Object(
            colour,
            top_left_offset,
            relative_positions,
            depth
        )

    @staticmethod
    def convert_to_relative_positions(
        top_left_offset: AbsolutePosition,
        absolute_positions: List[AbsolutePosition]
    ) -> List[RelativePosition]:
        return list(map(
            lambda absolute_position: (absolute_position[0] - top_left_offset[0], absolute_position[1] - top_left_offset[1]),
            absolute_positions
        ))

    @staticmethod
    def convert_to_absolute_positions(
            top_left_offset: AbsolutePosition,
            relative_positions: List[RelativePosition]
    ) -> List[AbsolutePosition]:
        def make_absolute_position(relative_position: RelativePosition):
            absolute_position = (top_left_offset[0] + relative_position[0], top_left_offset[1] + relative_position[1])
            if absolute_position[0] < 0:
                raise OverflowError(f"absolute x position can't be negative, {top_left_offset[0]} + {relative_position[0]}")
            if absolute_position[1] < 0:
                raise OverflowError(f"absolute y position can't be negative, {top_left_offset[1]} + {relative_position[1]}")
            return absolute_position
        return list(map(
            make_absolute_position,
            relative_positions
        ))

    def __repr__(self):
        absolute_positions = Object.convert_to_absolute_positions(self.top_left_offset, self.relative_positions)
        return f"(Object colour: {colour_names[self.colour]}, positions: {absolute_positions}, depth: {self.depth})"
