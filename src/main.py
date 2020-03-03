import os
import json
from pathlib import Path

import matplotlib

from src.Grid.Grid import Grid

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def plot_task(task):
    """
    Plots the first train and test pairs of a specified task,
    using same color scheme as the ARC app
    """

    number_of_training_examples = len(task['train'])
    fig, axes_array = plt.subplots(2, number_of_training_examples, figsize = (3 * number_of_training_examples, 3 * 2))
    for task_number in range(number_of_training_examples):
        input_axis = axes_array[0, task_number]
        input_matrix = task['train'][task_number]['input']
        input_grid = Grid(input_matrix)
        input_grid.plot(input_axis, 'train input')

        output_axis = axes_array[1, task_number]
        output_matrix = task['train'][task_number]['output']
        input_grid = Grid(output_matrix)
        input_grid.plot(output_axis, 'train output')
    plt.tight_layout()
    plt.show()

    number_of_test_examples = len(task['test'])
    fig, axes_array = plt.subplots(2, number_of_test_examples, figsize=(3 * number_of_test_examples, 3 * 2))
    if number_of_test_examples == 1:
        input_axis = axes_array[0]
        input_matrix = task['test'][0]['input']
        test_input_grid = Grid(input_matrix)
        test_input_grid.plot(input_axis, 'test input')

        output_axis = axes_array[1]
        output_matrix = task['test'][0]['output']
        test_input_grid = Grid(output_matrix)
        test_input_grid.plot(output_axis, 'test output')
    else:
        for task_number in range(number_of_test_examples):
            input_axis = axes_array[0, task_number]
            input_matrix = task['test'][task_number]['input']
            test_input_grid = Grid(input_matrix)
            test_input_grid.plot(input_axis, 'test input')

            output_axis = axes_array[1, task_number]
            output_matrix = task['test'][task_number]['output']
            test_input_grid = Grid(output_matrix)
            test_input_grid.plot(output_axis, 'test output')
    plt.tight_layout()
    plt.show()


def main():
    root_path = Path(Path(__file__).parent.parent.absolute())
    data_path = root_path / "data"

    training_path = data_path / 'training'
    training_tasks = sorted(os.listdir(training_path))

    # test_path = data_path / 'test'
    # test_tasks = sorted(os.listdir(test_path))

    # evaluation_path = data_path / 'evaluation'
    # evaluation_tasks = sorted(os.listdir(evaluation_path))
    for i in [1]:
        task_file = str(training_path / training_tasks[i])

        with open(task_file, 'r') as file:
            task_json = json.load(file)

        g = task_json["train"][0]["input"]
        print(training_tasks[i])

        grid = Grid(g)
        plot_task(task_json)


if __name__== "__main__":
    main()
