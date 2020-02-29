import numpy as np
import pandas as pd

import os
import json
from pathlib import Path

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import colors


def plot_grid(axes, input_matrix, title = "") -> None:
    colour_map = colors.ListedColormap(
        ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00', '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25']
    )
    norm = colors.Normalize(vmin = 0, vmax = 9)

    axes.imshow(input_matrix, cmap = colour_map, norm = norm)
    axes.grid(True, which = 'both', color = 'lightgrey', linewidth = 0.5)
    axes.set_yticks([x - 0.5 for x in range(1 + len(input_matrix))])
    axes.set_xticks([x - 0.5 for x in range(1 + len(input_matrix[0]))])
    axes.set_xticklabels([])
    axes.set_yticklabels([])
    if len(title) > 0:
        axes.set_title(title)


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
        plot_grid(input_axis, input_matrix, 'train input')

        output_axis = axes_array[1, task_number]
        output_matrix = task['train'][task_number]['output']
        plot_grid(output_axis, output_matrix, 'train output')
    plt.tight_layout()
    plt.show()

    # number_of_test_examples = len(task['test'])
    # fig, axes_array = plt.subplots(2, number_of_test_examples, figsize=(3 * number_of_test_examples, 3 * 2))
    # if number_of_test_examples == 1:
    #     input_axis = axes_array[0]
    #     input_matrix = task['test'][0]['input']
    #     plot_grid(input_axis, input_matrix, 'test input')
    #
    #     output_axis = axes_array[1]
    #     output_matrix = task['test'][0]['output']
    #     plot_grid(output_axis, output_matrix, 'test output')
    # else:
    #     for task_number in range(number_of_test_examples):
    #         input_axis = axes_array[0, task_number]
    #         input_matrix = task['test'][task_number]['input']
    #         plot_grid(input_axis, input_matrix, 'test input')
    #
    #         output_axis = axes_array[1, task_number]
    #         output_matrix = task['test'][task_number]['output']
    #         plot_grid(output_axis, output_matrix, 'test output')
    # plt.tight_layout()
    # plt.show()


rootPath = Path("../")
data_path = rootPath / "data"
training_path = data_path / 'training'
evaluation_path = data_path / 'evaluation'
test_path = data_path / 'test'

training_tasks = sorted(os.listdir(training_path))
evaluation_tasks = sorted(os.listdir(evaluation_path))
for i in range(1):
    task_file = str(training_path / training_tasks[i])

    with open(task_file, 'r') as f:
        task_json = json.load(f)

    print(i)
    print(training_tasks[i])
    plot_task(task_json)
