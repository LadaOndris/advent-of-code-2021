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
            game_idx = self._check_win(games)
            if game_idx is not None:
                remaining_values = np.sum(games[game_idx])
                return remaining_values * call
        return 0

    def _check_win(self, games) -> int:
        games_t = np.transpose(games, [0, 2, 1])
        sum_rows = np.sum(games, axis=-1)  # [100, 5]
        sum_cols = np.sum(games_t, axis=-1)  # [100, 5]
        row_wins = np.argmin(sum_rows)
        col_wins = np.argmin(sum_cols)
        row_wins_index = np.unravel_index(row_wins, sum_rows.shape)
        col_wins_index = np.unravel_index(col_wins, sum_cols.shape)
        if sum_rows[row_wins_index] == 0:
            return row_wins_index[0]
        if sum_cols[col_wins_index] == 0:
            return col_wins_index[0]
        return None

    def part_two(self):
        games = self.games.copy()
        games_active = np.ones(games.shape[0]).astype(bool)

        for call in self.calls:
            games[games == call] = 0

            game_idx = self._check_win(games[games_active])
            while game_idx is not None:
                if np.sum(games_active) == 1 and game_idx == 0:
                    win_game_idx = np.argmax(games_active)
                    remaining_values = np.sum(games[win_game_idx])
                    return remaining_values * call

                games_active_args = np.argwhere(games_active == True)
                games_active[games_active_args[game_idx]] = False
                game_idx = self._check_win(games[games_active])


if __name__ == '__main__':
    day = Day04()
    print(day.part_one())
    print(day.part_two())
