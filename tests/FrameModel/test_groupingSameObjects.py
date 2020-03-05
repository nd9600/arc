import unittest
from typing import Dict, List

from src.FrameModel.Object import Object
from src.Types import ObjectId, ObjectKind
from src.FrameModel.FrameModel import FrameModel
from src.Grid.Grid import Grid


class TestGroupingSameObjects(unittest.TestCase):
    def test_grouping_one_object(self):
        obj = Object(
            1,
            (1, 0),
            [
                (0, 0),
                (1, 0),
            ],
            0
        )
        frame_model = FrameModel(
            3,
            3,
            0,
            [
                obj
            ]
        )
        expected_grouped_objects: Dict[ObjectKind, List[ObjectId]] = {
            obj.get_object_kind(): [obj.id]
        }
        expected_object_group = expected_grouped_objects[obj.get_object_kind()]

        actual_grouped_objects = frame_model.group_same_objects()
        actual_object_group = actual_grouped_objects[obj.get_object_kind()]
        self.assertEqual(1, len(list(actual_grouped_objects.keys())))
        self.assertEqual(1, len(actual_object_group))

        print(expected_grouped_objects)
        print(actual_grouped_objects)

        self.assertEqual(
            list(expected_grouped_objects.keys()),
            list(actual_grouped_objects.keys())
        )
        self.assertEqual(
            expected_object_group,
            actual_object_group
        )

    def test_grouping_two_objects(self):
        obj_a = Object(
            1,
            (1, 0),
            [
                (0, 0),
                (1, 0),
            ],
            0
        )
        obj_b = Object(
            1,
            (0, 4),
            [
                (0, 0),
                (1, 0),
            ],
            1
        )
        frame_model = FrameModel(
            4,
            3,
            0,
            [
                obj_a,
                obj_b,
            ]
        )
        expected_grouped_objects: Dict[ObjectKind, List[ObjectId]] = {
            obj_a.get_object_kind(): [obj_a.id, obj_b.id]
        }
        expected_object_group = expected_grouped_objects[obj_a.get_object_kind()]

        actual_grouped_objects = frame_model.group_same_objects()
        actual_object_group = actual_grouped_objects[obj_a.get_object_kind()]

        self.assertEqual(1, len(list(actual_grouped_objects.keys())))
        self.assertEqual(2, len(actual_object_group))

        self.assertEqual(
            list(expected_grouped_objects.keys()),
            list(actual_grouped_objects.keys())
        )
        self.assertEqual(
            expected_object_group,
            actual_object_group
        )

    def test_grouping_two_objects_where_one_is_rotated(self):
        # todo: fails because rotation isn't taken into account
        g = [
            [0, 1, 1],
            [0, 0, 0],
            [0, 1, 0],
            [0, 1, 0],
        ]
        obj_a = Object(
            1,
            (1, 0),
            [
                (0, 0),
                (1, 0),
            ],
            0
        )
        obj_b = Object(
            1,
            (2, 3),
            [
                (0, 0),
                (0, 1),
            ],
            1
        )
        frame_model = FrameModel(
            4,
            3,
            0,
            [
                obj_a,
                obj_b,
            ]
        )
        expected_grouped_objects: Dict[ObjectKind, List[ObjectId]] = {
            obj_a.get_object_kind(): [obj_a.id, obj_b.id]
        }
        expected_object_group = expected_grouped_objects[obj_a.get_object_kind()]

        actual_grouped_objects = frame_model.group_same_objects()
        actual_object_group = actual_grouped_objects[obj_a.get_object_kind()]

        self.assertEqual(1, len(list(actual_grouped_objects.keys())))
        self.assertEqual(2, len(actual_object_group))

        self.assertEqual(
            list(expected_grouped_objects.keys()),
            list(actual_grouped_objects.keys())
        )
        self.assertEqual(
            expected_object_group,
            actual_object_group
        )


if __name__ == '__main__':
    unittest.main()
