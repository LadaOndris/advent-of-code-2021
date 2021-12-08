from itertools import permutations

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
        self.expected_segments = [0b1110111, 0b0100100, 0b1011101,
                                  0b1101101, 0b0101110, 0b1101011,
                                  0b1111011, 0b0100101, 0b1111111,
                                  0b1101111]

    def _get_lengths(self, array):
        return np.array([list(map(len, array_item)) for array_item in array])

    def part_one(self):
        lengths = self._get_lengths(self.output_lines)
        mask = (lengths == 2) | (lengths == 3) | (lengths == 4) | (lengths == 7)
        return np.sum(mask)

    def part_two(self):
        signal_lines = self._array_to_binary(self.signal_lines)
        output_lines = self._array_to_binary(self.output_lines)
        correct_permutations = self._get_correct_permuations_for_signals(signal_lines)
        projected_numbers = self._apply_permutations(output_lines, correct_permutations)
        result = np.sum(projected_numbers)
        return result

    def _get_correct_permuations_for_signals(self, signal_lines):
        permutations = self._get_permutations()
        correct_permutations = []

        for signals in signal_lines:
            for permutation in permutations:
                fits = True
                for signal in signals:
                    if not self._is_digit(signal, permutation):
                        fits = False
                        break
                if fits:
                    correct_permutations.append(permutation)
                    break
        return correct_permutations

    def _apply_permutations(self, output_lines, permutations):
        numbers = np.empty(len(output_lines), dtype=np.int32)
        for i, (outputs, permutation) in enumerate(zip(output_lines, permutations)):
            number = ''
            for output in outputs:
                digit = self._get_digit(output, permutation)
                number += str(digit)
            numbers[i] = int(number)
        return numbers

    def _get_permutations(self):
        base = self._to_binary("abcdefg")
        bin_permutations = np.asarray(list(permutations(base)))
        return bin_permutations

    def _array_to_binary(self, array):
        return [[self._to_binary(a) for a in b] for b in array]

    def _to_binary(self, chars: str):
        map_dict = 1 << np.arange(7)
        converted = map_dict[np.array(list(map(ord, chars))) - ord('a')]
        return converted

    def _is_digit(self, signal: int, permutation) -> bool:
        number = self._get_digit(signal, permutation)
        if number == -1:
            return False
        return True

    def _get_digit(self, bin_segments: int, permutation):
        segments_in_permutation = np.bitwise_and(bin_segments[:, np.newaxis],
                                                 permutation[np.newaxis, :])  # shape [bin_segments.len, 7]
        segments_locations = np.argmax(segments_in_permutation, axis=-1)
        number_representation = np.bitwise_or.reduce(1 << segments_locations)
        number = np.where(number_representation == self.expected_segments)[0]
        if number.shape[0] == 0:
            return -1
        return number[0]


if __name__ == '__main__':
    day = Day08()
    print(day.part_one())
    print(day.part_two())
