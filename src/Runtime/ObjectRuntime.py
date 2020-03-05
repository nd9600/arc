import json
from typing import List

import src.FrameModel.FrameModel
import src.FrameModel.Object as Object


def objects_are_the_same(a: Object.Object, b: Object.Object) -> bool:
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


def crop_frame_model_to_objects(objects: List[Object.Object], background_colour: int = 0) -> "src.FrameModel":
    # todo: find top left offset that is the the left of and above all objects, and convert all the objects top left offsets relative to that
    obj = objects[0]
    obj.top_left_offset = (0, 0)

    max_x_offset = max(list(map(
        lambda pos: pos[0],
        obj.relative_positions
    )))
    max_y_offset = max(list(map(
        lambda pos: pos[1],
        obj.relative_positions
    )))

    object_height = max_y_offset + 1  # if the only relative_position is (0, 0), the object is 1x1
    object_width = max_x_offset + 1
    return src.FrameModel.FrameModel.FrameModel(
        object_height,
        object_width,
        background_colour,
        [obj]
    )
