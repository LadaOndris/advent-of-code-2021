import numpy as np
from scipy.ndimage import measurements

from days.base import Day


class Day09(Day):

    def __init__(self):
        super().__init__('days/day_09/input.txt')
        self.input = np.array([list(line) for line in self.input_lines]).astype(int)

    def _count_larger_neighbours(self):
        input = self.input
        output = np.zeros(shape=[input.shape[0] + 2, input.shape[1] + 2])
        bordered_input = np.full(shape=[input.shape[0] + 2, input.shape[1] + 2], fill_value=9)
        bordered_input[1:-1, 1:-1] = input

        output[:-1, :] += bordered_input[1:, :] > bordered_input[:-1, :]
        output[1:, :] += bordered_input[:-1, :] > bordered_input[1:, :]
        output[:, :-1] += bordered_input[:, 1:] > bordered_input[:, :-1]
        output[:, 1:] += bordered_input[:, :-1] > bordered_input[:, 1:]

        return output, bordered_input

    def part_one(self):
        output, bordered_input = self._count_larger_neighbours()
        inputs = bordered_input[output == 4]
        return np.sum(inputs + 1)

    def _get_area_sizes(self, array) -> np.ndarray:
        structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        labeled_areas, num_areas = measurements.label(array, structure)
        area_sizes = np.zeros(shape=num_areas)
        for area_idx in range(1, num_areas + 1):
            count = np.sum(labeled_areas == area_idx)
            area_sizes[area_idx - 1] = count
        return area_sizes

    def _get_three_largest_areas(self, area_sizes):
        sorted_area_sizes = np.sort(area_sizes)
        return sorted_area_sizes[-3:]

    def part_two(self):
        area_sizes = self._get_area_sizes(self.input < 9)
        largest_area_sizes = self._get_three_largest_areas(area_sizes)
        return np.prod(largest_area_sizes).astype(int)


if __name__ == '__main__':
    day = Day09()
    print(day.part_one())
    print(day.part_two())
