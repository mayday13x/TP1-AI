from operator import index, indexOf
from random import choice
from re import sub
from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State


class teste2(MinesweeperPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: MinesweeperState):
        grid = state.get_grid()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()
        possible_actions = list(state.get_possible_actions())

        # IMPLEMENTATION ALGORITHM 
        # {set} -> count
        # {set} = 0 -> {set} is safe
        # {set}.len = count -> set() is mine
        # if (*,*) is safe -> {(*,*)}.pop
        # if (*,*) is mine -> {(*,*)}.pop -> count -= 1
        # if {set1} is subset of {set2} -> {set2} - {set1} = count2 - count1
        
        # a cada set() é associado um count
        # se o count for 0, então o set() é seguro
        # se o count for igual ao tamanho do set(), então o set() é uma bomba
        # se o set() for uma bomba, então o count é decrementado
        # se o set() for seguro, então o set() é removido
        # se o set1 for um subconjunto de set2, então set2 - set1 = count2 - count1

        scored_actions = []              

        for r in range(num_rows):   #scoring
            for c in range(num_cols):
                cell = grid[r][c]
                if cell == 0:
                    neighbors = set(teste2.get_unrevealed_neighbors(grid, r, c, num_rows, num_cols))
                    scored_actions.append((0, neighbors))

                if cell > 0:
                    mines_count = 0
                    unrevealed_neighbors = set(teste2.get_unrevealed_neighbors(grid, r, c, num_rows, num_cols))
                    neighbors = set(teste2.get_neighbors(grid, r, c, num_rows, num_cols))
                    for neighbor in neighbors:
                        _row, _col = neighbor
                        if grid[_row][_col] == MinesweeperState.MINE_CELL:
                            mines_count += 1
                            
                    if unrevealed_neighbors:
                        scored_actions.append((cell - mines_count, unrevealed_neighbors))
                   
        has_subset = True   # check for subsets
        while has_subset:
            has_subset = False                   
            for i, score in enumerate(scored_actions.copy()):
                for j, other in enumerate(scored_actions.copy()):

                    for score in scored_actions:    # clean empty sets
                        if not score[1]:        
                            scored_actions.remove(score)
                            
                        if i != j:
                            if score[1] == other[1]:
                                pass
                            elif  score[1].issubset(other[1]):
                                scored_actions.append((other[0] - score[0], other[1] - score[1]))
                                scored_actions.remove(other)
                                has_subset = True
                                break

        for score in scored_actions:
            if scored_actions:          #Choose action with lowest score
                mini = (min(scored_actions, key=lambda x: x[0])[1])
                return MinesweeperAction(mini.copy().pop()[0], mini.copy().pop()[1])

        for action in possible_actions:
            row = action.get_row()
            col = action.get_col()
            if teste2.count_unrevealed_neighbors(grid, row, col, num_rows, num_cols) == 8:
                    return action
            
            return choice(possible_actions)
        #return action
                

    @staticmethod
    def is_safe_reveal(grid, row, col, num_rows, num_cols):
        if grid[row][col] != MinesweeperState.EMPTY_CELL:
            return False  # Cell already revealed or marked

        # Check all neighbors for mine indicators
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if grid[r][c] > 0:  # Cell is a number
                    if teste2.count_unrevealed_neighbors(grid, r, c, num_rows, num_cols) == grid[r][c]:
                        return True  # Safe to reveal
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
            risk = teste2.count_unrevealed_neighbors(grid, row, col, num_rows, num_cols)

        return risk

    @staticmethod
    def get_unrevealed_neighbors(grid, row, col, num_rows, num_cols):
        
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if (r, c) != (row, col) and grid[r][c] == MinesweeperState.EMPTY_CELL:
                    yield (r, c)

    @staticmethod
    def get_neighbors(grid, row, col, num_rows, num_cols):
        
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if (r, c) != (row, col):
                    yield (r, c)
    
    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
