from typing import List

import numpy as np

from days.base import Day


class Day10(Day):

    def __init__(self):
        super().__init__('days/day_10/input.txt')
        self.codes_of_invalid = {')': 3, ']': 57, '}': 1197, '>': 25137}
        self.codes_of_missing = {')': 1, ']': 2, '}': 3, '>': 4}
        self.opening_to_closing = {'(': ')', '[': ']', '{': '}', '<': '>'}

    def _parse(self, line) -> (int, List[str]):
        stack = []
        opening = '([{<'
        for token in line:
            if token in opening:
                stack.append(token)
            else:
                if len(stack) == 0:
                    continue
                stack_token = stack.pop()
                expected_token = self.opening_to_closing[stack_token]
                if expected_token != token:
                    # print(F"Expected {expected_token}, but found {token} instead.")
                    return self.codes_of_invalid[token], []
        return 0, stack

    def _parse_inputs(self):
        return [self._parse(line) for line in self.input_lines]

    def _get_nonempty_stacks(self, parser_outputs):
        return [stack for _, stack in parser_outputs if len(stack) != 0]

    def _evaluate_stacks(self, stacks):
        return [self._evaluate(stack) for stack in stacks]

    def _evaluate(self, stack):
        score = 0
        while len(stack) > 0:
            score *= 5
            expected_token = self.opening_to_closing[stack.pop()]
            score += self.codes_of_missing[expected_token]
        return score

    def _get_middle_evaluation(self, evaluations):
        evals = np.array(evaluations)
        middle_index = int(evals.shape[0] / 2)
        evals = np.partition(evals, middle_index)
        return evals[middle_index]

    def part_one(self) -> int:
        parser_outputs = self._parse_inputs()
        evaluations = [code for code, _ in parser_outputs]
        return sum(evaluations)

    def part_two(self) -> int:
        parser_outputs = self._parse_inputs()
        stacks_to_evaluate = self._get_nonempty_stacks(parser_outputs)
        evaluations = self._evaluate_stacks(stacks_to_evaluate)
        middle_evaluation = self._get_middle_evaluation(evaluations)
        return middle_evaluation


if __name__ == '__main__':
    day = Day10()
    print(day.part_one())
    print(day.part_two())
