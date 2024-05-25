import math
import random
from collections import defaultdict
from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.state import State

class next(Connect4Player):

    def __init__(self, name, depth: int = 4):
        super().__init__(name)
        self.depth = depth
        self.cache = defaultdict(lambda: None)

    def get_action(self, state: Connect4State):
        best_action = None
        acting_player = state.get_acting_player()
        best_value = -math.inf if acting_player == 0 else math.inf

        possible_actions = state.get_possible_actions()
        if not possible_actions:
            raise Exception("Nenhuma ação possível encontrada")

        for action in possible_actions:
            new_state = state.clone()
            new_state.update(action)
            value = self.minimax(new_state, self.depth - 1, -math.inf, math.inf, acting_player == 1)

            if acting_player == 0 and value > best_value:
                best_value = value
                best_action = action
            elif acting_player == 1 and value < best_value:
                best_value = value
                best_action = action

        if best_action is None:
            best_action = self.choose_random_action(possible_actions)
        
        return best_action

    def choose_random_action(self, possible_actions):
        return random.choice(possible_actions)

    def minimax(self, state: Connect4State, depth: int, alpha: float, beta: float, maximizing_player: bool):
        cached_value = self.cache[(str(state.get_grid()), depth, maximizing_player)]
        if cached_value is not None:
            return cached_value

        if depth == 0 or state.is_finished():
            evaluation = self.evaluate(state)
            self.cache[(str(state.get_grid()), depth, maximizing_player)] = evaluation
            return evaluation

        if maximizing_player:
            max_eval = -math.inf
            for action in state.get_possible_actions():
                new_state = state.clone()
                new_state.update(action)
                eval = self.minimax(new_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.cache[(str(state.get_grid()), depth, maximizing_player)] = max_eval
            return max_eval
        else:
            min_eval = math.inf
            for action in state.get_possible_actions():
                new_state = state.clone()
                new_state.update(action)
                eval = self.minimax(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.cache[(str(state.get_grid()), depth, maximizing_player)] = min_eval
            return min_eval

    def evaluate(self, state: Connect4State):
        grid = state.get_grid()
        if state._Connect4State__check_winner(0):
            return math.inf
        elif state._Connect4State__check_winner(1):
            return -math.inf
        else:
            return self.evaluate_grid(grid, state.get_acting_player())

    def evaluate_grid(self, grid, player):
        opponent = 1 if player == 0 else 0
        player_score = self.count_sequences(grid, player)
        opponent_score = self.count_sequences(grid, opponent)
        return player_score - opponent_score

    def count_sequences(self, grid, player):
        score = 0
        rows = len(grid)
        cols = len(grid[0])

        # Horizontal sequences
        for row in range(rows):
            for col in range(cols - 3):
                score += self.evaluate_window([grid[row][col + i] for i in range(4)], player)

        # Vertical sequences
        for row in range(rows - 3):
            for col in range(cols):
                score += self.evaluate_window([grid[row + i][col] for i in range(4)], player)

        # Positive diagonal sequences
        for row in range(rows - 3):
            for col in range(cols - 3):
                score += self.evaluate_window([grid[row + i][col + i] for i in range(4)], player)

        # Negative diagonal sequences
        for row in range(3, rows):
            for col in range(cols - 3):
                score += self.evaluate_window([grid[row - i][col + i] for i in range(4)], player)

        return score

    def evaluate_window(self, window, player):
        score = 0
        opponent = 1 if player == 0 else 0

        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(Connect4State.EMPTY_CELL) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(Connect4State.EMPTY_CELL) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(Connect4State.EMPTY_CELL) == 1:
            score -= 4

        return score

    def event_action(self, pos: int, action, new_state: State):
        pass

    def event_end_game(self, final_state: State):
        pass
