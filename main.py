# main.py - Main program for the Word Ladder Game
import streamlit as st

from word_ladder import WordLadderGame

def main():
    """Main function for the Word Ladder Game"""
    st.set_page_config(page_title="Word Ladder Adventure", layout="wide")
    
    st.title("Word Ladder Game")
    
    # Initialize session state
    if 'game' not in st.session_state:
        st.session_state.game = WordLadderGame()
    if 'current_word' not in st.session_state:
        st.session_state.current_word = ""
    if 'target_word' not in st.session_state:
        st.session_state.target_word = ""
    if 'path' not in st.session_state:
        st.session_state.path = []
    if 'hints_used' not in st.session_state:
        st.session_state.hints_used = 0
    if 'optimal_path' not in st.session_state:
        st.session_state.optimal_path = []
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'last_hint' not in st.session_state:
        st.session_state.last_hint = ""
    if 'search_stats' not in st.session_state:
        st.session_state.search_stats = {}
    if 'move_count' not in st.session_state:
        st.session_state.move_count = 0
    
    # Game settings in sidebar
    st.sidebar.header("Game Settings")
    difficulty = st.sidebar.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
    algorithm = st.sidebar.selectbox("Choose Search Algorithm for Hint", ["A*", "BFS", "UCS", "GBFS"])
    
    # Reset game state
    def reset_game():
        st.session_state.game_over = False
        st.session_state.hints_used = 0
        st.session_state.path = []
        st.session_state.optimal_path = []
        st.session_state.score = 0
        st.session_state.last_hint = ""
        st.session_state.search_stats = {}
        st.session_state.move_count = 0
    
    # New game button
    if st.sidebar.button("New Game"):
        reset_game()
        start, target = st.session_state.game.generate_game_pair(difficulty)
        if start and target:
            st.session_state.current_word = start
            st.session_state.target_word = target
            st.session_state.path = [start]
            
            # Calculate optimal path for scoring
            if algorithm == "BFS":
                st.session_state.optimal_path, _ = bfs_search(
                    st.session_state.game.word_tree, start, target
                )
            elif algorithm == "UCS":
                st.session_state.optimal_path, _ = ucs_search(
                    st.session_state.game.word_tree, start, target
                )
            elif algorithm == "GBFS":
                st.session_state.optimal_path, _ = gbfs_search(
                    st.session_state.game.word_tree, start, target
                )
            else:  # A*
                st.session_state.optimal_path, _ = a_star_search(
                    st.session_state.game.word_tree, start, target
                )
            
    # Display game info
    if st.session_state.current_word:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"### Start Word: {st.session_state.path[0]}")
        with col2:
            st.markdown(f"### Current Word: {st.session_state.current_word}")
        with col3:
            st.markdown(f"### Target Word: {st.session_state.target_word}")
        
        # Display the current path and moves
        st.markdown(f"### Path So Far ({len(st.session_state.path)-1} moves):")
        st.write(" → ".join(st.session_state.path))
        
        # Hint system
        hint_col, metrics_col = st.columns([1, 2])
        with hint_col:
            if st.button("Get Hint") and not st.session_state.game_over:
                hint, stats = st.session_state.game.get_hint(
                    st.session_state.current_word, st.session_state.target_word, algorithm
                )
                st.session_state.last_hint = hint
                st.session_state.search_stats = stats
                st.session_state.hints_used += 1
        
            if st.session_state.last_hint:
                st.info(f"Hint: Move to → **{st.session_state.last_hint}**")
                st.write(f"Hints used: {st.session_state.hints_used}")
        
        with metrics_col:
            if st.session_state.search_stats:
                st.markdown("### Search Algorithm Metrics")
                metrics_container = st.container()
                c1, c2, c3 = metrics_container.columns(3)
                
                c1.metric("Nodes Explored", f"{st.session_state.search_stats.get('nodes_explored', 0)}")
                c2.metric("Max Queue Size", f"{st.session_state.search_stats.get('max_queue_size', 0)}")
                c3.metric("Execution Time", f"{st.session_state.search_stats.get('execution_time', 0):.4f} sec")

        # Display costs for current word options if available
        if (st.session_state.search_stats and 
            'costs' in st.session_state.search_stats and 
            st.session_state.search_stats['costs']):
            
            st.markdown("### Search Costs for Possible Moves")
            
            valid_moves = st.session_state.game.word_tree.get(st.session_state.current_word, [])
            costs_data = []
            
            for word in valid_moves:
                if word in st.session_state.search_stats['costs']:
                    costs = st.session_state.search_stats['costs'][word]
                    costs_data.append({
                        "Word": word,
                        "g(x)": costs['g'],
                        "h(x)": costs['h'] if costs['h'] != "N/A" else "N/A",
                        "f(x)": costs['f'] if costs['f'] != "N/A" else "N/A"
                    })
            
            if costs_data:
                st.table(costs_data)
        
        # Display valid moves as buttons
        st.markdown("### Valid Moves:")
        valid_moves = st.session_state.game.word_tree.get(st.session_state.current_word, [])
        
        # Arrange buttons in columns
        cols = st.columns(min(4, max(1, len(valid_moves))))
        for i, word in enumerate(valid_moves):
            with cols[i % len(cols)]:
                if st.button(word, key=f"word_{i}", disabled=st.session_state.game_over):
                    st.session_state.current_word = word
                    st.session_state.path.append(word)
                    st.session_state.move_count += 1
                    
                    if word == st.session_state.target_word:
                        st.session_state.game_over = True
                        st.session_state.score = st.session_state.game.calculate_player_score(
                            st.session_state.path, 
                            st.session_state.optimal_path, 
                            st.session_state.hints_used
                        )
        
        # Path visualization
        if len(st.session_state.path) > 1:
            st.markdown("### Path Visualization:")
            fig = st.session_state.game.create_visualization(st.session_state.path)
            st.plotly_chart(fig, use_container_width=True)
        
        # Game over display
        if st.session_state.game_over:
            st.balloons()
            st.success(f"🎉 Congratulations! You reached the target word in {len(st.session_state.path)-1} moves!")
            
            optimal_moves = len(st.session_state.optimal_path) - 1 if st.session_state.optimal_path else "unknown"
            st.markdown(f"#### Optimal solution: {optimal_moves} moves")
            st.markdown(f"#### Your score: {st.session_state.score} points")
            
            if st.session_state.optimal_path:
                st.markdown("#### Optimal path:")
                st.write(" → ".join(st.session_state.optimal_path))
                
                # Show optimal path visualization
                st.markdown("#### Optimal Path Visualization:")
                fig = st.session_state.game.create_visualization(st.session_state.optimal_path)
                st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.info("Click 'New Game' to start playing!")
        
    # Instructions in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### How to Play")
    st.sidebar.markdown("""
    1. Click 'New Game' to start
    2. Click valid word buttons to make moves
    3. Use the hint button if you get stuck
    4. Try to reach the target word in as few moves as possible
    """)
    
    st.sidebar.markdown("### Difficulty Levels")
    st.sidebar.markdown("""
    - **Easy**: Shorter words, fewer steps needed
    - **Medium**: Medium length words, moderate path length
    - **Hard**: Longer words, more complex paths
    """)
    
    st.sidebar.markdown("### Search Algorithms")
    st.sidebar.markdown("""
    - **A***: Uses both path cost and heuristic
    - **BFS**: Breadth-First Search, finds shortest path
    - **UCS**: Uniform Cost Search, considers edge costs
    - **GBFS**: Greedy Best-First Search, uses only heuristic
    """)

if __name__ == "__main__":
    from algorithms import bfs_search, ucs_search, gbfs_search, a_star_search
    main()