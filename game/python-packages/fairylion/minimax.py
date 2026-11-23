COLOR_GREEN = "\033[1;32;42m"
COLOR_RESET = "\033[0m"

import time
import fairylion.CONSTANT as c

class MinimaxSearchMixin:
    
    def think_minimax(self, time_limit=2.0, max_depth=10):
        """
        Iterative deepening Minimax with Alpha-Beta pruning.
        """
        self.nodes_searched = 0
        best_move = None
        start_time = time.time()
        
        # Iterative Deepening
        for depth in range(1, max_depth + 1):
            if time.time() - start_time > time_limit and best_move is not None:
                print(f"depth: {depth} time:{time.time() - start_time:.1f}.")
                break
                
            result = self._alphabeta_root(depth, float('-inf'), float('inf'), self.side == 0, start_time, time_limit, best_move)
            if result is None:  # Aborted due to time limit
                print(f"{COLOR_GREEN}depth: {depth} t:{time.time() - start_time:.1f}{COLOR_RESET}")
                break
                
            current_best_move, score = result
            
            if current_best_move:
                best_move = current_best_move
                print(f"Depth {depth}. Best move: {best_move}, s: {score}")
                
            # Stop early if we found a forced mate
            if abs(score) >= c.MAX_SCORE - 100:
                print("Forced mate found, stopping search.")
                break
            
        print(f"Total nodes searched: {self.nodes_searched}")
        return best_move

    def _alphabeta_root(self, depth, alpha, beta, maximizing_player, start_time, time_limit, prev_best_move=None):
        moves = self.gen_legal_moves()
        if not moves:
            return None
            
        # Put the previous best move first if it exists
        moves = self._order_moves(moves, prev_best_move)
        best_move = moves[0]
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                if time.time() - start_time > time_limit:
                    return None  # Abort
                self.make_move(move, check_legality=False)
                eval_score = self._alphabeta(depth - 1, alpha, beta, False)
                self.undo()
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                # Note: Alpha-beta pruning at the root node is generally less effective because all moves must be evaluated,
                # but it can occasionally cut off if an opponent completely refuted a line previously.
            return best_move, max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                if time.time() - start_time > time_limit:
                    return None  # Abort
                self.make_move(move, check_legality=False)
                eval_score = self._alphabeta(depth - 1, alpha, beta, True)
                self.undo()
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
            return best_move, min_eval

    def _alphabeta(self, depth, alpha, beta, maximizing_player):
        self.nodes_searched += 1
        
        if depth <= 0:
            return self._quiescence_search(alpha, beta, maximizing_player)
            
        moves = self.gen_legal_moves()
        
        if not moves:
            if self.is_in_check(self.side):
                # Subtracting depth allows prioritizing shorter mates
                return -c.MAX_SCORE + len(self.history) if maximizing_player else c.MAX_SCORE - len(self.history)
            return 0  # Stalemate / Draw
            
        moves = self._order_moves(moves)
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                self.make_move(move, check_legality=False)
                eval_score = self._alphabeta(depth - 1, alpha, beta, False)
                self.undo()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                self.make_move(move, check_legality=False)
                eval_score = self._alphabeta(depth - 1, alpha, beta, True)
                self.undo()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def _quiescence_search(self, alpha, beta, maximizing_player):
        """
        Quiescence search to avoid the horizon effect.
        Only evaluates noisy moves (captures/promotions) until a quiet position is reached.
        """
        self.nodes_searched += 1
        
        stand_pat = self.eval(self)
        
        if maximizing_player:
            if stand_pat >= beta:
                return beta
            alpha = max(alpha, stand_pat)
        else:
            if stand_pat <= alpha:
                return alpha
            beta = min(beta, stand_pat)
            
        moves = self.gen_legal_moves()
        # Filter for noisy moves (captures, promotions)
        noisy_moves = [m for m in moves if m.capture or ('promotion' in m.flag)]
        noisy_moves = self._order_moves(noisy_moves)
        
        if maximizing_player:
            for move in noisy_moves:
                self.make_move(move, check_legality=False)
                eval_score = self._quiescence_search(alpha, beta, False)
                self.undo()
                
                if eval_score >= beta:
                    return beta
                alpha = max(alpha, eval_score)
            return alpha
        else:
            for move in noisy_moves:
                self.make_move(move, check_legality=False)
                eval_score = self._quiescence_search(alpha, beta, True)
                self.undo()
                
                if eval_score <= alpha:
                    return alpha
                beta = min(beta, eval_score)
            return beta

    def _order_moves(self, moves, prev_best_move=None):
        """
        Move ordering to prioritize good moves first, vastly improving Alpha-Beta pruning.
        """
        def move_score(move):
            score = 0
            if prev_best_move and move == prev_best_move:
                score += 10000  # Highest priority for previous best move
            
            if move.capture:
                # Basic MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
                # Helps sort good captures (Pawn takes Queen) above bad captures (Queen takes Pawn)
                score += 10 * move.capture.value - move.piece.value
            if 'promotion' in move.flag:
                score += 900  # Highly prioritize promotions
            if 'check' in move.flag:
                score += 50   # Prioritize checks
            return score
            
        return sorted(moves, key=move_score, reverse=True)

    # def think(self, iterations=1000, makemove=False):
    #     best_move = self.think_minimax()
    #     if best_move and makemove:
    #         self.make_move(best_move, check_legality=False)
    #     return best_move