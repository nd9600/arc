from typing import List
from src.Types import AbsolutePosition, RelativePosition

import json
import math

import src.FrameModel.FrameModel
import src.FrameModel.Object as Object


def are_objects_the_same(a: Object.Object, b: Object.Object) -> bool:
    a_kind = a.get_object_kind()
    b_kind = b.get_object_kind()

    a_colour, a_relative_positions_string = a_kind.split(":")
    b_colour, b_relative_positions_string = b_kind.split(":")

    if a_colour != b_colour:
        return False

    a_relative_positions = list(map(
        lambda position: (position[0], position[1]),
        json.loads(a_relative_positions_string)
    ))
    b_relative_positions = list(map(
        lambda position: (position[0], position[1]),
        json.loads(b_relative_positions_string)
    ))
    if a_relative_positions != b_relative_positions:  # todo: won't recognise objects as the same if one is rotated
        return False

    return True


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


def rotate_object_about_point(obj: Object.Object, angle: int, about_point) -> Object.Object:
    def round_half_up(n):
        return math.floor(n + 0.5)

    def round_half_down(n):
        return math.ceil(n - 0.5)

    def rotate(point: RelativePosition, radian_angle: float, origin: AbsolutePosition = (0, 0)):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(radian_angle) * (px - ox) - math.sin(radian_angle) * (py - oy)
        qy = oy + math.sin(radian_angle) * (px - ox) + math.cos(radian_angle) * (py - oy)
        print((qx), (qy))
        rounded_qx = math.floor(qx) if qx > 0 else math.ceil(qx)
        rounded_qy = math.floor(qy) if qy > 0 else math.ceil(qy)
        return rounded_qx, rounded_qy

    angle_in_radians = (angle) * math.pi/180
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

    print(obj.top_left_offset, obj.relative_positions)
    print(top_left_offset_after_rotation, rotated_relative_positions)
    top_left_offset_after_rotation = (
        max(top_left_offset_after_rotation[0], 0),
        max(top_left_offset_after_rotation[1], 0)
    )
    # todo: move the tl offset if (it + max obj offset) is > grid size, too
    print(top_left_offset_after_rotation, rotated_relative_positions)

    return Object.Object(
        obj.colour,
        top_left_offset_after_rotation,
        rotated_relative_positions,
        obj.depth
    )


def rotate_object(obj: Object.Object, angle: int) -> Object.Object:
    return rotate_object_about_point(obj, angle, (0, 0))


def rotate_object_90(obj: Object.Object) -> Object.Object:
    return rotate_object(obj, 90)

def rotate_object_45(obj: Object.Object) -> Object.Object:
    return rotate_object(obj, 45)
