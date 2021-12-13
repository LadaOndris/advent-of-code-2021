from typing import List

import numpy as np

from days.base import Day


class Day13(Day):

    def __init__(self):
        super().__init__('days/day_13/input.txt')
        indices, self.folds = self._parse_indices_and_folds()
        max = np.max(indices) + 1
        if max % 2 == 0:
            max += 1
        self.array = np.zeros([max, max])
        self.array[indices[:, 1], indices[:, 0]] = 1
        pass

    def _parse_indices_and_folds(self) -> (np.ndarray, List):
        index_content, fold_content = self.input_content.split('\n\n')
        index_lines, fold_lines = index_content.split('\n'), fold_content.split('\n')
        indices = np.array([line.split(',') for line in index_lines]).astype(int)
        folds = []
        for fold_line in fold_lines:
            part_one, part_two = fold_line.split('=')
            folds.append([part_one[-1], int(part_two)])
        return indices, folds

    def _fold(self, array, type, index):
        if type == 'x':
            part_one, part_two = array[:, :index], array[:, index + 1:2 * index + 1]
            part_two = np.pad(part_two, [[0, 0], [0, (part_one.shape[1] - part_two.shape[1])]])
            return np.logical_or(part_one, np.flip(part_two, axis=1))
        else:
            part_one, part_two = array[:index, :], array[index + 1:2 * index + 1, :]
            part_two = np.pad(part_two, [[0, (part_one.shape[0] - part_two.shape[0])], [0, 0]])
            return np.logical_or(part_one, np.flip(part_two, axis=0))

    def part_one(self):
        array = self._fold(self.array.copy(), type=self.folds[0][0], index=self.folds[0][1])
        return np.sum(array)

    def part_two(self):
        array = self.array.copy()
        for fold_instr in self.folds:
            array = self._fold(array, type=fold_instr[0], index=fold_instr[1])
        return array  # Read it from the array


if __name__ == '__main__':
    day = Day13()
    print(day.part_one())
    print(day.part_two())
