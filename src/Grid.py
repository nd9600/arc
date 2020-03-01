from typing import List, Tuple
from matplotlib import colors

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  # noqa

from collections import deque # noqa

from Objects import Object  # noqa

colour_map = colors.ListedColormap(
    ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00', '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25']
)
norm = colors.Normalize(vmin = 0, vmax = 9)


class Grid:
    def __init__(self, grid: List[List[int]], title: str = ""):
        self.grid = grid
        self.number_of_rows = len(self.grid)
        self.number_of_columns = len(self.grid[0])

        self.title = title
        # self.objects: List["Object"] = self.parse_objects()

    def plot(self, axes = None) -> None:
        axes_not_passed_in = axes is None
        if axes_not_passed_in:
            fig, axes = plt.subplots(1, 1)

        axes.imshow(self.grid, cmap = colour_map, norm = norm)
        axes.grid(True, which = 'both', color = 'lightgrey', linewidth = 0.5)
        axes.set_xticks([x - 0.5 for x in range(1 + self.number_of_columns)])
        axes.set_xticklabels([x for x in range(self.number_of_columns)])
        axes.set_xticklabels([x for x in range(self.number_of_columns)])

        axes.set_yticks([x - 0.5 for x in range(1 + self.number_of_rows)])
        axes.set_yticklabels([y for y in range(self.number_of_rows)])
        if len(self.title) > 0:
            axes.set_title(self.title)

        if axes_not_passed_in:
            plt.tight_layout()
            plt.show()

    def get_neighbourhood(self, x: int, y: int) -> List[Tuple[int, int]]:
        xs = [
            row_x
            for row_x in [x - 1, x, x + 1]
            if (0 <= row_x <= self.number_of_columns - 1)
        ]
        ys = [
            row_y
            for row_y in [y - 1, y, y + 1]
            if (0 <= row_y <= self.number_of_rows - 1)
        ]

        neighbourhood = [
            (neighbour_x, neighbour_y)
            for neighbour_x in xs
            for neighbour_y in ys
            if (
                (neighbour_x, neighbour_y) != (x, y)
            )
        ]

        return neighbourhood

    def get_colour(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def parse_objects(self) -> List["Object"]:
        objects = []

        '''
        Objects are
            * complete
            * connected
            * solid bodies
            * each square of the object has the same colour, despite noise or occlusion
        
        we loop over every square in the grid, and if it's not black:
            this will be the start of a new object - it can't be part of an existing object, we'd have processed it already
            if we've already seen it (see below), ignore it
            add it to a queue of positions we need to process for this object,
                record that we've seen it,
                add it to a list of positions that this object has
                find all the neighbouring squares that have the same colour, and for each one
                    if we've seen it already, ignore it
                    add to the "needs processing" queue
                make a new object that that has all of the above-processed position in it, and add that object to the grid's list
        '''
        seen_positions = set()
        for rowN, row in enumerate(self.grid):
            for colN, squareColour in enumerate(row):
                current_position = (colN, rowN)
                if (
                    squareColour == 0
                    or current_position in seen_positions
                ):
                    continue

                positions_for_this_object = []
                object_position_queue = deque()
                object_position_queue.append(current_position)
                while len(object_position_queue) > 0:
                    current_position = object_position_queue.pop()
                    positions_for_this_object.append(current_position)
                    seen_positions.add(current_position)

                    x = current_position[0]
                    y = current_position[1]
                    neighbourhood = self.get_neighbourhood(x, y)
                    neighbouring_squares_with_the_same_colour = list(filter(lambda pos: self.get_colour(pos[0], pos[1]) == squareColour, neighbourhood))
                    for position in neighbouring_squares_with_the_same_colour:
                        if position not in seen_positions:
                            object_position_queue.append(position)
                            seen_positions.add(position)

                unseen_object = Object.Object(squareColour, positions_for_this_object)
                objects.append(unseen_object)

        return objects
