import unittest

import src.UsefulFunctions as UsefulFunctions
import src.Runtime.NumerosityRuntime as NumerosityRuntime
import src.Runtime.ListRuntime as ListRuntime


class TestListRuntime(unittest.TestCase):
    def test_copying_an_element(self):
        array = [12, 13, 14, 15, 16]
        self.assertSequenceEqual(
            [12, 13, 14, 15, 16, 13],
            ListRuntime.copy_element(array, 1)
        )

    def test_deleting_an_element(self):
        array = [12, 13, 14, 15, 16]
        self.assertSequenceEqual(
            [12, 14, 15, 16],
            ListRuntime.delete_element(array, 1)
        )

    def test_appending_an_element(self):
        array = [12, 13, 14, 15, 16]
        self.assertSequenceEqual(
            [12, 13, 14, 15, 16, 1234],
            ListRuntime.append_element(array, 1234)
        )

    def test_mapping_a_list(self):
        array = [12, 13, 14, 15, 16]
        self.assertSequenceEqual(
            [24, 26, 28, 30, 32],
            ListRuntime.map_list(lambda x: x * 2, array)
        )

        array = [12, 13, 14, 15, 16]
        self.assertSequenceEqual(
            [19, 20, 21, 22, 23],
            ListRuntime.map_list(NumerosityRuntime.add_partial(7), array)
        )

        array = [12, 13, 14, 15, 16]
        self.assertSequenceEqual(
            [5, 6, 7, 8, 9],
            ListRuntime.map_list(NumerosityRuntime.subtract_partial(7), array)
        )

    def test_filtering_a_list(self):
        array = [12, 13, 14, 15, 16]
        self.assertSequenceEqual(
            [15, 16],
            ListRuntime.filter_list(NumerosityRuntime.greater_than_partial(14), array)
        )

    def test_filtering_and_mapping_a_list(self):
        array = [12, 13, 14, 15, 16]
        self.assertSequenceEqual(
            [22, 23],
            ListRuntime.map_list(
                NumerosityRuntime.add_partial(7),
                ListRuntime.filter_list(NumerosityRuntime.greater_than_partial(14), array)
            )
        )

    def test_mapping_and_filtering_a_list(self):
        array = [12, 13, 14, 15, 16]
        self.assertSequenceEqual(
            [22, 23],
            ListRuntime.filter_list(
                NumerosityRuntime.greater_than_partial(21),
                ListRuntime.map_list(NumerosityRuntime.add_partial(7), array)
            )
        )

    def test_mapping_and_filtering_a_list_with_compose(self):
        array = [12, 13, 14, 15, 16]

        self.assertSequenceEqual(
            [22, 23],
            UsefulFunctions.compose([
                ListRuntime.filter_list_partial(NumerosityRuntime.greater_than_partial(21)),
                ListRuntime.map_list_partial(NumerosityRuntime.add_partial(7))
            ])(array)
        )


if __name__ == '__main__':
    unittest.main()
