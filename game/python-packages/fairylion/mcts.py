COLOR_GREEN = "\033[1;32;42m"
COLOR_RESET = "\033[0m"

import time
import math
import random
from copy import deepcopy
import fairylion.CONSTANT as c

# from fairylion.mcts_debug import save_mcts_tree # so while debugging you can enter save_mcts_tree(root)

class MCTSNode:
    count = 0
    def __init__(self, move=None, parent=None, color=None, depth=0):
        self.move = move  # Move that led to this node
        self.parent = parent
        # self.state = state  # Game state at this node
        self.children = []
        self.untried_moves = []
        self.expanded = False
        self.visits = 0
        self.score = None  # Evaluation score for the position
        self.solved = False
        self.quiet = False
        if color is None:
            self.color = move.color if move else 1
        else:
            self.color = color
        self.l_id = len(self.parent.children) if self.parent else 0
        self.id = MCTSNode.count
        self.depth = depth
        MCTSNode.count += 1

    def __repr__(self):
        return f"NODE({self.move}, score={self.score})"
    
    def tree(self):
        label = []
        node = self
        while node.parent:
            label.append(node.id)
            node = node.parent
        return f"{label[::-1]}"
    
    def tried_moves(self):
        """ returns all moves in children with at least 1 visit """
        return [child for child in self.children if child.visits]

    def utc(self):
        if self.move is None:
            return 0

        if self.visits == 0:  # dead code, but kept as safety net
            assert False
            return c.MAX_SCORE

        x = -self.score if self.color else self.score
        score_term = x / 100
        exploration_term = math.sqrt(self.parent.visits) / (1 + self.visits)

        return score_term + exploration_term
    
    def UCT_select_child(self):

        """
        Select a child node using a modified UCT formula that considers position evaluation
        
        The idea is to balance:
        1. Exploration of less-visited nodes
        2. Potential of the position (evaluation score)
        3. Exploitation of promising moves
        """
        best_score = float('-inf')
        best_child = None
        
        for child in self.children:
            uct_score = child.utc()

            if uct_score > best_score:
                best_score = uct_score
                best_child = child
            # elif uct_score == best_score and random.random()<1.0/len(self.children):
            #     best_child = child
                
        return best_child

    def expand_initial(self, state):
        # Generate all legal moves
        moves = list(state.gen_legal_moves())
        
        # Sort moves: checks and high-value captures first
        # This uses a similar logic to your promising_factor
        def move_priority(move):
            score = 0
            if 'check' in move.flag:
                score += 100
            if move.capture:
                # Prioritize capturing high value pieces (e.g., Queen=900)
                score += move.capture.value / 10
            if 'promotion' in move.flag and move.data.get('p') == 'q':
                score += 80
            return score

        # Sort in descending order (highest priority first)
        self.untried_moves = sorted(moves, key=move_priority, reverse=True)
        self.expanded = True
        
        # Update quiet status
        self.quiet = True
        if self.move and 'check' in self.move.flag:
            self.quiet = False
        else:
            for move in self.untried_moves:
                if move.capture or 'check' in move.flag or 'promotion' in move.flag:
                    self.quiet = False
                    break

    def expand_one(self):
        if not self.untried_moves:
            return None
        
        move = self.untried_moves.pop(0)
        child_node = MCTSNode(move=move, parent=self, depth=self.depth+1)
        self.children.append(child_node)
        return child_node

    def update(self, score):
        """Update node statistics using average score (for MCTS)."""
        self.visits += 1

        if self.score is None:
            self.score = score
            if abs(self.score) >= c.MAX_SCORE - 99:
                self.solved = True 
        else:
            # Running average update
            self.score += (score - self.score) / self.visits
            if abs(self.score) >= c.MAX_SCORE - 99:
                self.solved = True
        
        if self.expanded and not self.untried_moves and all(child.solved for child in self.children):
            self.solved = True


class MonteCarloSearchMixin:
    
# Modify MonteCarloSearchMixin to optionally return root node
    def monte_carlo_search(self, iterations=1000, time_limit=None, return_root=False):
        """
        Conduct Monte Carlo Tree Search to find the best move
        
        :param return_root: If True, returns the root node for debugging
        """
        random.seed(0)
        MCTSNode.count = 0
        root = MCTSNode(color=1-self.side)
        root_depth = len(self.history)
        self.positionCount = 0
        
        if time_limit:
            start_time = time.time()
            iterations = 9_999_999
        for _ in range(iterations):
            if root.solved:
                print(f"Solved the whole tree after {_} iterations")
                break
            elif _&256 == 0 and time_limit and time.time() - start_time > time_limit and _ > 0:
                print(f"iterations: {_}, time: {COLOR_GREEN}{time.time()-start_time:.2f}{COLOR_RESET}")
                break
            node = root
            state = self
            
            while len(self.history) > root_depth:
                self.undo()

            # Selection
            while node.expanded and not node.untried_moves and node.children:
                node = node.UCT_select_child()
                state.make_move(node.move)

            if not node.solved:
                # Expansion
                if not node.expanded:
                    node.expand_initial(state)
                
                if node.untried_moves:
                    node = node.expand_one()
                    state.make_move(node.move)

                # Evaluation
                if node.expanded and not node.children and not node.untried_moves: # termination
                    node.solved = True
                    if self.is_in_check(self.side):
                        position_score = c.MAX_SCORE-node.depth if self.side else -c.MAX_SCORE+node.depth
                    else:
                        if self.stalemate_flag == 0:
                            position_score = 0
                        elif self.stalemate_flag == 1:
                            position_score = c.MAX_SCORE
                        elif self.stalemate_flag == -1:
                            position_score = -c.MAX_SCORE
                        elif self.stalemate_flag == 2: #whoever gets stalemated loses
                            position_score = -c.MAX_SCORE * c.INDEX_TO_SIGN[self.side]
                else:
                    position_score = state.eval(state)
                    if abs(position_score) >= c.MAX_SCORE - 99:
                        node.solved = True
            else:
                position_score = node.score

            # if position_score>0:  # uncertainty penalty
            #     position_score -= (len(self.history)-1)*10
            # else:
            #     position_score += (len(self.history)-1)*10

            # Backpropagation
            while node:
                node.update(position_score)
                node = node.parent

        # Select move most visited
        best_child = max(root.children, key=lambda c: (c.visits))
        
        while len(self.history) > root_depth: # reset position
            self.undo()
    
        try:
            print(f"I think the best move is {best_child.move}, score: {int(best_child.score)}")
        except:
            print(f"I think the best move is {best_child.move}, score: ???")

        return root if return_root else best_child.move

    def think(self, iterations=1000, makemove=False, time_limit=None):
        # best_move = self.think_minimax()
        best_move = self.monte_carlo_search(iterations, time_limit)
        if best_move and makemove:
            self.make_move(best_move, check_legality=False)
        return best_move