from typing import List, Tuple

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
    def __init__(self, colour: int, positions: List[Tuple[int, int]], depth = 0):
        self.colour = colour
        self.positions = positions
        self.depth = depth

    def add_position(self, position: Tuple[int, int]):
        self.positions.append(position)

    def __repr__(self):
        return f"(Object colour: {colour_names[self.colour]}, positions: {self.positions}, depth: {self.depth})"
