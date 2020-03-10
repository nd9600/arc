import math
from functools import partial
from typing import Tuple

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