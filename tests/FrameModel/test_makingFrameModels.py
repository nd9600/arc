import unittest

from src.FrameModel.FrameModel import FrameModel
from src.Grid.Grid import Grid


class TestMakingFrameModels(unittest.TestCase):
    def test_making_frame_model_from_grid_with_one_object(self):
        g = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0],
            [0, 3, 0, 3, 0, 0],
            [0, 0, 3, 0, 3, 0],
            [0, 0, 0, 3, 0, 0],
        ]
        grid = Grid(g)

        frame_model = FrameModel.create_from_grid(grid)
        self.assertEqual(
            6,
            frame_model.number_of_columns
        )
        self.assertEqual(
            5,
            frame_model.number_of_rows
        )

        self.assertEqual(
            0,
            frame_model.background_colour
        )

        self.assertEqual(
            1,
            len(frame_model.objects)
        )


if __name__ == '__main__':
    unittest.main()
