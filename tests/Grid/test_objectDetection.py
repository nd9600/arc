import unittest


from src.Grid.Grid import Grid


class TestObjectDetection(unittest.TestCase):
    def test_getting_neighbourhoods(self):
        g = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0],
            [0, 3, 0, 3, 0, 0],
            [0, 0, 3, 0, 3, 0],
            [0, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]

        grid = Grid(g)

        self.assertEqual(
            [
                (0, 1),
                (1, 0),
                (1, 1),
            ],
            grid.get_neighbourhood(0, 0)
        )

        self.assertEqual(
            [
                (0, 0),
                (0, 1),
                (1, 1),
                (2, 0),
                (2, 1),
            ],
            grid.get_neighbourhood(1, 0)
        )

        self.assertEqual(
            [
                (0, 0),
                (0, 1),
                (0, 2),
                (1, 0),
                (1, 2),
                (2, 0),
                (2, 1),
                (2, 2),
            ],
            grid.get_neighbourhood(1, 1)
        )

    def test_getting_spatially_continuous_objects(self):
        g = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0],
            [0, 3, 0, 3, 0, 0],
            [0, 0, 3, 0, 3, 0],
            [0, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]

        grid = Grid(g)

        spatially_continuous_objects = grid.parse_objects()
        self.assertEqual(
            1,
            len(spatially_continuous_objects)
        )

    def test_getting_colour_continuous_objects(self):
        g = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 1, 0, 3, 0, 0],
            [0, 0, 3, 0, 3, 0],
            [0, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]

        grid = Grid(g)

        colour_continuous_objects = grid.parse_objects()
        self.assertEqual(
            2,
            len(colour_continuous_objects)
        )

        g = [
            [0, 1, 1, 0, 0, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 1, 3, 3, 3, 0],
            [0, 0, 2, 2, 3, 0],
            [0, 0, 0, 3, 3, 0],
            [0, 0, 0, 0, 0, 0],
        ]

        grid = Grid(g)
        colour_continuous_objects = grid.parse_objects()

        self.assertEqual(
            3,
            len(colour_continuous_objects)
        )

    def test_getting_many_colour_and_spatially_objects_in_a_small_grid(self):
        g = [
            [9, 0, 9, 0, 9, 9],
        ]

        grid = Grid(g)

        colour_continuous_objects = grid.parse_objects()
        self.assertEqual(
            3,
            len(colour_continuous_objects)
        )

    def test_getting_many_colour_and_spatially_objects_in_a_small_vertical_grid(self):
        g = [
            [8, 7],
            [7, 7],
            [0, 0],
            [0, 0],
            [8, 0],
            [8, 0],
        ]

        grid = Grid(g)

        colour_continuous_objects = grid.parse_objects()
        self.assertEqual(
            3,
            len(colour_continuous_objects)
        )


if __name__ == '__main__':
    unittest.main()
