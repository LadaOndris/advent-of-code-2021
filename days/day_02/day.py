from days.base import Day


class Day02(Day):

    def __init__(self):
        super().__init__('days/day_02/input.txt')

    def yield_commands(self):
        for command_line in self.input_lines:
            command, value = command_line.split(' ')
            value = int(value)
            yield command, value

    def part_one(self):
        position = 0
        depth = 0
        for command, value in self.yield_commands():
            if command == 'forward':
                position += value
            elif command == 'down':
                depth += value
            elif command == 'up':
                depth -= value
        return depth * position

    def part_two(self):
        position = 0
        depth = 0
        aim = 0
        for command, value in self.yield_commands():
            if command == 'forward':
                position += value
                depth += aim * value
            elif command == 'down':
                aim += value
            elif command == 'up':
                aim -= value
        return depth * position


if __name__ == '__main__':
    day = Day02()
    print(day.part_one())
    print(day.part_two())
