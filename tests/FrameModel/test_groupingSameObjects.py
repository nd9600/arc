import unittest
from typing import Dict, List

from src.Types import ObjectId, ObjectKind
from src.FrameModel.FrameModel import FrameModel
from src.Grid.Grid import Grid


class TestGroupingSameObjects(unittest.TestCase):
    def test_grouping_one_object(self):
        g = [
            [0, 1, 1],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        grid = Grid(g)
        frame_model = FrameModel.create_from_grid(grid)

        obj = list(grid.parse_objects().values())[0]
        expected_grouped_objects: Dict[ObjectKind, List[ObjectId]] = {
            obj.get_object_kind(): [obj.id]
        }
        expected_object_group = expected_grouped_objects[obj.get_object_kind()]

        actual_grouped_objects = frame_model.group_same_objects()
        print(actual_grouped_objects)
        self.assertEqual(1, len(list(actual_grouped_objects.keys())))
        self.assertEqual(1, len(expected_object_group))

        self.assertEqual(
            list(expected_grouped_objects.keys()),
            list(actual_grouped_objects.keys())
        )
        self.assertEqual(
            [obj.id],
            expected_object_group
        )

    def test_grouping_two_objects(self):
        g = [
            [0, 1, 1],
            [0, 0, 0],
            [0, 0, 0],
            [1, 1, 0],
        ]
        grid = Grid(g)
        frame_model = FrameModel.create_from_grid(grid)
        obj_a = list(grid.parse_objects().values())[0]
        obj_b = list(grid.parse_objects().values())[1]
        expected_grouped_objects: Dict[ObjectKind, List[ObjectId]] = {
            obj_a.get_object_kind(): [obj_a.id, obj_b.id]
        }
        expected_object_group = expected_grouped_objects[obj_a.get_object_kind()]

        actual_grouped_objects = frame_model.group_same_objects()
        print(actual_grouped_objects)

        self.assertEqual(1, len(list(actual_grouped_objects.keys())))
        self.assertEqual(2, len(expected_object_group))

        self.assertEqual(
            list(expected_grouped_objects.keys()),
            list(actual_grouped_objects.keys())
        )
        self.assertEqual(
            [obj_a.id, obj_b.id],
            expected_object_group
        )


if __name__ == '__main__':
    unittest.main()
