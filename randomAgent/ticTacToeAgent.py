import sys 
import os
import random
import pandas as pd
from agentTicTacToeLib import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ticTacToe.ticTacToeLib import TicTacToeAI

# from multiprocessing import Pool
import joblib



def get_model_type(model_path):
    model_name = os.path.basename(model_path)
    if 'enhanced' in model_name:
        return 'enhanced_' + ('dt' if 'dt_model' in model_name else 'rf')
    elif 'base' in model_name and ('base_dt' in model_name or 'base_rf' in model_name):
        return 'base_' + ('dt' if 'base_dt' in model_name else 'rf')
    elif 'deep_dt' in model_name:
        return 'deep_dt'
    elif 'gini_dt' in model_name:
        return 'gini_dt'
    elif 'light_rf' in model_name:
        return 'light_rf'
    elif 'heavy_rf' in model_name:
        return 'heavy_rf'
    elif model_name.startswith('tictactoe_'):
        return 'standard_' + ('dt' if 'dt_model' in model_name else 'rf')
    elif 'decision_tree' in model_name:
        return 'regular_dt'
    elif 'random_forest' in model_name:
        return 'regular_rf'
    else:
        return 'unknown_model'

def play_model_vs_random(model_path, num_games=100, model_plays_first=True):
    game = TicTacToe()
    
    # Get full path to model file
    models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Models')
    full_model_path = os.path.join(models_dir, model_path)
    print(f"Loading model from: {full_model_path}")
    
    ai = TicTacToeAI(full_model_path)
    if not ai.model:
        print(f"Failed to load model from {full_model_path}")
        return []
        
    results = []
    
    # Parse model type from filename
    model_type = get_model_type(model_path)
    
    for i in range(num_games):
        if i % 10 == 0:  # Only print every 10 games
            print(f"Completed {i+1}/{num_games} games")
        game.reset_game()
        
        game_data = {
            'model_type': model_type,
            'model_played_first': model_plays_first,
            'moves': [],
            'result': None,
            'num_moves': 0,
            'win_method': None
        }

        while game.get_winner() == " " and not game.is_full():
            # Model's turn
            if (game.current_player == "X") == model_plays_first:
                move = ai.get_move(game.board.board)
                if move:
                    row, col = move
                else:
                    # Fallback to random move if AI fails
                    valid_moves = [(r, c) for r in range(3) for c in range(3) 
                                if game.board.board[r][c] == " "]
                    row, col = random.choice(valid_moves)
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
            game_data['win_method'] = 'none'
        else:
            game_data['result'] = 'win' if (winner == "X") == model_plays_first else 'loss'
            # Determine win method (row, column, diagonal)
            for i in range(3):
                if game.board.board[i][0] == game.board.board[i][1] == game.board.board[i][2] == winner:
                    game_data['win_method'] = 'row'
                    break
                if game.board.board[0][i] == game.board.board[1][i] == game.board.board[2][i] == winner:
                    game_data['win_method'] = 'column'
                    break
            if game_data['win_method'] is None:
                if game.board.board[0][0] == game.board.board[1][1] == game.board.board[2][2] == winner:
                    game_data['win_method'] = 'diagonal'
                elif game.board.board[0][2] == game.board.board[1][1] == game.board.board[2][0] == winner:
                    game_data['win_method'] = 'diagonal'
        
        results.append(game_data)
    
    return results

# def play_model_vs_random(preloaded_model, num_games=100, model_plays_first=True):
#     game = TicTacToe()
#     ai = TicTacToeAI(preloaded_model=preloaded_model)  # Pass the model directly
#     results = []
    
#     for i in range(num_games):
#         if i % 10 == 0:  # Only print every 10 games
#             print(f"Completed {i+1}/{num_games} games")
#         game.reset_game()
        
#         game_data = {
#             'model_type': preloaded_model['model_type'],  # Include type from preloaded model
#             'model_played_first': model_plays_first,
#             'moves': [],
#             'result': None,
#             'num_moves': 0,
#             'win_method': None
#         }

