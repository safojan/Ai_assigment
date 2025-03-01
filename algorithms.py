# algorithms.py - Contains the search algorithms for the word ladder game

from collections import deque
import heapq
import time
from node import Node

def bfs_search(word_tree, start, target):
    """Breadth-First Search algorithm"""
    # Initialize with start node
    queue = deque([Node(start)])
    visited = set([start])
    GameValues = {
        "nodes_explored": 0, 
        "max_queue_size": 1, 
        "costs": {},
        "execution_time": 0
    }
    
    start_time = time.time()
    
    while queue:
        GameValues["max_queue_size"] = max(GameValues["max_queue_size"], len(queue))
        
        current_node = queue.popleft()
        current_word = current_node.word
        GameValues["nodes_explored"] += 1
        
        # If we found the target, return the path
        if current_word == target:
            path = current_node.get_path()
            GameValues["costs"] = {word: {"g": i, "h": "N/A", "f": "N/A"} 
                              for i, word in enumerate(path)}
            GameValues["execution_time"] = time.time() - start_time
            return path, GameValues
        
        # Check all neighbors
        for neighbor in word_tree.get(current_word, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_node = Node(neighbor, current_node, current_node.path_cost + 1)
                queue.append(new_node)
                GameValues["costs"][neighbor] = {"g": new_node.path_cost, "h": "N/A", "f": "N/A"}
    
    GameValues["execution_time"] = time.time() - start_time
    return [], GameValues

def ucs_search(word_tree, start, target):
    """Uniform Cost Search algorithm"""
    start_node = Node(start)
    # Priority queue with (path_cost, id, node) to break ties
    pr_queue = [(start_node.path_cost, id(start_node), start_node)]
    visited = set()
    GameValues = {
        "nodes_explored": 0, 
        "max_queue_size": 1, 
        "costs": {start: {"g": 0, "h": "N/A", "f": 0}},
        "execution_time": 0
    }
    
    start_time = time.time()
    
    while pr_queue:
        GameValues["max_queue_size"] = max(GameValues["max_queue_size"], len(pr_queue))
        
        # Get node with lowest path cost
        _, _, current_node = heapq.heappop(pr_queue)
        current_word = current_node.word
        GameValues["nodes_explored"] += 1
        
        if current_word == target:
            path = current_node.get_path()
            GameValues["execution_time"] = time.time() - start_time
            return path, GameValues
        
        if current_word in visited:
            continue
            
        visited.add(current_word)
        
        # Check all neighbors
        for neighbor in word_tree.get(current_word, []):
            if neighbor not in visited:
                new_cost = current_node.path_cost + 1
                new_node = Node(neighbor, current_node, new_cost)
                GameValues["costs"][neighbor] = {"g": new_cost, "h": "N/A", "f": new_cost}
                heapq.heappush(pr_queue, (new_node.path_cost, id(new_node), new_node))
    
    GameValues["execution_time"] = time.time() - start_time
    return [], GameValues

def gbfs_search(word_tree, start, target):
    """Greedy Best-First Search algorithm"""
    # Calculate initial heuristic
    start_heuristic = calculate_hamming_distance(start, target)
    start_node = Node(start, None, 0, start_heuristic)
    
    # Priority queue with (heuristic_cost, id, node) to break ties
    pr_queue = [(start_node.heuristic_cost, id(start_node), start_node)]
    visited = set()
    GameValues = {
        "nodes_explored": 0, 
        "max_queue_size": 1, 
        "costs": {start: {"g": 0, "h": start_heuristic, "f": start_heuristic}},
        "execution_time": 0
    }
    
    start_time = time.time()
    
    while pr_queue:
        GameValues["max_queue_size"] = max(GameValues["max_queue_size"], len(pr_queue))
        
        # Get node with lowest heuristic cost
        _, _, current_node = heapq.heappop(pr_queue)
        current_word = current_node.word
        GameValues["nodes_explored"] += 1
        
        if current_word == target:
            path = current_node.get_path()
            GameValues["execution_time"] = time.time() - start_time
            return path, GameValues
        
        if current_word in visited:
            continue
            
        visited.add(current_word)
        
        # Check all neighbors
        for neighbor in word_tree.get(current_word, []):
            if neighbor not in visited:
                heuristic = calculate_hamming_distance(neighbor, target)
                new_node = Node(neighbor, current_node, current_node.path_cost + 1, heuristic)
                GameValues["costs"][neighbor] = {"g": new_node.path_cost, "h": heuristic, "f": heuristic}
                heapq.heappush(pr_queue, (new_node.heuristic_cost, id(new_node), new_node))
    
    GameValues["execution_time"] = time.time() - start_time
    return [], GameValues

def a_star_search(word_tree, start, target):
    """A* Search algorithm"""
    # Calculate initial heuristic
    start_heuristic = calculate_hamming_distance(start, target)
    start_node = Node(start, None, 0, start_heuristic)
    
    # Priority queue with (total_cost, id, node) to break ties
    pr_queue = [(start_node.total_cost, id(start_node), start_node)]
    visited = set()
    GameValues = {
        "nodes_explored": 0, 
        "max_queue_size": 1, 
        "costs": {start: {"g": 0, "h": start_heuristic, "f": start_heuristic}},
        "execution_time": 0
    }
    
    start_time = time.time()
    
    while pr_queue:
        GameValues["max_queue_size"] = max(GameValues["max_queue_size"], len(pr_queue))
        
        # Get node with lowest total cost
        _, _, current_node = heapq.heappop(pr_queue)
        current_word = current_node.word
        GameValues["nodes_explored"] += 1
        
        if current_word == target:
            path = current_node.get_path()
            GameValues["execution_time"] = time.time() - start_time
            return path, GameValues
        
        if current_word in visited:
            continue
            
        visited.add(current_word)
        
        # Check all neighbors
        for neighbor in word_tree.get(current_word, []):
            if neighbor not in visited:
                new_path_cost = current_node.path_cost + 1
                heuristic = calculate_hamming_distance(neighbor, target)
                total_cost = new_path_cost + heuristic
                new_node = Node(neighbor, current_node, new_path_cost, heuristic)
                GameValues["costs"][neighbor] = {"g": new_path_cost, "h": heuristic, "f": total_cost}
                heapq.heappush(pr_queue, (total_cost, id(new_node), new_node))
    
    GameValues["execution_time"] = time.time() - start_time
    return [], GameValues

# Helper function for all algorithms
def calculate_hamming_distance(word1, word2):
    """Calculate Hamming distance between two words (number of differing positions)"""
    return sum(1 for a, b in zip(word1, word2) if a != b)