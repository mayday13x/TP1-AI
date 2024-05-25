from random import choice
import math
from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.result import Connect4Result
from games.connect4.state import Connect4State
from games.state import State

class simple(Connect4Player):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: Connect4State):
        col, minimax_score = self.minimax(state, 4, False if self.get_current_pos() == 1 else True)
        for action in state.get_possible_actions():
            if action.get_col() == col:
                return action
    
    def pick_best_action(self, state: Connect4State):
        valid_locations = self.get_valid_locations(state)
        best_score = -100000000000000
        best_col = choice(valid_locations)

        for col in valid_locations:
            temp_grid = state.clone()
            temp_grid.update(Connect4Action(col))
            score = self.eval_state(temp_grid)
            if score > best_score:
                best_score = score
                best_col = col
            
        return Connect4Action(best_col)

    def minimax(self, state: Connect4State, depth: int, maximizing_player: bool):
        valid_locations = self.get_valid_locations(state)
        is_terminal = state.is_finished()
        if depth == 0 or is_terminal:
            if is_terminal:
                if state.get_result(self.get_current_pos()) == Connect4Result.WIN:
                    return (None, 100000000000000)
                elif state.get_result(self.get_current_pos()) == Connect4Result.LOOSE:
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.eval_state(state))

        if maximizing_player:
            value = -math.inf
            best_column = 0
            for col in valid_locations:
                state_clone = state.clone()
                state_clone.update(Connect4Action(col))
                new_score = self.minimax(state_clone, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    best_column = col
            return best_column, value
            
        else:  # Minimizing player
            value = math.inf
            best_column = 0
            for col in valid_locations:
                state_clone = state.clone()
                state_clone.update(Connect4Action(col))
                new_score = self.minimax(state_clone, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    best_column = col
            return best_column, value


    def eval_state(self, state):
        score = 0
        center_array = [state.get_grid()[i][state.get_num_cols() // 2] for i in range(state.get_num_rows())]
        center_count = center_array.count(self.get_current_pos())
        score += center_count * 3

        for row in range(state.get_num_rows()):
            row_array = state.get_grid()[row]
            for col in range(state.get_num_cols() - 3):
                window = row_array[col:col + 4]
                score += self.eval_window(window, self.get_current_pos())

        for col in range(state.get_num_cols()):
            col_array = [state.get_grid()[row][col] for row in range(state.get_num_rows())]
            for row in range(state.get_num_rows() - 3):
                window = col_array[row:row + 4]
                score += self.eval_window(window, self.get_current_pos())

        for row in range(state.get_num_rows() - 3):
            for col in range(state.get_num_cols() - 3):
                window = [state.get_grid()[row + i][col + i] for i in range(4)]
                score += self.eval_window(window, self.get_current_pos())

        for row in range(state.get_num_rows() - 3):
            for col in range(state.get_num_cols() - 3):
                window = [state.get_grid()[row + 3 - i][col + i] for i in range(4)]
                score += self.eval_window(window, self.get_current_pos())

        return score

    def eval_window(self, window, current_pos):
        score = 0
        opp_pos = 1 if current_pos == 0 else 0

        if window.count(current_pos) == 4:
            score += 100
        elif window.count(current_pos) == 3 and window.count(Connect4State.EMPTY_CELL) == 1:
            score += 5
        elif window.count(current_pos) == 2 and window.count(Connect4State.EMPTY_CELL) == 2:
            score += 2

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
        pass

    def event_end_game(self, final_state: State):
        pass
