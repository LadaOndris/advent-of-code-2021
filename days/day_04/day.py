import numpy as np

from days.base import Day


class Day04(Day):

    def __init__(self):
        super().__init__('days/day_04/input.txt')
        self.calls = np.array(self.input_lines[0].split(',')).astype(int)
        games_lines = self.input_lines[1:]
        games_numbers = np.concatenate([list(filter(None, line.split(' '))) for line in games_lines])
        self.games = np.reshape(games_numbers, [-1, 5, 5]).astype(int)

    def part_one(self):
        games = self.games.copy()
        for call in self.calls:
            games[games == call] = 0
            win_games_idx = self._find_win_games(games)
            if win_games_idx.size != 0:
                remaining_values = np.sum(games[win_games_idx[0]])
                return remaining_values * call
        return 0

    def _find_win_games(self, games) -> np.ndarray:
        games_t = np.transpose(games, [0, 2, 1])
        sum_rows = np.sum(games, axis=-1)  # [100, 5]
        sum_cols = np.sum(games_t, axis=-1)  # [100, 5]
        rows_cols_sums = np.concatenate([sum_rows, sum_cols], axis=-1)
        win_games, win_row_cols = np.where(rows_cols_sums == 0)
        return win_games

    def part_two(self):
        games = self.games.copy()
        games_active = np.ones(games.shape[0]).astype(bool)

        for call in self.calls:
            games[games == call] = 0

            win_games_idx = self._find_win_games(games[games_active])
            if win_games_idx.size != 0:
                if np.sum(games_active) == 1:
                    win_game_idx = np.argmax(games_active)
                    remaining_values = np.sum(games[win_game_idx])
                    return remaining_values * call

                games_active_args = np.argwhere(games_active)
                games_active[games_active_args[win_games_idx]] = False


if __name__ == '__main__':
    day = Day04()
    print(day.part_one())
    print(day.part_two())
