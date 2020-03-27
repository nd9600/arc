import unittest

import src.Runtime.ObjectRuntime as ObjectRuntime
from src.FrameModel.Object import Object


class TestGettingObjectSize(unittest.TestCase):
    def test_getting_object_size(self):
        obj_a = Object(
            1,
            (0, 0),
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
        self.assertEqual(
            10,
            ObjectRuntime.get_size(obj_a)
        )

        obj_b = Object(
            8,
            (7, 3),
            [
                (10, 12),
            ]
        )
        self.assertEqual(
            1,
            ObjectRuntime.get_size(obj_b)
        )

        obj_c = Object(
            1,
            (2, 9),
            [
                (0, 0),
                (1, 0),
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
            ]
        )
        self.assertEqual(
            6,
            ObjectRuntime.get_size(obj_c)
        )


if __name__ == '__main__':
    unittest.main()
