import unittest

from src.FrameModel.FrameModel import FrameModel
from src.Grid.Grid import Grid


class TestMakingGridsFromFrameModels(unittest.TestCase):
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
        grid2 = frame_model.to_grid()
        self.assertEqual(
            grid,
            grid2
        )


if __name__ == '__main__':
    unittest.main()
