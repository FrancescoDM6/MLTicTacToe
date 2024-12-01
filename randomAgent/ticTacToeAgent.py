import sys 
import os
import random
import pandas as pd
from agentTicTacToeLib import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ticTacToe.ticTacToeLib import TicTacToeAI


def play_model_vs_random(model_path, num_games=100, model_plays_first=True):
    game = TicTacToe()
    models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Models')
    full_model_path = os.path.join(models_dir, model_path)

    ai = TicTacToeAI(full_model_path)
    if not ai.model:
        print(f"Failed to load model from {full_model_path}")
        return []
        
    results = []
    
    for i in range(num_games):
        print(f"Game {i+1}")
        game.reset_game()
        
        # Record game data
        game_data = {
            'model_type': 'decision_tree' if 'dt_model' in model_path else 'random_forest',
            'model_played_first': model_plays_first,
            'moves': [],
            'result': None,
            'num_moves': 0
        }

        while game.get_winner() == " " and not game.is_full():
            # Model's turn
            if (game.current_player == "X") == model_plays_first:
                move = ai.get_move(game.board.board)
                if move:
                    row, col = move
                    game_data['moves'].append(('model', (row, col)))
            # Random's turn
            else:
                valid_moves = [(r, c) for r in range(3) for c in range(3) 
                             if game.board.board[r][c] == " "]
                row, col = random.choice(valid_moves)
                game_data['moves'].append(('random', (row, col)))
            
            game.make_move(None, row, col)
            game_data['num_moves'] += 1

        # Record result
        winner = game.get_winner()
        if winner == " ":
            game_data['result'] = 'draw'
        else:
            game_data['result'] = 'win' if (winner == "X") == model_plays_first else 'loss'
        
        results.append(game_data)
    
    return results

if __name__ == "__main__":
    # Test all model configurations
    model_paths = [
        'regular_tictactoe_dt_base_dt_model.pkl',
        'regular_tictactoe_rf_base_rf_model.pkl',
        # Add other model configurations
    ]
    
    all_results = []
    
    for model_path in model_paths:
        print(f"\nTesting {model_path}")
        # Test as X
        results_x = play_model_vs_random(model_path, num_games=100, model_plays_first=True)
        # Test as O
        results_o = play_model_vs_random(model_path, num_games=100, model_plays_first=False)
        all_results.extend(results_x + results_o)
    
    # Save results to CSV for analysis
    analysis_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Models', 'analysis')

    results_df = pd.DataFrame(all_results)
    results_path = os.path.join(analysis_dir, 'model_vs_random_results.csv')
    results_df.to_csv(results_path, index=False)