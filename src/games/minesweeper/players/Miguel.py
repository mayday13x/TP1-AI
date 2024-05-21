from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State


class MiguelMinesweeperPlayer(MinesweeperPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: MinesweeperState):
        grid = state.get_grid()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()
        possible_actions = list(state.get_possible_actions())

        scored_actions = []
        for action in possible_actions:
            for r in range(num_rows):
                for c in range(num_cols):
                    cell = grid[r][c]
                    #se a célula é 0's pode jogar à volta dessa célula pois não vai ter bomba
                    if cell == 0:
                        neighbors = list(MiguelMinesweeperPlayer.get_neighbors(grid, r, c, num_rows, num_cols))
                        for neighbor in neighbors:
                            _row, _col = neighbor
                           # print(f"safe: neighbor: {_row}, {_col}")
                            if _row == action.get_row() and _col == action.get_col():
                                return action
                            
            row, col = action.get_row(), action.get_col()
            risk = self.calculate_risk(grid, action, num_rows, num_cols)
            # Prioritize exploration over guaranteed safety for some actions
            exploration_factor = 0.2  # Adjust this factor as needed
            score = risk + (exploration_factor if self.is_interesting_exploration(grid, row, col, num_rows, num_cols) else 0)
            scored_actions.append((action, score))

        return min(scored_actions, key=lambda x: x[1])[0]  # Choose action with lowest score


    @staticmethod
    def get_neighbors(grid, row, col, num_rows, num_cols):
        
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                yield (r, c)

    @staticmethod
    def is_interesting_exploration(grid, row, col, num_rows, num_cols):
        # Explore near revealed numbers, edges of revealed areas, or isolated cells
        if grid[row][col] == MinesweeperState.EMPTY_CELL:
            # Near revealed numbers
            for r in range(max(0, row - 1), min(num_rows, row + 2)):
                for c in range(max(0, col - 1), min(num_cols, col + 2)):
                    if grid[r][c] > 0:
                        return True
            # Edges of revealed areas
            if (row == 0 or row == num_rows - 1 or col == 0 or col == num_cols - 1):
                return True
            # Isolated cells (careful, can be risky)
            if MiguelMinesweeperPlayer.count_unrevealed_neighbors(grid, row, col, num_rows, num_cols) == 8:
                return True
        return False

    @staticmethod
    def count_unrevealed_neighbors(grid, row, col, num_rows, num_cols):
        count = 0
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if (r != row or c != col) and grid[r][c] == MinesweeperState.EMPTY_CELL:
                    count += 1
        return count

    @staticmethod
    def calculate_risk(grid, action, num_rows, num_cols):
        row, col = action.get_row(), action.get_col()
        if grid[row][col] != MinesweeperState.EMPTY_CELL:
            return float('inf')  # Already revealed or marked

        risk = 0
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if grid[r][c] > 0:  # Cell is a number
                    risk += grid[r][c]

        # If no risk indication from neighbors, consider the number of unrevealed neighbors as a fallback risk measure
        if risk == 0:
            risk = MiguelMinesweeperPlayer.count_unrevealed_neighbors(grid, row, col, num_rows, num_cols)

        return risk

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
