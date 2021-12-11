import numpy as np

from days.base import Day


class Day11(Day):

    def __init__(self):
        super().__init__('days/day_11/input.txt')
        self.octopuses = np.array([list(line) for line in self.input_lines]).astype(int)

    def _flash(self, octopuses: np.ndarray) -> (int, np.ndarray):
        flashes_count = 0
        octopuses_to_flash = np.where(octopuses == 10, 1, 0)
        while np.sum(octopuses_to_flash) != 0:
            flashes_count += np.sum(octopuses_to_flash)
            neighbours_count = self._count_neighbours(octopuses_to_flash)
            masked_octopuses = np.where(octopuses_to_flash, 0, octopuses)
            octopuses = np.where(masked_octopuses == 0, 0, masked_octopuses + neighbours_count)
            octopuses_to_flash = np.where(octopuses >= 10, 1, 0)
        return flashes_count, octopuses

    def _count_neighbours(self, input):
        padded_input = np.pad(input, 1, constant_values=0)
        output = np.zeros(shape=[input.shape[0] + 2, input.shape[1] + 2], dtype=int)

        output[1:-1, 1:-1] += (padded_input[:-2, :-2] + padded_input[:-2, 1:-1] + padded_input[:-2, 2:] +
                               padded_input[1:-1, :-2] + padded_input[1:-1, 2:] +
                               padded_input[2:, :-2] + padded_input[2:, 1:-1] + padded_input[2:, 2:])
        return output[1:-1, 1:-1]

    def part_one(self):
        octopuses = self.octopuses.copy()
        total_flashes = 0
        steps = 100
        for step in range(steps):
            octopuses += 1
            flashes, octopuses = self._flash(octopuses)
            total_flashes += flashes
        return total_flashes

    def part_two(self):
        octopuses = self.octopuses.copy()
        step = 0
        octopuses_sum = np.sum(octopuses)
        while octopuses_sum > 0:
            octopuses += 1
            flashes, octopuses = self._flash(octopuses)
            octopuses_sum = np.sum(octopuses)
            step += 1
        return step


if __name__ == '__main__':
    day = Day11()
    print(day.part_one())
    print(day.part_two())
