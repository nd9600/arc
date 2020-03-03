import unittest

from src.FrameModel.Object import Object


class TestMakingObjects(unittest.TestCase):
    def test_making_object_with_absolute_positions(self):
        absolute_positions = [
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 2),
            (2, 3),
        ]
        o = Object.create_with_absolute_positions(1, absolute_positions, 0)
        self.assertEqual((1, 0), o.top_left_offset)

        self.assertEqual(
            [
                (0, 0),
                (0, 1),
                (0, 2),
                (1, 2),
                (1, 3),
            ],
            o.relative_positions
        )

    def test_converting_from_relative_to_absolute_positions(self):
        relative_positions = [
            (-1, 0),
            (0, -1),
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 2)
        ]

        self.assertEqual(
            [
                (0, 1),
                (1, 0),
                (1, 1),
                (1, 2),
                (2, 2),
                (2, 3),
            ],
            Object.convert_to_absolute_positions((1, 1), relative_positions)
        )


if __name__ == '__main__':
    unittest.main()
