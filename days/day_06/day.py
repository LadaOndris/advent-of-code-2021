import numpy as np

from days.base import Day


class Day06(Day):

    def __init__(self):
        super().__init__('days/day_06/input.txt')
        self.lanterns = np.array(self.input_lines[0].split(','), dtype=int)

    def part_one(self):
        days = 80
        lanterns = self.lanterns.copy()
        for day in range(days):
            zero_lanterns = np.where(lanterns == 0)
            count_zeros = len(zero_lanterns[0])
            lanterns[zero_lanterns] = 7
            lanterns -= 1
            spawned_lanterns = np.full(count_zeros, fill_value=8)
            lanterns = np.concatenate([lanterns, spawned_lanterns], axis=-1)
        return lanterns.shape[0]

    def part_two(self):
        days = 256
        lifetimes = np.arange(9)
        lanters_grouped = {lifetime: 0 for lifetime in lifetimes}
        for lantern in self.lanterns:
            lanters_grouped[lantern] += 1

        for day in range(days):
            zero_lanterns = lanters_grouped[0]
            for lifetime in lifetimes[1:]:
                lanters_grouped[lifetime - 1] = lanters_grouped[lifetime]
            lanters_grouped[6] += zero_lanterns
            lanters_grouped[8] = zero_lanterns

        return sum(lanters_grouped.values())


if __name__ == '__main__':
    day = Day06()
    print(day.part_one())
    print(day.part_two())
