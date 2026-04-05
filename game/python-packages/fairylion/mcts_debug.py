# usage
# save_mcts_tree_json(engine, 3000)

import json
import time

def export_mcts_tree_to_json(chess, root_node, min_visits=0, max_depth=50):
    """
    Export the Monte Carlo Tree Search node structure to JSON format
    
    :param root_node: The root MCTSNode to export
    :param min_visits: Minimum number of visits for a node to be included
    :param max_depth: Maximum depth of the tree to export
    :return: Dictionary representing the tree structure
    """
    
    def node_to_dict(node, depth=0):
        if depth > max_depth or node.visits < min_visits:
            return None
        
        # Extract move information
        move_info = None
        if node.move:
            move_info = {
                'move_str': node.move.PGN(simplified=True),
                'flag': list(node.move.flag) if hasattr(node.move, 'flag') and node.move.flag else [],
                'capture': str(node.move.capture) if hasattr(node.move, 'capture') else False
            }
        
        # Create node dictionary
        node_dict = {
            'id': node.id,
            'local_id': node.l_id,
            'depth': node.depth,
            'move': move_info,
            'color': node.color,
            'visits': node.visits,
            'score': node.score,
            'solved': node.solved,
            'quiet': node.quiet,
            'utc': round(node.utc(), 2) if hasattr(node, 'utc') and callable(node.utc) else None,
            'parent_id': node.parent.id if node.parent else None,
            'children': [],
            'position': str(chess).replace(' ','')
        }
        
        # Recursively add children
        for child in node.children:
            chess.make_move(child.move)
            child_dict = node_to_dict(child, depth + 1)
            chess.undo()
            if child_dict is not None:  # Only add if child meets criteria
                node_dict['children'].append(child_dict)
        
        return node_dict
    
    # Convert tree to dictionary
    tree_dict = node_to_dict(root_node)
    
    return tree_dict

def save_mcts_tree_json(chess, iterations=3000, root_node=None, time_limit=None, min_visits=1, max_depth=50, indent=2, filename="mcts_tree"):
    """
    Save MCTS tree to a JSON file
    
    :param root_node: The root MCTSNode to export
    :param filename: Output filename (should end with .json)
    :param min_visits: Minimum number of visits for a node to be included
    :param max_depth: Maximum depth of the tree to export
    :param indent: JSON formatting indent level
    """
    total_t0 = time.perf_counter()

    search_time = 0.0
    if root_node is None:
        search_t0 = time.perf_counter()
        root_node = chess.monte_carlo_search(iterations, time_limit, return_root=True)
        search_time = time.perf_counter() - search_t0

    export_t0 = time.perf_counter()
    tree_dict = export_mcts_tree_to_json(chess, root_node, min_visits, max_depth)
    export_time = time.perf_counter() - export_t0

    filename='/Users/omshinwa/Documents/GAMEDEV/Fairylion_MCTS visualizer/game/'+filename+'.json'
    dump_t0 = time.perf_counter()
    with open(filename, 'w') as f:
        json.dump(tree_dict, f, indent=indent)
    dump_time = time.perf_counter() - dump_t0

    total_time = time.perf_counter() - total_t0
    print(
        "timings -> "
        f"search: {search_time:.4f}s | "
        f"export: {export_time:.4f}s | "
        f"dump: {dump_time:.4f}s | "
        f"total: {total_time:.4f}s"
    )
    
    print(f"MCTS tree exported to {filename}")

