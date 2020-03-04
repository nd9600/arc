import unittest

from src.FrameModel.Object import Object
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
            grid.grid_array,
            grid2.grid_array
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
            grid.grid_array,
            grid2.grid_array
        )

    def test_making_grid_from_frame_model_with_an_occluded_object(self):
        frame_model = FrameModel(
            3,
            3,
            0,
            {
                1: Object(
                    1,
                    (0, 0),
                    [
                        (0, 0),
                        (1, 0),
                        (0, 1),
                        (1, 1),
                    ],
                    0
                ),
                2: Object(
                    2,
                    (1, 1),
                    [
                        (0, 0),
                        (1, 0),
                        (0, 1),
                        (1, 1),
                    ],
                    -1
                )
            },
            []
        )
        grid = frame_model.to_grid()
        self.assertSequenceEqual(
            [
                [1, 1, 0],
                [1, 1, 2],
                [0, 2, 2],
            ],
            grid.grid_array
        )


if __name__ == '__main__':
    unittest.main()
