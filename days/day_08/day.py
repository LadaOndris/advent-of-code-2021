from itertools import permutations
from typing import List

import numpy as np

from days.base import Day


class Day08(Day):

    def __init__(self):
        super().__init__('days/day_08/input.txt')
        signals_and_outputs = [line.split(' | ') for line in self.input_lines]
        self.signal_lines = []
        self.output_lines = []
        for signal, output in signals_and_outputs:
            self.signal_lines.append(signal.split(' '))
            self.output_lines.append(output.split(' '))
        self.segments = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
        self.numbers = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bdcf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']
        self.expected_segments = [[0, 1, 2, 4, 5, 6],
                                  [2, 5],
                                  [0, 2, 3, 4, 6],
                                  [0, 2, 3, 5, 6],
                                  [1, 2, 3, 5],
                                  [0, 1, 3, 5, 6],
                                  [0, 1, 3, 4, 5, 6],
                                  [0, 2, 5],
                                  [0, 1, 2, 3, 4, 5, 6],
                                  [0, 1, 2, 3, 5, 6]]

    def _get_lengths(self, array):
        return np.array([list(map(len, array_item)) for array_item in array])

    def part_one(self):
        lengths = self._get_lengths(self.output_lines)
        mask = (lengths == 2) | (lengths == 3) | (lengths == 4) | (lengths == 7)
        return np.sum(mask)

    def part_two(self):
        permutations = self._get_permutations()
        correct_permutations = []

        for signals in self.signal_lines:
            for permutation in permutations:
                fits = True
                for signal in signals:
                    if not self._is_number(signal, permutation):
                        fits = False
                        break
                if fits:
                    correct_permutations.append(permutation)
                    break

        result = 0
        for outputs, permutation in zip(self.output_lines, correct_permutations):
            numbers = ''
            for output in outputs:
                number = self._get_number(output, permutation)
                numbers += str(number)
            result += int(numbers)
        return result

    def _get_permutations(self):
        base = "abcdefg"
        return np.asarray(list(permutations(base)))

    def _is_number(self, signal: str, permutation) -> bool:
        number = self._get_number(signal, permutation)
        if number == -1:
            return False
        return True

    def _get_number(self, char_segments: str, permutation):
        segments = []
        for signal_char in char_segments:
            segment_id = np.argwhere(signal_char == permutation)
            segments.append(segment_id.squeeze())
        segments = np.asarray(segments)
        segments = np.sort(segments)
        number = self._arg_list_in_list_of_lists(segments, self.expected_segments)
        return number

    def _arg_list_in_list_of_lists(self, list: List[int], list_of_lists: List[List[int]]) -> int:
        for i, expected_list in enumerate(list_of_lists):
            if len(list) != len(expected_list):
                continue
            found = True
            for val1, val2 in zip(list, expected_list):
                if val1 != val2:
                    found = False
                    break
            if not found:
                continue
            return i
        return -1


if __name__ == '__main__':
    day = Day08()
    print(day.part_one())
    print(day.part_two())
