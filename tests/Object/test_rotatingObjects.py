import unittest

import UsefulFunctions
import src.Runtime.ObjectRuntime as ObjectRuntime
from FrameModel.FrameModel import FrameModel
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
        rotated_obj: Object = ObjectRuntime.relatively_rotate_object_90(obj)
        self.assertEqual(
            [
                (0, 0),
                (0, 1),
                (0, 2),
            ],
            rotated_obj.relative_positions
        )

    def test_relatively_rotating_l_shape_270_degrees(self):
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
        rotated_obj: Object = UsefulFunctions.compose([
            ObjectRuntime.relatively_rotate_object_270,
        ])(obj)
        self.assertEqual(
            (1, 0),
            rotated_obj.top_left_offset
        )
        self.assertEqual(
            [
                (0, 2),
                (0, 1),
                (0, 0),
                (1, 0)
            ],
            rotated_obj.relative_positions
        )

    def test_absolutely_rotating_l_shape_270_degrees_when_it_would_go_off_top_of_grid(self):
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

        rotated_obj: Object = ObjectRuntime.absolutely_rotate_object_270((1, 0), obj)
        self.assertEqual(
            (1, 0),
            rotated_obj.top_left_offset
        )
        self.assertEqual(
            [
                (0, 2),
                (0, 1),
                (0, 0),
                (1, 0)
            ],
            rotated_obj.relative_positions
        )

    def test_absolutely_rotating_l_shape_270_degrees_when_it_wouldnt_go_off_top_of_grid(self):
        obj = Object(
            1,
            (5, 5),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ]
        )

        rotated_obj: Object = ObjectRuntime.absolutely_rotate_object_270((5, 5), obj)
        self.assertEqual(
            (5, 3),
            rotated_obj.top_left_offset
        )
        self.assertEqual(
            [
                (0, 2),
                (0, 1),
                (0, 0),
                (1, 0)
            ],
            rotated_obj.relative_positions
        )

    def test_relatively_rotating_l_shape_270_degrees_when_it_wouldnt_go_off_top_of_grid(self):
        obj = Object(
            1,
            (5, 5),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ]
        )

        rotated_obj: Object = ObjectRuntime.relatively_rotate_object_270(obj)
        self.assertEqual(
            (5, 3),
            rotated_obj.top_left_offset
        )
        self.assertEqual(
            [
                (0, 2),
                (0, 1),
                (0, 0),
                (1, 0)
            ],
            rotated_obj.relative_positions
        )

    def test_rotating_l_shape_90_degrees_when_it_wouldnt_go_off_grid(self):
        obj = Object(
            1,
            (9, 3),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ]
        )
        rotated_obj: Object = UsefulFunctions.compose([ObjectRuntime.relatively_rotate_object_90])(obj)
        # the top left offset had to be shifted to accommodate the L being 2 squares wide
        self.assertEqual(
            (8, 3),
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

        rotated_obj: Object = ObjectRuntime.relatively_rotate_object(360, obj)
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
                ObjectRuntime.relatively_rotate_object_90,
                ObjectRuntime.relatively_rotate_object_90,
                ObjectRuntime.relatively_rotate_object_90,
                ObjectRuntime.relatively_rotate_object_90
            ]
        )(obj)
        self.assertEqual(
            obj.relative_positions,
            rotated_obj.relative_positions
        )


if __name__ == '__main__':
    unittest.main()
