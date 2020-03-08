import unittest

import UsefulFunctions
import src.Runtime.ObjectRuntime as ObjectRuntime
from src.FrameModel.Object import Object


class TestRotatingObjects(unittest.TestCase):
    def test_rotating_line_90_degrees(self):
        obj = Object(
            1,
            (1, 0),
            [
                (0, 0),
                (1, 0),
                (2, 0),
            ]
        )
        rotated_obj: Object = ObjectRuntime.rotate_object(obj, 90)
        self.assertEqual(
            [
                (0, 0),
                (0, 1),
                (0, 2),
            ],
            rotated_obj.relative_positions
        )

    def test_rotating_l_shape_90_degrees(self):
        obj = Object(
            1,
            (1, 0),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ]
        )
        # rotated_obj: Object = UsefulFunctions.compose([ObjectRuntime.rotate_object_90])(obj)
        rotated_obj: Object = ObjectRuntime.rotate_object(obj, 90)
        # the top left offset had to be shifted to accomodate something
        self.assertEqual(
            (0, 0),
            rotated_obj.top_left_offset
        )
        self.assertEqual(
            [
                (1, 0),
                (1, 1),
                (1, 2),
                (0, 2),
            ],
            rotated_obj.relative_positions
        )

    def test_rotating_l_shape_360_degrees_doesnt_move_it_at_all(self):
        obj = Object(
            1,
            (1, 0),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ]
        )

        rotated_obj: Object = ObjectRuntime.rotate_object(obj, 360)
        self.assertEqual(
            obj.top_left_offset,
            rotated_obj.top_left_offset
        )
        self.assertEqual(
            obj.relative_positions,
            rotated_obj.relative_positions
        )

    def test_rotating_l_shape_90_degrees_4_times_doesnt_change_its_relative_positions(self):
        """
        rotating an object can make it go off the grid; to prevent that, we snap it back onto the grid
        :return:
        """
        obj = Object(
            1,
            (1, 0),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ]
        )

        rotated_obj = UsefulFunctions.compose(
            [
                ObjectRuntime.rotate_object_90,
                ObjectRuntime.rotate_object_90,
                ObjectRuntime.rotate_object_90,
                ObjectRuntime.rotate_object_90
            ]
        )(obj)
        self.assertEqual(
            obj.relative_positions,
            rotated_obj.relative_positions
        )


if __name__ == '__main__':
    unittest.main()
