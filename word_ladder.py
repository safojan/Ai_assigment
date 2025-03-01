# word_ladder.py - Contains the WordLadderGame class

from collections import defaultdict
import string
import time
from utils import load_words, calculate_hamming_distance, create_graph_visualization, calculate_score, generate_word_pair
from algorithms import bfs_search, ucs_search, gbfs_search, a_star_search

class WordLadderGame:
    def __init__(self, word_file='wordslist.txt'):
        """Initialize the word ladder game"""
        self.words = load_words(word_file)
        self.word_tree = {}  # Initialize as empty
        if self.words:
            self.word_tree = self.build_word_tree()
            
    def build_word_tree(self):
        """Build a tree of words that differ by one letter"""
        tree = defaultdict(list)
        words_by_length = defaultdict(list)
        
        # Group words by length
        for word in self.words:
            words_by_length[len(word)].append(word)
        
        # For each group of same-length words
        for length, words_list in words_by_length.items():
            for word in words_list:
                # Try changing each position to each letter
                for i in range(length):
                    for letter in string.ascii_lowercase:
                        new_word = word[:i] + letter + word[i+1:]
                        # Add to tree if it's a valid word and not the same word
                        if new_word in self.words and new_word != word:
                            tree[word].append(new_word)
        return tree

    def get_hint(self, start_word, target_word, algorithm):
        """Get a hint for the next move using the selected algorithm"""
        # Reset statistics
        stats = {
            "nodes_explored": 0,
            "max_queue_size": 0,
            "execution_time": 0,
            "costs": {}
        }
        
        # Make sure words are in our tree
        if start_word not in self.word_tree or target_word not in self.word_tree:
            return "Hint not available", stats
        
        # Run the selected algorithm
        if algorithm == "BFS":
            path, stats = bfs_search(self.word_tree, start_word, target_word)
        elif algorithm == "UCS":
            path, stats = ucs_search(self.word_tree, start_word, target_word)
        elif algorithm == "GBFS":
            path, stats = gbfs_search(self.word_tree, start_word, target_word)
        else:  # A*
            path, stats = a_star_search(self.word_tree, start_word, target_word)
        
        # Return the next word in the path as a hint
        return path[1] if len(path) > 1 else "No hint available", stats

    def generate_game_pair(self, difficulty):
        """Generate a pair of words for a new game based on difficulty"""
        return generate_word_pair(self.word_tree, difficulty)

    def create_visualization(self, path):
        """Create a visualization of the path"""
        return create_graph_visualization(path)
        
    def calculate_player_score(self, player_path, optimal_path, hints_used):
        """Calculate player's score"""
        return calculate_score(player_path, optimal_path, hints_used)