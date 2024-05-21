from operator import index, indexOf
from re import sub
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State


class teste(MinesweeperPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: MinesweeperState):
        grid = state.get_grid()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()
        possible_actions = list(state.get_possible_actions())

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
        # se o set() for seguro, então o set() é removido ************ X
        # se o set1 for um subconjunto de set2, então set2 - set1 = count2 - count1

        scored_actions = []
        
        for score in scored_actions:
            if not score[1]:        # clean empty sets
                print(f"poped -> {score}")
                scored_actions.remove(score)  
               

        for r in range(num_rows):   #scoring
            for c in range(num_cols):
                cell = grid[r][c]
                if cell == 0:
                    neighbors = set(teste.get_unrevealed_neighbors(grid, r, c, num_rows, num_cols))
                    scored_actions.append((0, neighbors))
                    #scored_actions.extend((0,neighbors))

                if cell > 0:
                    mines_count = 0
                    unrevealed_neighbors = set(teste.get_unrevealed_neighbors(grid, r, c, num_rows, num_cols))
                    neighbors = set(teste.get_neighbors(grid, r, c, num_rows, num_cols))
                    #neighbors_copy = neighbors.copy()
                    for neighbor in neighbors:
                        _row, _col = neighbor
                        if grid[_row][_col] == MinesweeperState.MINE_CELL:
                            mines_count += 1
                            
                    if unrevealed_neighbors:
                        scored_actions.append((cell - mines_count, unrevealed_neighbors))
                   
                            
        scored_actions_copy = scored_actions.copy()  # Create a copy to avoid modifying the original list while iterating
        for i, score in enumerate(scored_actions_copy):
            for j, other in enumerate(scored_actions_copy):
                if i != j and score[0] > 0:

                    if len(score[1].intersection(other[1])) == len(score[1]):
                        pass
                    elif  score[1].issubset(other[1]):
                        print(f"existeeee: {score[1]} ------ {other[1]}\n")
                        scored_actions.append((other[0] - score[0], other[1] - score[1]))
                        scored_actions.remove(other)

        for score in scored_actions:
            if not score[1]:
                print(f"poped -> {score}")
                scored_actions.remove(score) 
    
        for score in scored_actions:
            print(f"score: {score}\n")

        for action in possible_actions:
                if scored_actions:
                    mini = (min(scored_actions, key=lambda x: x[0])[1])  # Choose action with lowest score
                    if mini:
                        _row, _col = action.get_row(), action.get_col()
                        if _row == mini.copy().pop()[0] and _col == mini.copy().pop()[1]:
                            return action
        return action
                

    @staticmethod
    def is_safe_reveal(grid, row, col, num_rows, num_cols):
        if grid[row][col] != MinesweeperState.EMPTY_CELL:
            return False  # Cell already revealed or marked

        # Check all neighbors for mine indicators
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if grid[r][c] > 0:  # Cell is a number
                    if teste.count_unrevealed_neighbors(grid, r, c, num_rows, num_cols) == grid[r][c]:
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
            risk = teste.count_unrevealed_neighbors(grid, row, col, num_rows, num_cols)

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
