import numpy as np

from days.base import Day


class AStar:

    def __init__(self, graph):
        self.graph = graph

    def _h(self, node):
        return self.graph[node[0], node[1]]

    def eval_nodes(self, nodes):
        return [self.graph[node[0], node[1]] for node in nodes]

    def _get_neighbours(self, node):
        neighbours = []
        if node[0] > 0:
            neighbours.append((node[0] - 1, node[1]))
        if node[1] > 0:
            neighbours.append((node[0], node[1] - 1))
        if node[1] < self.graph.shape[1] - 1:
            neighbours.append((node[0], node[1] + 1))
        if node[0] < self.graph.shape[0] - 1:
            neighbours.append((node[0] + 1, node[1]))
        weights = self.eval_nodes(neighbours)
        return zip(neighbours, weights)

    def compute(self, start, stop):
        open_lst = {start}
        closed_lst = set()
        distance_from_start = {start: 0}
        adjacent_mappings = {start: start}

        while len(open_lst) > 0:
            current = None

            for v in open_lst:
                if current is None or distance_from_start[v] + self._h(v) < distance_from_start[current] + self._h(
                        current):
                    current = v

            if current is None:
                print('Path does not exist!')
                return None

            if current == stop:
                reconst_path = []
                while adjacent_mappings[current] != current:
                    reconst_path.append(current)
                    current = adjacent_mappings[current]

                reconst_path.append(start)
                reconst_path.reverse()
                return reconst_path

            for (neighbour, weight) in self._get_neighbours(current):
                if neighbour not in open_lst and neighbour not in closed_lst:
                    open_lst.add(neighbour)
                    adjacent_mappings[neighbour] = current
                    distance_from_start[neighbour] = distance_from_start[current] + weight
                elif distance_from_start[neighbour] > distance_from_start[current] + weight:
                    distance_from_start[neighbour] = distance_from_start[current] + weight
                    adjacent_mappings[neighbour] = current

                    if neighbour in closed_lst:
                        closed_lst.remove(neighbour)
                        open_lst.add(neighbour)
            open_lst.remove(current)
            closed_lst.add(current)


class Day15(Day):

    def __init__(self):
        super().__init__('days/day_15/input.txt')
        self.graph = np.array([list(line) for line in self.input_lines]).astype(int)

    def _construct_full_map(self):
        height = self.graph.shape[0]
        width = self.graph.shape[1]
        full_graph = np.empty(shape=[height * 5, width * 5])

        for row in range(5):
            for col in range(5):
                updated_tile = (self.graph + (row + col))
                updated_tile[updated_tile > 9] -= 9
                full_graph[row * height:row * height + height, col * width:col * width + width] = updated_tile
        return full_graph.astype(int)

    def part_one(self):
        astar = AStar(self.graph)
        path = astar.compute((0, 0), (self.graph.shape[0] - 1, self.graph.shape[1] - 1))
        weights = astar.eval_nodes(path)[1:]
        return sum(weights)

    def part_two(self):
        full_graph = self._construct_full_map()
        astar = AStar(full_graph)
        path = astar.compute((0, 0), (full_graph.shape[0] - 1, full_graph.shape[1] - 1))
        weights = astar.eval_nodes(path)[1:]
        return sum(weights)


if __name__ == '__main__':
    day = Day15()
    print(day.part_one())
    print(day.part_two())
