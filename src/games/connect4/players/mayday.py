from random import randint, choice

from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.state import State


class simple22(Connect4Player):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: Connect4State):

        return self.pick_best_action(state)
    

    def pick_best_action(self, state: Connect4State):
        valid_locations = self.get_valid_locations(state)
        best_score = -100000
        best_col = choice(valid_locations)

        for col in valid_locations:
            temp_grid = state.clone()
            temp_grid.update(Connect4Action(col))
            score = self.eval_state(temp_grid)
            if score > best_score:
                best_score = score
                best_col = col
            
        return Connect4Action(best_col)

    def eval_state(self, state):    # Heuristic function
        score = 0

        # Score center column
        center_array = [state.get_grid()[i][state.get_num_cols()//2] for i in range(state.get_num_rows())]
        center_count = center_array.count(self.get_current_pos())
        score += center_count * 6

        # HORZONTAL
        for row in range(state.get_num_rows()):
            row_array = state.get_grid()[row]
            for col in range(state.get_num_cols() - 3):
                window = row_array[col:col + 4] #slice from col to col+3
                score += self.eval_window(window, self.get_current_pos())

        # VERTICAL
        for col in range(state.get_num_cols()):
            col_array = [state.get_grid()[row][col] for row in range(state.get_num_rows())]
            for row in range(state.get_num_rows() - 3):
                window = col_array[row:row + 4] 
                score += self.eval_window(window, self.get_current_pos())

        # DIAGONAL POSITIVE SLOPE
        for row in range(state.get_num_rows() - 3):
            for col in range(state.get_num_cols() - 3):
                window = [state.get_grid()[row + i][col + i] for i in range(4)]
                score += self.eval_window(window, self.get_current_pos())

        # DIAGONAL NEGATIVE SLOPE
        for row in range(state.get_num_rows() - 3):
            for col in range(state.get_num_cols() - 3):
                window = [state.get_grid()[row + 3 - i][col + i] for i in range(4)]
                score += self.eval_window(window, self.get_current_pos())

        return score
       

    def eval_window(self, window, current_pos):
        score = 0
        opp_pos = 1 if current_pos == 0 else 0  # get opponent's position

        if window.count(current_pos) == 4:
            score += 100
        elif window.count(current_pos) == 3 and window.count(Connect4State.EMPTY_CELL) == 1:
            score += 10
        elif window.count(current_pos) == 2 and window.count(Connect4State.EMPTY_CELL) == 2:
            score += 5

        if window.count(opp_pos) == 3 and window.count(Connect4State.EMPTY_CELL) == 1:
            score -= 80

        return score
    
    def get_valid_locations(self, state: Connect4State):
        valid_locations = []
        for col in range(state.get_num_cols()):
            if state.validate_action(Connect4Action(col)):
                valid_locations.append(col)
        return valid_locations

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