#         while game.get_winner() == " " and not game.is_full():
#             # Model's turn
#             if (game.current_player == "X") == model_plays_first:
#                 move = ai.get_move(game.board.board)
#                 if move:
#                     row, col = move
#                 else:
#                     # Fallback to random move if AI fails
#                     valid_moves = [(r, c) for r in range(3) for c in range(3) 
#                                 if game.board.board[r][c] == " "]
#                     row, col = random.choice(valid_moves)
#                 game_data['moves'].append(('model', (row, col)))
#             # Random's turn
#             else:
#                 valid_moves = [(r, c) for r in range(3) for c in range(3) 
#                              if game.board.board[r][c] == " "]
#                 row, col = random.choice(valid_moves)
#                 game_data['moves'].append(('random', (row, col)))
            
#             game.make_move(None, row, col)
#             game_data['num_moves'] += 1

#         # Record result
#         winner = game.get_winner()
#         if winner == " ":
#             game_data['result'] = 'draw'
#             game_data['win_method'] = 'none'
#         else:
#             game_data['result'] = 'win' if (winner == "X") == model_plays_first else 'loss'
#             # Determine win method (row, column, diagonal)
#             for i in range(3):
#                 if game.board.board[i][0] == game.board.board[i][1] == game.board.board[i][2] == winner:
#                     game_data['win_method'] = 'row'
#                     break
#                 if game.board.board[0][i] == game.board.board[1][i] == game.board.board[2][i] == winner:
#                     game_data['win_method'] = 'column'
#                     break
#             if game_data['win_method'] is None:
#                 if game.board.board[0][0] == game.board.board[1][1] == game.board.board[2][2] == winner:
#                     game_data['win_method'] = 'diagonal'
#                 elif game.board.board[0][2] == game.board.board[1][1] == game.board.board[2][0]:
#                     game_data['win_method'] = 'diagonal'
        
#         results.append(game_data)
    
#     return results




if __name__ == "__main__":
    # import joblib

    # Test all model configurations
    model_paths = [
        'tictactoe_dt_model.pkl',
        'tictactoe_rf_model.pkl',
        'regular_tictactoe_dt_base_dt_model.pkl',
        'regular_tictactoe_rf_base_rf_model.pkl',
        'regular_tictactoe_decision_tree_model.pkl',
        'regular_tictactoe_random_forest_model.pkl',
        'tictactoe_enhanced_dt_model.pkl',
        'tictactoe_enhanced_rf_model.pkl',
        'regular_tictactoe_dt_deep_dt_model.pkl',
        'regular_tictactoe_dt_gini_dt_model.pkl',
        'regular_tictactoe_rf_light_rf_model.pkl',
        'regular_tictactoe_rf_heavy_rf_model.pkl',

    ]

    # models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Models')
    # preloaded_models = {
    #     model_path: joblib.load(os.path.join(models_dir, model_path)) for model_path in model_paths
    # }
    
    num_games = 250  # Set the desired number of games
    # scenarios = [(path, num_games, plays_first) for path in model_paths for plays_first in [True, False]]

    # with Pool(processes=4) as pool:  # Use available CPU cores
    all_results = []

    # for model_path, preloaded_model in preloaded_models.items():
    #     print(f"\nTesting {model_path} as X...")
    #     results_x = play_model_vs_random(preloaded_model, num_games=num_games, model_plays_first=True)

    #     print(f"\nTesting {model_path} as O...")
    #     results_o = play_model_vs_random(preloaded_model, num_games=num_games, model_plays_first=False)

    #     all_results.extend(results_x + results_o)

    
    for model_path in model_paths:
        print(f"\nTesting {model_path}")
        # Test as X
        results_x = play_model_vs_random(model_path, num_games=num_games, model_plays_first=True)
        # Test as O
        results_o = play_model_vs_random(model_path, num_games=num_games, model_plays_first=False)
        all_results.extend(results_x + results_o)
    
    # Save results to CSV for analysis
    analysis_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Models', 'analysis')

    # results_df = pd.DataFrame(all_results)
    # results_path = os.path.join(analysis_dir, 'model_vs_random_results.csv')
    # results_df.to_csv(results_path, index=False)

    # results = [result for sublist in all_results for result in sublist]
    results_df = pd.DataFrame(all_results)
    results_path = os.path.join(analysis_dir, 'final_model_vs_random_results.csv')
    results_df.to_csv(results_path, index=False)