# difference:
# this mcts does lazy expansion

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
        # if self.solved:
        #     return float('-inf')

        def promising_factor(move):
            """
            return a positive number for move that could be interesting
            negative for moves that seemingly doesnt do anything
            """
            factor = 1
            if 'check' in move.flag:
                factor *= 1.2
            if 'promotion' in move.flag and move.data['p'] == 'q':
                factor *= 1.1
            if move.capture:
                factor *= 1 + move.capture.value/10000 # queen is 1.09
            # if move.piece.fen == 'g':
            #     return 0.5
            return factor
        
        if self.visits == 0: # Baseline: avoid division by zero
            return c.MAX_SCORE * promising_factor(self.move)

        visits_term = math.sqrt(self.parent.visits) / (1 + self.visits)
        if self.score is not None:
            # raw_score = -self.score if self.color else self.score
            # # Scale raw_score so the curve feels right (400 is standard chess scaling)
            # raw_score /= 400.0
            # # FAST SIGMOID: maps x to range (-1, 1), then shifted to (0, 1)
            # raw_score = 0.5 * (1.0 + (raw_score / (1.0 + abs(raw_score))))

            # # Add the tiny linear term so massive scores still differentiate
            # linear_term = raw_score / (c.MAX_SCORE)
            
            # score_term = raw_score + linear_term

            x = -self.score if self.color else self.score
            score_term = x / 100
        else:
            score_term = 0
        
        exploration_term = promising_factor(self.move) * visits_term
        # if self.quiet:
        #     exploration_term *= 0.5
        
        # Combined UCT-like score that considers evaluation
        uct_score = score_term + exploration_term #* promising_factor(self.move)
        return uct_score
    
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

    def expand(self, state):
        quiet_position = True
        if self.move and 'check' in self.move.flag:
            quiet_position = False
        for i, move in enumerate(state.gen_legal_moves()):
            if quiet_position:
                if move.capture or 'check' in move.flag or 'promotion' in move.flag:
                    quiet_position = False
            child_node = MCTSNode(move=move, parent=self, depth=self.depth+1)
            self.children.append(child_node)
        self.quiet = quiet_position

    # def update(self, score):
    #     """
    #     Update node statistics
    #     Instead of tracking wins, we now track evaluation scores
    #     """
    #     self.visits += 1
        
    #     # If this is the first evaluation or introduces a better score
    #     if self.score is None:
    #         self.score = score
    #     else:    
    #         if self.color: # black
    #             if len(self.children): # possible for the IF to be false if we're revisiting a Solved node
    #                 self.score = max(child.score for child in self.children if not child.score is None)
    #             if self.score <= -c.MAX_SCORE + 99:
    #                 self.solved = True 
    #         else: # white
    #             if len(self.children):
    #                 self.score = min(child.score for child in self.children if not child.score is None)
    #             if self.score >= c.MAX_SCORE - 99:
    #                 self.solved = True 

    #         if all(child.solved for child in self.children):
    #             self.solved = True

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
        
        if all(child.solved for child in self.children):
            self.solved = True


class MonteCarloSearchMixin:
    
# Modify MonteCarloSearchMixin to optionally return root node
    def monte_carlo_search(self, iterations=1000, return_root=False):
        """
        Conduct Monte Carlo Tree Search to find the best move
        
        :param return_root: If True, returns the root node for debugging
        """
        random.seed(0)
        MCTSNode.count = 0
        root = MCTSNode(color=1-self.side)
        root_depth = len(self.history)
        self.positionCount = 0
        
        for _ in range(iterations):
            if root.solved:
                print(f"Solved the whole tree after {_} iterations")
                break
            node = root
            state = self
            
            while len(self.history) > root_depth: # state = deepcopy(self) 
                self.undo()

            # Selection
            while node.children:
                node = node.UCT_select_child()
                state.make_move(node.move)

            if not node.solved:
                # Expansion
                node.expand(state)

                # Evaluation
                if not node.children: # termination
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
                            position_score = -c.MAX_SCORE * c.COLOR_TO_SIGN[self.side]
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

        # Return either the best move or the root node for debugging
        return root if return_root else best_child.move

    def think(self, iterations=1000, makemove=False):
        # best_move = self.think_minimax()
        best_move = self.monte_carlo_search(iterations)
        if best_move and makemove:
            self.make_move(best_move, check_legality=False)
        return best_move