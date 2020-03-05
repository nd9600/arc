import unittest
from typing import Dict, List

from src.ARCDriver.ARCDriver import ARCDriver
from src.FrameModel.Object import Object
from src.Types import ObjectId, ObjectKind
from src.FrameModel.FrameModel import FrameModel
from src.Grid.Grid import Grid


class TestGettingFrameSimilarity(unittest.TestCase):
    def test_identical_frames(self):
        frame_model_a = FrameModel.create_from_grid(
            Grid([
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ])
        )
        frame_model_b = FrameModel.create_from_grid(
            Grid([
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ])
        )

        self.assertEqual(
            1,
            ARCDriver.get_frame_similarity(frame_model_a, frame_model_b)
        )

    def test_nearly_identical_frames(self):
        frame_model_a = FrameModel.create_from_grid(
            Grid([
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ])
        )
        frame_model_b = FrameModel.create_from_grid(
            Grid([
                [0, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
            ])
        )

        self.assertEqual(
            8 / 9,
            ARCDriver.get_frame_similarity(frame_model_a, frame_model_b)
        )

    def test_different_frames(self):
        frame_model_a = FrameModel.create_from_grid(
            Grid([
                [1, 1, 3],
                [3, 2, 2],
                [3, 2, 2],
            ])
        )
        frame_model_b = FrameModel.create_from_grid(
            Grid([
                [0, 0, 0],
                [0, 2, 2],
                [0, 2, 2],
            ])
        )

        self.assertEqual(
            4 / 9,
            ARCDriver.get_frame_similarity(frame_model_a, frame_model_b)
        )

    def test_frames_of_different_sizes(self):
        frame_model_a = FrameModel.create_from_grid(
            Grid([
                [1, 1, 3],
                [3, 2, 2],
                [3, 2, 2],
            ])
        )
        frame_model_b = FrameModel.create_from_grid(
            Grid([
                [0, 0, 0],
                [0, 2, 2],
                [0, 2, 2],
                [0, 2, 2],
            ])
        )

        self.assertEqual(
            0,
            ARCDriver.get_frame_similarity(frame_model_a, frame_model_b)
        )


if __name__ == '__main__':
    unittest.main()
