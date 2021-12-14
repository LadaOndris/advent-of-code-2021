from collections import defaultdict

import numpy as np

from days.base import Day


class Day14(Day):

    def __init__(self):
        super().__init__('days/day_14/input.txt')
        self.template = self.input_lines[0]
        raw_insertions = [line.split(" -> ") for line in self.input_lines[1:]]
        self.insertions = {key: value for key, value in raw_insertions}
        self.rules = {key: [key[0] + value, value + key[1]] for key, value in raw_insertions}

    def _find_polymer(self, polymer, steps):
        for i in range(steps):
            new_polymer = np.empty(shape=len(polymer) * 2 - 1, dtype=str)
            for j in range(len(polymer) - 1):
                new_polymer[j * 2] = polymer[j]
                new_polymer[j * 2 + 1] = self.insertions[str(polymer[j:j + 2])]
            new_polymer[-1] = polymer[-1]
            polymer = ''.join(new_polymer)
        unique, counts = np.unique(list(polymer), return_counts=True)
        return np.max(counts) - np.min(counts)

    def _count_materials(self, polymer, steps):
        pair_counts = defaultdict(int)
        for i in range(len(polymer) - 1):
            pair_counts[str(polymer[i:i + 2])] += 1

        for i in range(steps):
            new_pair_counts = defaultdict(int)
            for pair, count in pair_counts.items():
                new_pairs = self.rules[pair]
                new_pair_counts[new_pairs[0]] += count
                new_pair_counts[new_pairs[1]] += count
            pair_counts = new_pair_counts

        char_counts = defaultdict(int)
        for pair, count in pair_counts.items():
            char_counts[pair[0]] += count
        char_counts[polymer[-1]] += 1
        return max(char_counts.values()) - min(char_counts.values())

    def part_one(self):
        return self._find_polymer(self.template, steps=10)

    def part_two(self):
        return self._count_materials(self.template, steps=40)


if __name__ == '__main__':
    day = Day14()
    print(day.part_one())
    print(day.part_two())
