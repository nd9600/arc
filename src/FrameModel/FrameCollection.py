from typing import List

from FrameModel.FrameModel import FrameModel


class FrameCollection:
    def __init__(
        self,
        frames: List[FrameModel]
    ):
        self.frames = frames
