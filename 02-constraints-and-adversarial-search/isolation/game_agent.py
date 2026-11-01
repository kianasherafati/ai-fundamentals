"""
This file contains all the classes and functions that need to be
implemented for the second part of the project (Isolation Game).
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    """
    Heuristic 1: Simple Move Difference
    Calculates the difference between the number of available moves for the player
    and the opponent.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

def custom_score_2(game, player):
    """
    Heuristic 2: Aggressive Move Difference
    Weights the opponent's moves more heavily to force them into corners.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 2 * opp_moves)

def custom_score_3(game, player):
    """
    Heuristic 3: Center Control + Move Difference
    Rewards occupying the center of the board, which usually offers more mobility.
    """
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    w, h = game.width, game.height
    y, x = game.get_player_location(player)
    center_y, center_x = h / 2, w / 2
    
    # Calculate distance from center
    dist = ((y - center_y)**2 + (x - center_x)**2) ** 0.5
    max_dist = ((h/2)**2 + (w/2)**2) ** 0.5
    
    # Maximize moves difference and minimize distance to center (maximize 1 - normalized_dist)
    return float((own_moves - opp_moves) + (1 - dist/max_dist))

class IsolationPlayer:
    """Base class for minimax and alphabeta agents."""
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax search."""

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        """
        self.time_left = time_left
        best_move = (-1, -1)
        
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return best_move
        best_move = legal_moves[0] # Initialize with a valid move

        try:
            return self.minimax(game, self.search_depth)
        except SearchTimeout:
            print(f"Timeout occurred at depth {self.search_depth}!")
            return best_move # Return the best move found so far

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm."""
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        best_move = legal_moves[0]
        best_score = float("-inf")

        for move in legal_moves:
            next_game = game.forecast_move(move)
            score = self.min_value(next_game, depth - 1)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move

    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)

        v = float("-inf")
        for move in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(move), depth - 1))
        return v

    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)
            
        v = float("inf")
        for move in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(move), depth - 1))
        return v

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning.
    """

    def get_move(self, game, time_left):
        self.time_left = time_left
        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return best_move
        best_move = legal_moves[0]

        try:
            # Iterative Deepening: Start at depth 1 and increase
            depth = 1
            while True:
                move = self.alphabeta(game, depth)
                if move != (-1, -1):
                    best_move = move
                depth += 1
        except SearchTimeout:
            # Time is up! Return the best move found in the deepest completed search
            return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        best_move = legal_moves[0]
        v = float("-inf")
        
        for move in legal_moves:
            score = self.min_value(game.forecast_move(move), depth - 1, alpha, beta)
            if score > v:
                v = score
                best_move = move
            alpha = max(alpha, v)
            if v >= beta:
                break # Pruning
        return best_move

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)

        v = float("-inf")
        for move in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(move), depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)

        v = float("inf")
        for move in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(move), depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

class ExpectimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited expectimax."""

    def get_move(self, game, time_left):
        self.time_left = time_left
        legal_moves = game.get_legal_moves()
        if not legal_moves: return (-1, -1)
        best_move = legal_moves[0]
        
        try:
            return self.expectimax(game, self.search_depth)
        except SearchTimeout:
            return best_move

    def expectimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()
        
        legal_moves = game.get_legal_moves()
        if not legal_moves: return (-1, -1)
        
        best_move = legal_moves[0]
        best_score = float("-inf")
        
        for move in legal_moves:
            score = self.exp_value(game.forecast_move(move), depth - 1)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)
        
        v = float("-inf")
        for move in game.get_legal_moves():
            v = max(v, self.exp_value(game.forecast_move(move), depth - 1))
        return v

    def exp_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD: raise SearchTimeout()
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)
        
        v = 0.0
        moves = game.get_legal_moves()
        prob = 1.0 / len(moves) # Assuming uniform probability for chance nodes
        for move in moves:
            v += prob * self.max_value(game.forecast_move(move), depth - 1)
        return v