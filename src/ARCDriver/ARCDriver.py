from typing import Dict, List

from src.FrameModel.FrameModel import FrameModel
from src.Grid.Grid import Grid


class ARCDriver:
    def __init__(self, task: Dict):
        self.task = task
        self.training_frames = self.make_frames_from_task("train")
        self.test_frames = self.make_frames_from_task("test")

    def make_frames_from_task(self, train_or_test: str) -> List[Dict[str, FrameModel]]:
        frames: List[Dict[str, FrameModel]] = []

        pairs = self.task[train_or_test]
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

    @staticmethod
    def get_frame_similarity(frame_model_a: FrameModel, frame_model_b: FrameModel) -> float:
        """
        Returns how similar frame A is to frame B
        Similarity is the percentage of squares that are the same in each frame
        - the number of correct squares / the total number of squares

        If the numbers of rows or columns don't match, this returns 0 - might be too harsh

        :param frame_model_a:
        :param frame_model_b:
        :return: the percentage of squares that are the same in each frame
        """
        if (  # might be too harsh
            frame_model_a.number_of_rows != frame_model_b.number_of_rows
            or frame_model_a.number_of_columns != frame_model_b.number_of_columns
        ):
            return 0

        grid_a_array = frame_model_a.to_grid().grid_array
        grid_b = frame_model_b.to_grid()

        number_of_correct_squares = 0
        total_number_of_squares = 0
        for y, row in enumerate(grid_a_array):
            for x, square_colour_a in enumerate(row):
                if square_colour_a == grid_b.get_colour(x, y):
                    number_of_correct_squares = number_of_correct_squares + 1

                total_number_of_squares = total_number_of_squares + 1

        return number_of_correct_squares / total_number_of_squares
