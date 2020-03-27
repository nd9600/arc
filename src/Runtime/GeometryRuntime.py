import math
from collections import deque
from functools import partial
from typing import Tuple, Deque, Set, List

import src.FrameModel.FrameModel
import src.FrameModel.Object as Object
from src.Types import AbsolutePosition


def rotate_object_about_point(
    obj: Object.Object,
    angle: int,
    about_point: Tuple[int, int],
    is_relative_rotation: bool = True
) -> Object.Object:
    def rotate(point: Tuple[int, int], radian_angle: float, origin: Tuple[int, int]):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(radian_angle) * (px - ox) - math.sin(radian_angle) * (py - oy)
        qy = oy + math.sin(radian_angle) * (px - ox) + math.cos(radian_angle) * (py - oy)
        # we need to round them because we'd return stuff like (6.123233995736766e-17, 1.0) otherwise
        return round(qx), round(qy)

    angle_in_radians = (angle) * math.pi/180

    if is_relative_rotation:
        rotated_relative_positions = list(map(
            lambda pos: rotate(pos, angle_in_radians, about_point),
            obj.relative_positions
        ))

        # if any of the rotated_relative_positions contain a negative int,
        # we need to move the top left offset so that they're all >= 0, and recalculate all the relative positions
        min_x_offset = min(list(map(
            lambda pos: pos[0],
            rotated_relative_positions
        )))
        min_y_offset = min(list(map(
            lambda pos: pos[1],
            rotated_relative_positions
        )))
        top_left_offset_after_rotation = obj.top_left_offset
        if min_x_offset < 0:
            rotated_relative_positions = list(map(
                lambda pos: (pos[0] + abs(min_x_offset), pos[1]),
                rotated_relative_positions
            ))
            top_left_offset_after_rotation = (top_left_offset_after_rotation[0] + min_x_offset, top_left_offset_after_rotation[1])

        if min_y_offset < 0:
            rotated_relative_positions = list(map(
                lambda pos: (pos[0], pos[1] + abs(min_y_offset)),
                rotated_relative_positions
            ))
            top_left_offset_after_rotation = (top_left_offset_after_rotation[0], top_left_offset_after_rotation[1] + min_y_offset)

        top_left_offset_after_rotation = (
            max(top_left_offset_after_rotation[0], 0),
            max(top_left_offset_after_rotation[1], 0)
        )
        # todo: move the tl offset if (it + max obj offset) is > grid size, too

        return Object.Object(
            obj.colour,
            top_left_offset_after_rotation,
            rotated_relative_positions,
            obj.depth
        )
    else:
        rotated_absolute_positions = list(map(
            lambda pos: rotate(pos, angle_in_radians, about_point),
            obj.convert_to_absolute_positions()
        ))

        # if any of the rotated_absolute_positions contain a negative int,
        # we need to move them all so that they're all >= 0
        min_x_offset = min(list(map(
            lambda pos: pos[0],
            rotated_absolute_positions
        )))
        min_y_offset = min(list(map(
            lambda pos: pos[1],
            rotated_absolute_positions
        )))
        if min_x_offset < 0:
            rotated_absolute_positions = list(map(
                lambda pos: (pos[0] + abs(min_x_offset), pos[1]),
                rotated_absolute_positions
            ))

        if min_y_offset < 0:
            rotated_absolute_positions = list(map(
                lambda pos: (pos[0], pos[1] + abs(min_y_offset)),
                rotated_absolute_positions
            ))

        return Object.Object.create_with_absolute_positions(
            obj.colour,
            rotated_absolute_positions,
            obj.depth
        )


def relatively_rotate_object(angle: int, obj: Object.Object) -> Object.Object:
    return rotate_object_about_point(obj, angle, (0, 0))


def absolutely_rotate_object(angle: int, about_point: AbsolutePosition, obj: Object.Object) -> Object.Object:
    return rotate_object_about_point(obj, angle, about_point, False)


relatively_rotate_object_90 = partial(relatively_rotate_object, 90)
relatively_rotate_object_180 = partial(relatively_rotate_object, 180)
relatively_rotate_object_270 = partial(relatively_rotate_object, 270)

absolutely_rotate_object_90 = partial(absolutely_rotate_object, 90)
absolutely_rotate_object_180 = partial(absolutely_rotate_object, 180)
absolutely_rotate_object_270 = partial(absolutely_rotate_object, 270)


