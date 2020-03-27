import unittest

import src.Runtime.NumerosityRuntime as NumerosityRuntime


class TestNumerosityRuntime(unittest.TestCase):
    def test_incrementing(self):
        self.assertEqual(
            2,
            NumerosityRuntime.inc(1)
        )

if __name__ == '__main__':
    unittest.main()
