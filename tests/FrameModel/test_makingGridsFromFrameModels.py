import unittest

from src.FrameModel.FrameModel import FrameModel
from src.Grid.Grid import Grid


class TestMakingGridsFromFrameModels(unittest.TestCase):
    def test_making_grid_from_frame_model_with_one_object(self):
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
        self.assertSequenceEqual(
            grid.grid,
            grid2.grid
        )

    def test_making_grid_from_frame_model_with_four_objects(self):
        g = [
            [1, 1, 1, 1, 1, 1],
            [1, 0, 3, 0, 0, 0],
            [1, 3, 5, 3, 0, 0],
            [1, 0, 3, 5, 3, 4],
            [1, 0, 0, 3, 0, 0],
        ]
        grid = Grid(g)

        frame_model = FrameModel.create_from_grid(grid)
        grid2 = frame_model.to_grid()
        self.assertSequenceEqual(
            grid.grid,
            grid2.grid
        )


if __name__ == '__main__':
    unittest.main()
