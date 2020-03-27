from typing import List

import src.FrameModel.FrameModel as FrameModel
import src.FrameModel.Object as Object


def change_objects(
    frame_model: FrameModel.FrameModel,
    objects: List[Object.Object],
) -> "src.FrameModel.FrameModel.FrameModel":
    return FrameModel.FrameModel(
        frame_model.number_of_rows,
        frame_model.number_of_columns,
        frame_model.background_colour,
        objects,
        frame_model.agents
    )