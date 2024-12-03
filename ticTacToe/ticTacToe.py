from ticTacToeLib import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tictactoelogger import TicTacToeLogger

if __name__ == "__main__":
    root = tk.Tk()
    
    # Get model path
    # model_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "MLTicTacToe", "Models", "tictactoe_enhanced_dt_model.pkl")
    # model_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "MLTicTacToe", "Models", "tictactoe_dt_model.pkl")
    # model_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "MLTicTacToe", "Models", "regular_tictactoe_decision_tree_model.pkl")
    # model_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "MLTicTacToe", "Models", "regular_tictactoe_random_forest_model.pkl")
    model_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "MLTicTacToe", "Models", "regular_tictactoe_rf_base_rf_model.pkl")


    # model_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "MLTicTacToe", "Models", "tictactoe_enhanced_decision_tree_model.pkl")

    # Create game instance
    game = TicTacToe(root, model_path, enable_logging=True)
    
    root.mainloop()