from ticTacToeLib import *
import os

if __name__ == "__main__":
    root = tk.Tk()

    model_path = os.path.join("Models", "tictactoe_dt_model.pkl")
    game = TicTacToe(root, model_path)


    # game = TicTacToe(root)
    root.mainloop()

