import unittest

import src.Runtime.ObjectRuntime as ObjectRuntime
import src.Runtime.NumerosityRuntime as NumerosityRuntime
import src.Runtime.ListRuntime as ListRuntime
import src.Runtime.FrameModelRuntime as FrameModelRuntime

from src.FrameModel.Object import Object
from src.FrameModel.FrameModel import FrameModel


class TestRuntimeCombinations(unittest.TestCase):
    def test_getting_the_biggest_object(self):
        obj_a = Object(
            1,
            (0, 0),
            [
                (0, 0),
                (1, 1),
                (2, 2),
            ]
        )
        obj_b = Object(
            2,
            (0, 1),
            [
                (0, 0),
                (1, 1),
                (2, 2),
                (3, 3),
            ]
        )
        obj_c = Object(
            3,
            (0, 2),
            [
                (0, 0),
                (1, 1),
            ]
        )

        frame_model = ObjectRuntime.make_frame_model_from_objects([obj_a, obj_b, obj_c], 0)

        # get list of objects
        #
        new_frame_model = FrameModelRuntime.change_objects(frame_model, [obj_b])
        new_frame_model.to_grid().plot()
        self.assertEqual(
            1,
            len(list(new_frame_model.objects.values()))
        )
        self.assertEqual(
            obj_b,
            list(new_frame_model.objects.values())[0]
        )


if __name__ == '__main__':
    unittest.main()
