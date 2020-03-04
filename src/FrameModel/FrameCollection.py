from typing import List

from src.FrameModel.FrameModel import FrameModel


class FrameCollection:
    def __init__(
        self,
        frames: List[FrameModel]
    ):
        self.frames = frames
