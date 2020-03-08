from typing import List, Tuple
from functools import partial

import json
import math

import src.FrameModel.FrameModel
import src.FrameModel.Object as Object
from Types import AbsolutePosition


def are_objects_the_same(a: Object.Object, b: Object.Object) -> bool:
    a_kind = a.get_object_kind()
    b_kind = b.get_object_kind()

    a_colour, a_relative_positions_string = a_kind.split(":")
    b_colour, b_relative_positions_string = b_kind.split(":")

    if a_colour != b_colour:
        return False

    # we convert to sets so that the order of the relative_positions doesn't matter
    a_relative_positions = set(map(
        lambda position: (position[0], position[1]),
        json.loads(a_relative_positions_string)
    ))
    b_relative_positions = set(map(
        lambda position: (position[0], position[1]),
        json.loads(b_relative_positions_string)
    ))

    b_rotated_90: Object.Object = relatively_rotate_object_90(b)
    b_rotated_180: Object.Object = relatively_rotate_object_180(b)
    b_rotated_270: Object.Object = relatively_rotate_object_270(b)

    relative_positions_are_the_same_after_some_rotation = (
        a_relative_positions == b_relative_positions
        or a_relative_positions == set(b_rotated_90.relative_positions)
        or a_relative_positions == set(b_rotated_180.relative_positions)
        or a_relative_positions == set(b_rotated_270.relative_positions)
    )
    return relative_positions_are_the_same_after_some_rotation


def crop_frame_model_to_objects(objects: List[Object.Object], background_colour: int = 0) -> "src.FrameModel.FrameModel.FrameModel":
    # finds the top left offset that is the the left of and above all objects,
    # and converts all the objects' top left offsets relative to that
    min_top_left_x = 32
    min_top_left_y = 32

    # also calculates the max x and y offsets, used to find the numbers of rows and columns needed
    max_x_offset = 0
    max_y_offset = 0

    for obj in objects:
        if obj.top_left_offset[0] < min_top_left_x:
            min_top_left_x = obj.top_left_offset[0]
        if obj.top_left_offset[1] < min_top_left_y:
            min_top_left_y = obj.top_left_offset[1]

        obj_max_x_offset = max(list(map(
            lambda pos: pos[0],
            obj.relative_positions
        )))
        if obj_max_x_offset > max_x_offset:
            max_x_offset = obj_max_x_offset

        obj_max_y_offset = max(list(map(
            lambda pos: pos[1],
            obj.relative_positions
        )))
        if obj_max_y_offset > max_y_offset:
            max_y_offset = obj_max_y_offset

    for i, obj in enumerate(objects):
        obj.top_left_offset = (obj.top_left_offset[0] - min_top_left_x, obj.top_left_offset[1] - min_top_left_y)
        objects[i] = obj

    number_of_rows = max_y_offset + 1  # if the only relative_position is (0, 0), the object is 1x1
    number_of_columns = max_x_offset + 1
    return src.FrameModel.FrameModel.FrameModel(
        number_of_rows,
        number_of_columns,
        background_colour,
        objects
    )


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