def is_point_fully_enclosed(
    point: AbsolutePosition,
    frame_model: "src.FrameModel.FrameModel.FrameModel"
) -> bool:
    if (
        point[0] < 0 or point[0] >= frame_model.number_of_columns
        or point[1] < 0 or point[1] >= frame_model.number_of_rows
    ):
        raise OverflowError(f"point is off the grid, ({point[0]}, {point[1]})")

    grid = frame_model.to_grid()

    # the point must not be an object
    if grid.get_colour(point[0], point[1]) != frame_model.background_colour:
        return False

    seen_positions: Set[AbsolutePosition] = set()
    positions_to_check: Deque[AbsolutePosition] = deque()
    positions_to_check.append(point)
    while (len(positions_to_check)) > 0:
        current_position = positions_to_check.pop()
        seen_positions.add(current_position)

        x = current_position[0]
        y = current_position[1]
        neighbourhood = grid.get_neighbourhood(x, y)

        # if any neighbour is the background, return False
        for neighbour in neighbourhood:
            neighbour_is_on_the_border = ((neighbour[0] <= 0 or neighbour[0] >= frame_model.number_of_columns - 1)
                or (neighbour[1] <= 0 or neighbour[1] >= frame_model.number_of_rows - 1))
            neighbour_is_background = grid.get_colour(neighbour[0], neighbour[1]) == frame_model.background_colour
            if neighbour_is_on_the_border and neighbour_is_background:
                return False

        # add all neighbours that aren't the background to the queue, if we haven't seen them yet
        neighbouring_squares_that_arent_the_background = list(filter(
            lambda pos: grid.get_colour(pos[0], pos[1]) == frame_model.background_colour,
            neighbourhood
        ))
        for neighbour in neighbouring_squares_that_arent_the_background:
            if neighbour not in seen_positions:
                positions_to_check.append(neighbour)

    return True


def points_contained_by_object(
    obj: Object.Object,
    frame_model: "src.FrameModel.FrameModel.FrameModel"
) -> List[AbsolutePosition]:
    obj_min_x = obj.top_left_offset[0] + min(list(map(
        lambda pos: pos[0],
        obj.relative_positions
    )))
    obj_max_x = obj.top_left_offset[0] + max(list(map(
        lambda pos: pos[0],
        obj.relative_positions
    )))

    obj_min_y = obj.top_left_offset[0] + min(list(map(
        lambda pos: pos[1],
        obj.relative_positions
    )))
    obj_max_y = obj.top_left_offset[0] + max(list(map(
        lambda pos: pos[1],
        obj.relative_positions
    )))

    grid = frame_model.to_grid()
    objs_positions = set(obj.convert_to_absolute_positions())
    contained_points = []

    seen_positions: Set[AbsolutePosition] = set()
    positions_that_have_neighbours_out_of_bounds: Set[AbsolutePosition] = set()
    """
    a point p is contained by an object o if it's not possible to go outside of o's min or max x or y using 
    neighbouring free squares or objects (this includes neighbours of neighbours, etc.) - the positions mustn't already
    be a part of object o 
    """
    for x in range(obj_min_x, obj_max_x + 1):
        for y in range(obj_min_y, obj_max_y + 1):
            if (x, y) in objs_positions: # a part of the object definitely isn't contained _in_ the object
                continue

            possible_positions_that_could_have_out_of_bounds_neighbours: Deque[AbsolutePosition] = deque()
            possible_positions_that_could_have_out_of_bounds_neighbours.append((x, y))
            neighbours_that_are_out_of_bounds = set()
            while (len(possible_positions_that_could_have_out_of_bounds_neighbours)) > 0:
                possible_pos = possible_positions_that_could_have_out_of_bounds_neighbours.pop()
                seen_positions.add(possible_pos)

                possible_x = possible_pos[0]
                possible_y = possible_pos[1]
                neighbourhood = grid.get_neighbourhood(possible_x, possible_y)
                neighbourhood_not_this_obj = list(filter(
                    lambda pos: (pos[0], pos[1]) not in objs_positions,
                    neighbourhood
                ))

                for neighbour in neighbourhood_not_this_obj:
                    neighbour_x = neighbour[0]
                    neighbour_y = neighbour[1]
                    neighbour_is_outside_of_object_bounds = (
                            (neighbour_x < obj_min_x or neighbour_x > obj_max_x)
                            or (neighbour_y < obj_min_y or neighbour_y > obj_max_y)
                    )
                    neighbour_has_its_own_neighbours_out_of_bounds = neighbour in positions_that_have_neighbours_out_of_bounds
                    if neighbour_is_outside_of_object_bounds or neighbour_has_its_own_neighbours_out_of_bounds:
                        neighbours_that_are_out_of_bounds.add(neighbour)
                    elif neighbour not in seen_positions:
                        possible_positions_that_could_have_out_of_bounds_neighbours.append(neighbour)

            if len(neighbours_that_are_out_of_bounds) == 0:
                contained_points.append((x, y))
            else:
                positions_that_have_neighbours_out_of_bounds.add((x, y))
    return contained_points
