import numpy as np

from days.base import Day


class Day07(Day):

    def __init__(self):
        super().__init__('days/day_07/input.txt')
        self.numbers = np.array(self.input_lines[0].split(','), dtype=int)

    def _get_distances(self):
        numbers = self.numbers[:, np.newaxis]
        candidates = np.arange(numbers.shape[0])[np.newaxis, :]
        numbers_diffs = np.abs(candidates - numbers)
        return numbers_diffs

    def _find_minimum_distance_sum(self, distances):
        candidate_sums = np.sum(distances, axis=0)
        min_fuel = np.min(candidate_sums)
        return min_fuel

    def _adjust_distances(self, distances):
        return distances / 2 * (1 + distances)

    def part_one(self):
        distances = self._get_distances()
        min_fuel = self._find_minimum_distance_sum(distances)
        return min_fuel

    def part_two(self):
        distances = self._get_distances()
        distances = self._adjust_distances(distances)
        min_fuel = self._find_minimum_distance_sum(distances.astype(int))
        return min_fuel


if __name__ == '__main__':
    day = Day07()
    print(day.part_one())
    print(day.part_two())
