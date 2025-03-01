import plotly.graph_objects as go
import networkx as nx
import random

def load_words(filename):
    """Load words from a file into a set"""
    try:
        with open(filename, 'r') as file:
            # Keep words that are 3-6 letters long and only contain letters
            return {word.strip().lower() for word in file 
                   if 3 <= len(word.strip()) <= 6 and word.strip().isalpha()}
    except FileNotFoundError:
        print(f"Could not find {filename}. Using a small test set of words.")
        # Fallback to a small set of words for testing
        return {"cat", "bat", "hat", "rat", "mat", "sat", "pat", "eat", "fat", "fit", "hit", "kit", "lit", "pit"}

def calculate_hamming_distance(word1, word2):
    """Calculate the Hamming distance between two words"""
    return sum(1 for a, b in zip(word1, word2) if a != b)

def create_graph_visualization(path):
    """Create a visualization of the word ladder path"""
    # Create a directed graph
    graph = nx.DiGraph()
    
    # Add nodes and edges
    for i in range(len(path) - 1):
        graph.add_edge(path[i], path[i+1])
        
    # Calculate positions
    positions = {node: (i, 0) for i, node in enumerate(path)}
    
    # Create edges trace
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    # Create nodes trace
    node_x = [positions[node][0] for node in graph.nodes()]
    node_y = [positions[node][1] for node in graph.nodes()]
    
    # Choose colors: start=orange, end=blue, middle=green
    node_colors = ['#FF9500' if i == 0 else '#00BFFF' if i == len(path)-1 else '#1FCC92' 
                  for i in range(len(path))]
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=list(graph.nodes()),
        textposition="top center",
        marker=dict(
            showscale=False,
            color=node_colors,
            size=20,
            line=dict(width=2, color='white')
        )
    )
    
    # Create figure
    figure = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=200,
            plot_bgcolor='rgba(0,0,0,0)'
        )
    )
                  
    return figure

def calculate_score(player_path, optimal_path, hints_used):
    """Calculate player's score based on path efficiency and hints used"""
    if not player_path or not optimal_path:
        return 0
        
    optimal_moves = len(optimal_path) - 1  # Number of moves in optimal path
    player_moves = len(player_path) - 1  # Number of moves in player's path
    
    base_score = 100
    efficiency_factor = optimal_moves / max(player_moves, 1)
    hint_penalty = hints_used * 10
    
    score = int(base_score * efficiency_factor - hint_penalty)
    return max(score, 0)  # Ensure score is not negative

def generate_word_pair(word_tree, difficulty):
    """Generate start and target words based on difficulty"""
    word_list = list(word_tree.keys())
    if not word_list:
        print("No words available. Please check your word list file.")
        return "", ""
        
    # Filter words by length based on difficulty
    if difficulty == "Easy":
        word_length = 3
    elif difficulty == "Medium":
        word_length = 4
    else:  # Hard
        word_length = [5, 6]  # Use longer words for hard difficulty
        
    if isinstance(word_length, list):
        filtered_words = [w for w in word_list if len(w) in word_length]
    else:
        filtered_words = [w for w in word_list if len(w) == word_length]
        
    if len(filtered_words) < 2:
        print(f"Not enough words for {difficulty} difficulty. Using all available words.")
        filtered_words = word_list
    
    # Just return a random pair for simplicity
    start = random.choice(filtered_words)
    target = random.choice([w for w in filtered_words if w != start])
    return start, target