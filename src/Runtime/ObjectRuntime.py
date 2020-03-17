import json
from typing import List

import src.FrameModel.FrameModel
import src.FrameModel.Object as Object
from src.Runtime import GeometryRuntime


def are_objects_the_same_kind(a: Object.Object, b: Object.Object) -> bool:
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

    b_rotated_90: Object.Object = GeometryRuntime.relatively_rotate_object_90(b)
    b_rotated_180: Object.Object = GeometryRuntime.relatively_rotate_object_180(b)
    b_rotated_270: Object.Object = GeometryRuntime.relatively_rotate_object_270(b)

    relative_positions_are_the_same_after_some_rotation = (
        a_relative_positions == b_relative_positions
        or a_relative_positions == set(b_rotated_90.relative_positions)
        or a_relative_positions == set(b_rotated_180.relative_positions)
        or a_relative_positions == set(b_rotated_270.relative_positions)
    )
    return relative_positions_are_the_same_after_some_rotation


def are_objects_the_same_instance(a: Object.Object, b: Object.Object) -> bool:
    return (
        a.colour == b.colour
        and a.top_left_offset == b.top_left_offset
        and a.depth == b.depth
        and set(a.relative_positions) == set(b.relative_positions)
    )


def crop_frame_model_to_objects(objects: List[Object.Object], background_colour: int = 0) -> "src.FrameModel.FrameModel.FrameModel":
    # finds the top left offset that is the the left of and above all objects,
    # and converts all the objects' top left offsets relative to that
    min_top_left_x = 32
    min_top_left_y = 32

    # also calculates the max x and y absolute positions, used to find the numbers of rows and columns needed
    max_x = 0
    max_y = 0

    for obj in objects:
        if obj.top_left_offset[0] < min_top_left_x:
            min_top_left_x = obj.top_left_offset[0]
        if obj.top_left_offset[1] < min_top_left_y:
            min_top_left_y = obj.top_left_offset[1]

        obj_max_x = obj.top_left_offset[0] + max(list(map(
            lambda pos: pos[0],
            obj.relative_positions
        )))
        if obj_max_x > max_x:
            max_x = obj_max_x

        obj_max_y = obj.top_left_offset[1] + max(list(map(
            lambda pos: pos[1],
            obj.relative_positions
        )))
        if obj_max_y > max_y:
            max_y = obj_max_y

    # converts all the objects' top left offsets relative to the the min top left offset
    for i, obj in enumerate(objects):
        obj.top_left_offset = (obj.top_left_offset[0] - min_top_left_x, obj.top_left_offset[1] - min_top_left_y)
        objects[i] = obj

    max_y_distance = max_y - min_top_left_y
    number_of_rows = max_y_distance + 1 # if the only relative_position is (0, 0), the object is 1x1

    max_x_distance = max_x - min_top_left_x
    number_of_columns = max_x_distance + 1
    return src.FrameModel.FrameModel.FrameModel(
        number_of_rows,
        number_of_columns,
        background_colour,
        objects
    )


def match_objects_in_second_frame_to_those_in_first(
    original_frame_model: "src.FrameModel.FrameModel.FrameModel",
    second_frame_model: "src.FrameModel.FrameModel.FrameModel"
) -> "src.FrameModel.FrameModel.FrameModel":

    matched_objects_in_second_frame = []
    for second_obj in second_frame_model.objects.values():
        for original_obj in original_frame_model.objects.values():
            if are_objects_the_same_instance(original_obj, second_obj):
                second_obj.id = original_obj.id
                break
        matched_objects_in_second_frame.append(second_obj)

    return src.FrameModel.FrameModel.FrameModel(
        second_frame_model.number_of_rows,
        second_frame_model.number_of_columns,
        second_frame_model.background_colour,
        matched_objects_in_second_frame,
        second_frame_model.agents,
    )
