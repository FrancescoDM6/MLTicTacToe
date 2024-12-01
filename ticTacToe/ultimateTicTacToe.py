from ticTacToeLib import *
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tictactoelogger import TicTacToeLogger

if __name__ == "__main__":
    root = tk.Tk()

    model_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "MLTicTacToe", "Models", "ultimate_tictactoe_decision_tree_model.pkl")
    # model_path = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "MLTicTacToe", "Models", "ultimate_tictactoe_random_forest_model.pkl")


    game = UltimateTicTacToe(root, model_path)
    root.mainloop()

