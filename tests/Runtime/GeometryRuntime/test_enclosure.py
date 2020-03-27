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

        self.assertFalse(GeometryRuntime.is_point_fully_enclosed((0, 0), frame_model))
        for pos in obj_b.convert_to_absolute_positions():
            self.assertFalse(GeometryRuntime.is_point_fully_enclosed(pos, frame_model))

        self.assertFalse(GeometryRuntime.is_point_fully_enclosed((1, 0), frame_model))
        self.assertFalse(GeometryRuntime.is_point_fully_enclosed((1, 1), frame_model))
        self.assertFalse(GeometryRuntime.is_point_fully_enclosed((0, 1), frame_model))

        self.assertTrue(GeometryRuntime.is_point_fully_enclosed((3, 3), frame_model))
        self.assertTrue(GeometryRuntime.is_point_fully_enclosed((4, 3), frame_model))

    def test_what_points_object_contains_when_its_enclosed(self):
        obj_a = Object(
            2,
            (0, 0),
            [
                (0, 0)
            ]
        )

        obj_b = Object(
            1,
            (2, 2),
            [
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
        )
        frame_model = ObjectRuntime.make_frame_model_from_objects([obj_a, obj_b], 0)

        self.assertEqual(
            0,
            len(GeometryRuntime.points_contained_by_object(obj_a, frame_model))
        )

        points_contained_by_b = GeometryRuntime.points_contained_by_object(obj_b, frame_model)
        self.assertEqual(
            2,
            len(points_contained_by_b)
        )
        self.assertSequenceEqual(
            [
                (3, 3),
                (4, 3)
            ],
            points_contained_by_b
        )

    def test_what_points_object_contains_when_its_not_enclosed(self):
        obj_a = Object(
            1,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (3, 2),
                (2, 2),
                (1, 2),
                (0, 2),
                (0, 1),
            ]
        )
        obj_b = Object(
            2,
            (5, 5),
            [
                (0, 0)
            ]
        )

        frame_model = ObjectRuntime.make_frame_model_from_objects([obj_a, obj_b], 0, False)
        points_contained_by_b = GeometryRuntime.points_contained_by_object(obj_a, frame_model)
        self.assertEqual(
            0,
            len(points_contained_by_b)
        )

    def test_what_points_object_contains_when_theres_another_object_in_the_way(self):
        obj_a = Object(
            1,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (3, 2),
                (3, 3),
                (2, 2),
                (1, 2),
                (0, 2),
                (0, 1),
            ]
        )
        obj_b = Object(
            2,
            (5, 5),
            [
                (0, 0)
            ]
        )
        obj_c = Object(
            3,
            (4, 2),
            [
                (0, 0)
            ]
        )

        frame_model = ObjectRuntime.make_frame_model_from_objects([obj_a, obj_b, obj_c], 0, False)
        points_contained_by_b = GeometryRuntime.points_contained_by_object(obj_a, frame_model)
        self.assertEqual(
            0,
            len(points_contained_by_b)
        )


if __name__ == '__main__':
    unittest.main()
