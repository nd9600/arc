from typing import Dict, List, Tuple

from src.FrameModel.FrameModel import FrameModel
from src.Grid.Grid import Grid


class ARCDriver:
    def __init__(self, task: Dict):

        self.training_frames = self.make_frames_from_task(task, "train")
        self.test_frames = self.make_frames_from_task(task, "test")

    def make_frames_from_task(self, task, train_or_test: str) -> List[Dict[str, FrameModel]]:
        frames: List[Dict[str, FrameModel]] = []

        pairs = task[train_or_test]
        number_of_pairs = len(pairs)
        for pair_number in range(number_of_pairs):
            input_matrix = pairs[pair_number]['input']
            input_grid = Grid(input_matrix)
            input_frame_model = FrameModel.create_from_grid(input_grid)

            output_matrix = pairs[pair_number]['output']
            output_grid = Grid(output_matrix)
            output_frame_model = FrameModel.create_from_grid(output_grid)
            frames.append({
                "input": input_frame_model,
                "output": output_frame_model,
            })

        return frames
