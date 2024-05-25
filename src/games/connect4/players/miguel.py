from calendar import c
import math
from random import randint, choice

from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.result import Connect4Result
from games.connect4.state import Connect4State
from games.state import State


class MiguelConnect4Player(Connect4Player):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: Connect4State):
        col, value = self.minimax(state, 3, -math.inf, math.inf, True)
        
        if col is None:
            raise Exception("There is no valid action")

        return Connect4Action(col)
        #return self.pick_best_action(state)
    

    def minimax(self, state: Connect4State, depth: int, alpha: float, beta: float, max_player: bool):
        '''if depth == 0 or state.is_finished():
            return (None, self.eval_state(state))'''
        if state.is_finished():
            if state.get_result(self.get_current_pos()) == Connect4Result.WIN.value:
                #print("WIN")
                return (None, 100000)
            elif state.get_result(self.get_current_pos()) == Connect4Result.LOOSE.value:
                #print("LOOSE")
                #for row in state.get_grid():
                    #print(f"{row}\n")
                return (None, -100000)
            else:
                return (None, 0)
        if depth == 0:
            return (None, self.eval_state(state))
        
        if max_player:
            value = -math.inf
            best_col = 3 ## ou random
            for action in state.get_possible_actions():
                state_clone = state.clone()
                state_clone.update(action)
                new_value = self.minimax(state_clone, depth - 1, alpha, beta, False)[1]
                if new_value > value:
                    value = new_value
                    best_col = action.get_col()

                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return (best_col, value)
        
        else:
            value = math.inf
            for action in state.get_possible_actions():
                state_clone = state.clone()
                state_clone.update(action)
                new_value = self.minimax(state_clone, depth - 1, alpha, beta, True)[1]
                if new_value < value:
                    value = new_value
                    best_col = action.get_col()
                
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return (best_col, value)
    

    def pick_best_action(self, state: Connect4State):
        valid_locations = self.get_valid_locations(state)
        best_score = -100000000
        best_col = choice(valid_locations)

        for col in valid_locations:
            temp_grid = state.clone()
            temp_grid.update(Connect4Action(col))
            score = self.eval_state(temp_grid)
            print(score, col)
            if score > best_score:
                best_score = score
                best_col = col
            
        return Connect4Action(best_col)

    def eval_state(self, state):    # Heuristic function
        score = 0

        # Score center column
        grid = state.get_grid()
        num_cols = state.get_num_cols()
        num_rows = state.get_num_rows()

        center_array = [grid[i][num_cols//2] for i in range(num_rows)]
        center_count = center_array.count(self.get_current_pos())
        score += center_count * 3

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

        # DIAGONAL PARA CIMA    
        for row in range(state.get_num_rows() - 3):
            for col in range(state.get_num_cols() - 3):
                window = [state.get_grid()[row + i][col + i] for i in range(4)]
                score += self.eval_window(window, self.get_current_pos())

        # DIAGONAL PARA BAIXO
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
            score += 5
        elif window.count(current_pos) == 2 and window.count(Connect4State.EMPTY_CELL) == 2:
            score += 2
        if window.count(opp_pos) == 3 and window.count(Connect4State.EMPTY_CELL) == 1:
            score -= 4

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
