import tkinter as tk
from tkinter import messagebox
import numpy as np


# Class just for the TicTacToe board (doesn't have playing functions and is just used for the callback)
class TicTacToeBoard:

    # Creates and displays a TicTacToe board on the master tk object
    # master: the parent tk object for display
    # boardNum: a number representing what board this represents (used for UltimateTicTacToe)
    # callbackFunc: a function that can be called in the form callbackFunc(boardNum, row, col) where row and col are 0-2 inclusive
    def __init__(self, master, boardNum, callbackFunc):
        self.mater = master
        self.boardNum = boardNum
        self.callbackFunc = callbackFunc
        self.board = [[" " for _ in range(3)] for _ in range(3)] # board consists of 3x3 nested list

        # Set up a frame to hold our buttons
        # self.frame = tk.Frame(master)
        # self.frame.grid(padx=10, pady=10)  # Adds some padding around the frame
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                button = tk.Button(master, text=" ", font=("Arial", 24), width=5, height=2,
                                   command=lambda b=boardNum, r=row, c=col: self.callbackFunc(b, r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

# Basic TicTacToe object
class TicTacToe:
    # master is the tk display object containing this game view
    def __init__(self, master, ai_model_path=None):
        self.master = master
        master.title("Tic Tac Toe")        

        self.frame = tk.Frame(master)
        self.frame.grid(padx=10, pady=10)  # Adds some padding around the frame

        self.board = TicTacToeBoard(self.frame, 0, self.make_move)
        self.current_player = "X" # current player stores the player whos turn it is (changed in make_move)

        self.ai = TicTacToeAI(ai_model_path) if ai_model_path else None


    # boardNum ignored since we only have one board
    def make_move(self, boardNum, row, col):
        if self.board.board[row][col] == " ":
            self.board.board[row][col] = self.current_player
            self.board.buttons[row][col].config(text=self.current_player)

            winner = self.get_winner()
            if winner != " ":
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
                self.reset_game()
            elif self.is_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

                if self.current_player == "O" and self.ai:
                    self.make_ai_move()

    # Returns the winner's char if there is one and a space otherwise
    def get_winner(self):
        for i in range(3):
            if self.board.board[i][0] == self.board.board[i][1] == self.board.board[i][2] != " ": # check rows
                return self.board.board[i][0]
            if self.board.board[0][i] == self.board.board[1][i] == self.board.board[2][i] != " ": # check columns
                return self.board.board[0][i]
        if self.board.board[0][0] == self.board.board[1][1] == self.board.board[2][2] != " ": # top left -> bottom right diagonal
            return self.board.board[1][1]
        if self.board.board[0][2] == self.board.board[1][1] == self.board.board[2][0] != " ": # top right -> bottom left diagonal
            return self.board.board[1][1]
        return " "

    def is_full(self):
        return all(cell != " " for row in self.board.board for cell in row)

    def reset_game(self):
        self.board.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for row in range(3):
            for col in range(3):
                self.board.buttons[row][col].config(text=" ")

    def make_ai_move(self):
        move = self.ai.get_move(self.board.board)
        if move:
            row, col = move
            self.make_move(0, row, col)  # boardNum is always 0 for regular TicTacToe


# Ultimate TicTacToe object
class UltimateTicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Ultimate Tic Tac Toe")

        self.frames = [[tk.Frame(master) for _ in range(3)] for _ in range(3)] # create frames to be the master object of the mini-boards
        self.boards = [[TicTacToeBoard(self.frames[row][col], (row, col), self.make_move) for col in range(3)] for row in range(3)] # Create our board of smaller boards
        self.boardWinners = [[" " for _ in range(3)] for _ in range(3)] # none of the sub-boards have winners yet
        self.current_player = "X"
        self.nextBoard = None

        for brow in range(3):
            for bcol in range(3):
                self.frames[brow][bcol].grid(row=brow, column=bcol, padx=10, pady=10)

    # bcoord is (brow, bcol) in the 3x3 board matrix
    def make_move(self, bcoord, row, col):

        # print(bcoord, row, col, self.nextBoard)

        # Do nothing if that board has already been won
        if self.boardWinners[bcoord[0]][bcoord[1]] != " ":
            return

        # Do nothing if the spot has already been taken
        if self.boards[bcoord[0]][bcoord[1]].board[row][col] != " ":
            return

        # Verify that the player is in their intended board if there is a restriction
        if self.nextBoard != None and self.nextBoard != bcoord:
            return # failed to match the restriction

        # Set the square
        self.boards[bcoord[0]][bcoord[1]].board[row][col] = self.current_player # update square
        self.boards[bcoord[0]][bcoord[1]].buttons[row][col].config(text=self.current_player) # update the button text

        self.boardWinners[bcoord[0]][bcoord[1]] = self.get_3x3_winner(self.boards[bcoord[0]][bcoord[1]]) # update if this board was won
        winner = self.get_real_winner()
        if winner != " ":
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            self.reset_game()
        elif self.is_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_game()
        else:
            self.current_player = "O" if self.current_player == "X" else "X" # update current player

            # If the board indicated by this move isn't won or full then we allow the next player to play whereever they'd like
            if (self.boardWinners[row][col] == " ") and (not self.is_3x3_full(self.boards[row][col])):
                self.nextBoard = (row, col)
            else:
                self.nextBoard = None # if the board isn't available for a move then we allow the next player to make a move whereever is valid

    # Determines if there has been a winner for a 3x3 board (board is of type class TicTacToeBoard)
    def get_3x3_winner(self, board):
        
        for i in range(3):
            if board.board[i][0] == board.board[i][1] == board.board[i][2] != " ":
                return board.board[i][0]
            if board.board[0][i] == board.board[1][i] == board.board[2][i] != " ":
                return board.board[0][i]
        if board.board[0][0] == board.board[1][1] == board.board[2][2] != " ":
            return board.board[1][1]
        if board.board[0][2] == board.board[1][1] == board.board[2][0] != " ":
            return board.board[1][1]
        return " "

    # Determines if the board is full for a 3x3 board (board is of type class TicTacToeBoard)
    def is_3x3_full(self, board):
        
        for r in range(3):
            for c in range(3):
                if board.board[r][c] == " ":
                    return False
        return True

    # requires an up to date self.boardWinners list
    def get_real_winner(self):
        for i in range(3):
            if self.boardWinners[i][0] == self.boardWinners[i][1] == self.boardWinners[i][2] != " ":
                return self.boardWinners[i][0]
            if self.boardWinners[0][i] == self.boardWinners[1][i] == self.boardWinners[2][i] != " ":
                return self.boardWinners[0][i]
        if self.boardWinners[0][0] == self.boardWinners[1][1] == self.boardWinners[2][2] != " ":
            return self.boardWinners[1][1]
        if self.boardWinners[0][2] == self.boardWinners[1][1] == self.boardWinners[2][0] != " ":
            return self.boardWinners[1][1]
        return " "


    def is_full(self):
        return all(cell != " " for row in self.boardWinners for cell in row)

    def reset_game(self) :
        for row in range(3):
            for col in range(3):
                self.boards[row][col].board = [[" " for _ in range(3)] for _ in range(3)] # resets the board
        self.boardWinners = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

        for brow in range(3):
            for bcol in range(3):
                for row in range(3):
                    for col in range(3):
                        self.boards[brow][bcol].buttons[row][col].config(text=" ")


class TicTacToeAI:
    def __init__(self, model_path=None):
        self.model = None
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, path):
        try:
            import pickle
            with open(path, 'rb') as f:
                self.model = pickle.load(f)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model = None
    
    def get_move(self, board):
        if not self.model:
            return None
            
        print("\nCurrent board state:")
        for row in board:
            print(row)
        
        valid_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
        if not valid_moves:
            return None

        print("Valid moves:", valid_moves)

        best_move = None
        best_score = float('-inf')
        
        for move in valid_moves:
            row, col = move
            test_board = [row[:] for row in board]
            test_board[row][col] = "O"
            
            features = []
            for r in test_board:
                for c in r:
                    if c == "X": features.append(1)
                    elif c == "O": features.append(-1)
                    else: features.append(0)
            
            score = 1 - self.model.predict_proba(np.array(features).reshape(1, -1))[0][1]
            print(f"Move {move}: score = {score:.4f}")
            
            if score > best_score:
                best_score = score
                best_move = move
        
        print(f"Choosing move: {best_move}")
        return best_move

