import unittest

import src.Runtime.ObjectRuntime as ObjectRuntime
import src.Runtime.GeometryRuntime as GeometryRuntime
from src.FrameModel.Object import Object


class TestEnclosure(unittest.TestCase):
    def test_is_point_enclosed_in_cropped_rectangle(self):
        relative_positions = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (3, 1),
            (3, 2),
            (2, 2),
            (1, 2),
            (0, 2),
            (0, 1),
        ]
        obj = Object(
            1,
            (0, 0),
            relative_positions
        )
        frame_model = ObjectRuntime.make_frame_model_from_objects([obj], 0)

        for pos in relative_positions:
            self.assertFalse(GeometryRuntime.is_point_fully_enclosed(pos, frame_model))
        self.assertTrue(GeometryRuntime.is_point_fully_enclosed((1, 1), frame_model))
        self.assertTrue(GeometryRuntime.is_point_fully_enclosed((2, 1), frame_model))

    def test_is_point_enclosed_in_rectangle(self):
        obj_a = Object(
            2,
            (0, 0),
            [
                (0, 0)
            ]
        )

        relative_positions = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (3, 1),
            (3, 2),
            (2, 2),
            (1, 2),
            (0, 2),
            (0, 1),
        ]
        obj_b = Object(
            1,
            (2, 2),
            relative_positions
        )
        frame_model = ObjectRuntime.make_frame_model_from_objects([obj_a, obj_b], 0)
        # frame_model.to_grid().plot()

        self.assertFalse(GeometryRuntime.is_point_fully_enclosed((0, 0), frame_model))
        for pos in obj_b.convert_to_absolute_positions():
            self.assertFalse(GeometryRuntime.is_point_fully_enclosed(pos, frame_model))

        self.assertFalse(GeometryRuntime.is_point_fully_enclosed((1, 0), frame_model))
        self.assertFalse(GeometryRuntime.is_point_fully_enclosed((1, 1), frame_model))
        self.assertFalse(GeometryRuntime.is_point_fully_enclosed((0, 1), frame_model))

        self.assertTrue(GeometryRuntime.is_point_fully_enclosed((3, 3), frame_model))
        self.assertTrue(GeometryRuntime.is_point_fully_enclosed((4, 3), frame_model))


if __name__ == '__main__':
    unittest.main()
