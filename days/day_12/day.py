import time
from collections import defaultdict
from typing import List

from days.base import Day


class Day12(Day):

    def __init__(self):
        super().__init__('days/day_12/input.txt')
        graph = defaultdict(list)
        for line in self.input_lines:
            from_node, to_node = line.split('-')
            graph[from_node].append(to_node)
            graph[to_node].append(from_node)
        self.graph = graph

    def find_paths(self, from_node: str, to_node: str, path: List[str]):
        path = path.copy()
        path.append(from_node)

        if from_node == to_node:
            return [path]
        paths = []
        for node in self.graph[from_node]:
            if not (node.lower() == node and node in path):
                sub_paths = self.find_paths(node, to_node, path)
                paths.extend(sub_paths)
        return paths

    def find_paths_part_two(self, from_node, to_node, path):
        path = path.copy()
        path.append(from_node)

        if from_node == to_node:
            return [path]
        paths = []
        for node in self.graph[from_node]:
            sub_paths = []
            if not (node.lower() == node and node in path):
                sub_paths = self.find_paths_part_two(node, to_node, path)
            elif node.lower() == node and path.count(node) == 1 and node not in ['start', 'end']:
                sub_paths = self.find_paths(node, to_node, path)
            paths.extend(sub_paths)
        return paths

    def part_one(self):
        paths = self.find_paths('start', 'end', [])
        return len(paths)

    def part_two(self):
        paths = self.find_paths_part_two('start', 'end', [])
        return len(paths)


if __name__ == '__main__':
    day = Day12()
    print(day.part_one())
    print(day.part_two())
