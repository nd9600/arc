import numpy as np
import pandas as pd

import os
import json
from pathlib import Path

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import colors


def plotOne(ax, i, train_or_test, input_or_output):
    cmap = colors.ListedColormap(
        ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00',
         '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25'])
    norm = colors.Normalize(vmin=0, vmax=9)

    input_matrix = task[train_or_test][i][input_or_output]
    ax.imshow(input_matrix, cmap=cmap, norm=norm)
    ax.grid(True, which='both', color='lightgrey', linewidth=0.5)
    ax.set_yticks([x - 0.5 for x in range(1 + len(input_matrix))])
    ax.set_xticks([x - 0.5 for x in range(1 + len(input_matrix[0]))])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(train_or_test + ' ' + input_or_output)


def plotTask(task):
    """
    Plots the first train and test pairs of a specified task,
    using same color scheme as the ARC app
    """
    num_train = len(task['train'])
    fig, axs = plt.subplots(2, num_train, figsize=(3 * num_train, 3 * 2))
    for i in range(num_train):
        plotOne(axs[0, i], i, 'train', 'input')
        plotOne(axs[1, i], i, 'train', 'output')
    plt.tight_layout()
    plt.show()

    num_test = len(task['test'])
    fig, axs = plt.subplots(2, num_test, figsize=(3 * num_test, 3 * 2))
    if num_test == 1:
        plotOne(axs[0], 0, 'test', 'input')
        plotOne(axs[1], 0, 'test', 'output')
    else:
        for i in range(num_test):
            plotOne(axs[0, i], i, 'test', 'input')
            plotOne(axs[1, i], i, 'test', 'output')
    plt.tight_layout()
    plt.show()

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
        task = json.load(f)

    print(i)
    print(training_tasks[i])
    plotTask(task)