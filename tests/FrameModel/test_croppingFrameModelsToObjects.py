import unittest

import src.Runtime.ObjectRuntime
from src.FrameModel.Object import Object


class TestCroppingFrameModelsToObjects(unittest.TestCase):
    def test_making_frame_model_from_one_object(self):
        obj = Object(
            7,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1),
                (1, 2),
            ],
        )

        frame_model = src.Runtime.ObjectRuntime.crop_frame_model_to_objects([obj], 0)
        self.assertEqual(
            3,
            frame_model.number_of_rows
        )
        self.assertEqual(
            2,
            frame_model.number_of_columns
        )

        self.assertEqual(
            0,
            frame_model.background_colour
        )

        self.assertSequenceEqual(
            [
                [7, 7],
                [7, 7],
                [0, 7],
            ],
            frame_model.to_grid().grid_array
        )

    def test_making_frame_model_from_one_bigger_object(self):

        obj = Object(
            7,
            (10, 14),
            [
                (0, 0),
                (1, 0),
                (1, 1),
                (1, 2),
                (0, 2),
                (1, 3),
                (2, 1),
                (0, 4),
            ],
        )
        frame_model = src.Runtime.ObjectRuntime.crop_frame_model_to_objects([obj], 0)
        self.assertEqual(
            5,
            frame_model.number_of_rows
        )
        self.assertEqual(
            3,
            frame_model.number_of_columns
        )

        self.assertEqual(
            0,
            frame_model.background_colour
        )

        self.assertSequenceEqual(
            [
                [7, 7, 0],
                [0, 7, 7],
                [7, 7, 0],
                [0, 7, 0],
                [7, 0, 0],
            ],
            frame_model.to_grid().grid_array
        )

    def test_making_frame_model_from_one_object_inside_another(self):
        obj_a = Object(
            7,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
                (2, 2),
                (1, 2),
                (0, 2),
                (0, 1),
            ],
        )

        obj_b = Object(
            5,
            (2, 2),
            [
                (0, 0)
            ],
        )

        frame_model = src.Runtime.ObjectRuntime.crop_frame_model_to_objects([obj_a, obj_b], 0)
        self.assertEqual(
            3,
            frame_model.number_of_rows
        )
        self.assertEqual(
            3,
            frame_model.number_of_columns
        )

        self.assertEqual(
            0,
            frame_model.background_colour
        )

        self.assertSequenceEqual(
            [
                [7, 7, 7],
                [7, 5, 7],
                [7, 7, 7],
            ],
            frame_model.to_grid().grid_array
        )


if __name__ == '__main__':
    unittest.main()
