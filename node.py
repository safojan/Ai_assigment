# node.py - Contains the Node class for search algorithms

class Node:
    """Node class for search algorithms"""
    def __init__(self, word, parent=None, path_cost=0, heuristic_cost=0):
        self.word = word
        self.parent = parent
        self.path_cost = path_cost  # Cost from start to current node
        self.heuristic_cost = heuristic_cost  # Estimated cost to goal
        self.total_cost = path_cost + heuristic_cost  # Total cost
    
    def __lt__(self, other):
        # For priority queue comparison
        return self.total_cost < other.total_cost
    
    def get_path(self):
        """Reconstruct path from this node to the start node"""
        path = []
        current = self
        while current:
            path.append(current.word)
            current = current.parent
        return path[::-1]  # Reverse to get start-to-goal path