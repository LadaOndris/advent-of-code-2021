import numpy as np

from days.base import Day


class Day01(Day):

    def __init__(self):
        super().__init__('days/day_01/input.txt')
        self.input = np.array(self.input_lines).astype(int)

    def get_increasing_count(self, sequence):
        diff = sequence[1:] - sequence[:-1]
        num_increasing = np.sum(diff > 0)
        return num_increasing

    def part_one(self):
        return self.get_increasing_count(self.input)

    def part_two(self):
        groups_sums = self.input[0:-2] + self.input[1:-1] + self.input[2:]
        return self.get_increasing_count(groups_sums)


if __name__ == '__main__':
    day = Day01()
    print(day.part_one())
    print(day.part_two())
