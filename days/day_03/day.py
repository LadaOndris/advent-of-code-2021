import numpy as np

from days.base import Day


class Day03(Day):

    def __init__(self):
        super().__init__('days/day_03/input.txt')
        input_chars = [list(line) for line in self.input_lines]
        self.numbers = np.array(input_chars).astype(np.int8)
        self.bit_columns = np.transpose(self.numbers)

    def _to_decimal(self, array):
        full_twos = np.full(array.shape[0], fill_value=2)
        to_decimal_conv = np.flip(np.cumprod(full_twos) >> 1)
        return np.sum(to_decimal_conv * array)

    def _get_most_and_least_common_bits(self, bit_columns):
        bits_sum = np.sum(bit_columns, axis=-1)
        numbers_count = np.shape(bit_columns)[1]
        most_common_bits = np.where(bits_sum >= numbers_count / 2, 1, 0)
        least_common_bits = np.logical_not(most_common_bits)
        return most_common_bits, least_common_bits

    def part_one(self):
        most_common_bits, least_common_bits = self._get_most_and_least_common_bits(self.bit_columns)
        gamma_rate = self._to_decimal(most_common_bits)
        epsilon_rate = self._to_decimal(least_common_bits)
        return gamma_rate * epsilon_rate

    def part_two(self):
        generator_candidates = self.bit_columns.copy()
        scrubber_candidates = self.bit_columns.copy()

        for column_idx in range(self.bit_columns.shape[0]):
            if generator_candidates.shape[1] > 1:
                gen_mcb, _ = self._get_most_and_least_common_bits(generator_candidates)
                gen_mask = generator_candidates[column_idx, :] == gen_mcb[column_idx]
                generator_candidates = generator_candidates[:, gen_mask]
            if scrubber_candidates.shape[1] > 1:
                _, scr_lcb = self._get_most_and_least_common_bits(scrubber_candidates)
                scr_mask = scrubber_candidates[column_idx, :] == scr_lcb[column_idx]
                scrubber_candidates = scrubber_candidates[:, scr_mask]

        generator_rating = self._to_decimal(generator_candidates[:, 0])
        scrubber_rating = self._to_decimal(scrubber_candidates[:, 0])
        return generator_rating * scrubber_rating


if __name__ == '__main__':
    day = Day03()
    print(day.part_one())
    print(day.part_two())
