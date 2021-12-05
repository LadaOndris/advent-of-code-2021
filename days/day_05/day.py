import numpy as np

from days.base import Day


class Day05(Day):

    def __init__(self):
        super().__init__('days/day_05/input.txt')
        pairs = [line.replace('->', ',').split(',') for line in self.input_lines]
        self.coords = np.array(pairs, dtype=int)

    def _setup_field(self):
        max = np.max(self.coords) + 1
        return np.zeros([max, max], dtype=int)

    def _fill_hoz_ver_lines(self, field):
        for coord in self.coords:
            if self._is_straight_line(coord):
                if coord[0] > coord[2]:
                    field[coord[1]:coord[3] + 1, coord[2]:coord[0] + 1] += 1
                elif coord[1] > coord[3]:
                    field[coord[3]:coord[1] + 1, coord[0]:coord[2] + 1] += 1
                else:
                    field[coord[1]:coord[3] + 1, coord[0]:coord[2] + 1] += 1
        return field

    def _is_straight_line(self, line_coords):
        return line_coords[0] == line_coords[2] or line_coords[1] == line_coords[3]

    def _fill_diagonals(self, field):
        for coord in self.coords:
            if self._is_diagonal_line(coord):
                x_range = np.abs(coord[2] - coord[0])
                x_slope = np.sign(coord[3] - coord[1])
                y_slope = np.sign(coord[2] - coord[0])
                for i in range(x_range + 1):
                    field[coord[1] + i * x_slope, coord[0] + i * y_slope] += 1
        return field

    def _is_diagonal_line(self, line_coords):
        return line_coords[0] != line_coords[2] and line_coords[1] != line_coords[3]

    def _count_dangerous_points(self, field):
        return np.sum(np.where(field > 1, 1, 0))

    def part_one(self):
        field = self._setup_field()
        field = self._fill_hoz_ver_lines(field)
        return self._count_dangerous_points(field)

    def part_two(self):
        field = self._setup_field()
        field = self._fill_hoz_ver_lines(field)
        field = self._fill_diagonals(field)
        return self._count_dangerous_points(field)


if __name__ == '__main__':
    day = Day05()
    print(day.part_one())
    print(day.part_two())
