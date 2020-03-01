import unittest

import sys
sys.path.append('../../src')

from Grid import Grid


class MyTestCase(unittest.TestCase):
    def test_getting_neighbourhoods(self):
        g = [[0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0], [0, 3, 0, 3, 0, 0], [0, 0, 3, 0, 3, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0]]

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


if __name__ == '__main__':
    unittest.main()
