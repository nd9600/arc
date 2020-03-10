import unittest
from typing import Dict, List

from src.FrameModel.FrameModel import FrameModel
from src.FrameModel.Object import Object
from src.Runtime import ObjectRuntime
from src.Types import ObjectId, ObjectKind


class TestMatchingSameObjectInstances(unittest.TestCase):
    def test_matching_one_object_across_frames(self):
        obj_1 = Object(
            1,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ],
            0,
            1
        )
        obj_1b = Object(
            1,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ],
            0,
            2
        )
        original_frame_model = FrameModel(
            5,
            5,
            0,
            [
                obj_1
            ]
        )
        second_frame_model = FrameModel(
            5,
            5,
            0,
            [
                obj_1b
            ]
        )

        self.assertSequenceEqual(
            [
                2
            ],
            list(second_frame_model.objects.keys())
        )

        second_frame_model_after_match = ObjectRuntime.match_objects_in_second_frame_to_those_in_first(
            original_frame_model, second_frame_model
        )
        matched_second_object = second_frame_model_after_match.objects[obj_1.id]

        self.assertSequenceEqual(
            [
                1
            ],
            list(second_frame_model_after_match.objects.keys())
        )
        self.assertEqual(
            obj_1.colour,
            matched_second_object.colour,
        )
        self.assertEqual(
            obj_1.top_left_offset,
            matched_second_object.top_left_offset,
        )
        self.assertSequenceEqual(
            obj_1.relative_positions,
            matched_second_object.relative_positions,
        )

    def test_matching_one_object_out_of_three_across_frames(self):
        obj_1 = Object(
            1,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ],
            0,
            1
        )
        obj_2 = Object(
            2,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ],
            0,
            2
        )
        obj_3 = Object(
            1,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 2),
            ],
            0,
            3
        )

        obj_1b = Object(
            1,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ],
            0,
            4
        )
        obj_2b = Object(
            3,
            (1, 1),
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
            ],
            0,
            5
        )
        obj_3b = Object(
            1,
            (1, 1),
            [
                (0, 1),
                (1, 0),
                (2, 0),
                (2, 1),
            ],
            0,
            6
        )

        original_frame_model = FrameModel(
            5,
            5,
            0,
            [
                obj_1,
                obj_2,
                obj_3,
            ]
        )
        second_frame_model = FrameModel(
            5,
            5,
            0,
            [
                obj_1b,
                obj_2b,
                obj_3b,
            ]
        )

        self.assertSequenceEqual(
            [
                4,
                5,
                6
            ],
            list(second_frame_model.objects.keys())
        )

        second_frame_model_after_match = ObjectRuntime.match_objects_in_second_frame_to_those_in_first(
            original_frame_model, second_frame_model
        )
        matched_second_object = second_frame_model_after_match.objects[obj_1.id]

        self.assertSequenceEqual(
            [
                1,
                5,
                6
            ],
            list(second_frame_model_after_match.objects.keys())
        )
        self.assertEqual(
            obj_1.colour,
            matched_second_object.colour,
        )
        self.assertEqual(
            obj_1.top_left_offset,
            matched_second_object.top_left_offset,
        )
        self.assertSequenceEqual(
            obj_1.relative_positions,
            matched_second_object.relative_positions,
        )




if __name__ == '__main__':
    unittest.main()
