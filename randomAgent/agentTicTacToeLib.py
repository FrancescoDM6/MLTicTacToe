import tkinter as tk
from tkinter import messagebox
import numpy as np


# Class just for the TicTacToe board (doesn't have playing functions and is just used for the callback)
class TicTacToeBoard:

    # Creates and displays a TicTacToe board on the master tk object
    # master: the parent tk object for display
    # boardNum: a number representing what board this represents (used for UltimateTicTacToe)
    # callbackFunc: a function that can be called in the form callbackFunc(boardNum, row, col) where row and col are 0-2 inclusive
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)] # board consists of 3x3 nested list


# Basic TicTacToe object
class TicTacToe:
    # master is the tk display object containing this game view
    def __init__(self):
        self.current_player = "X" # current player stores the player whos turn it is (changed in make_move)
        self.frame = None
        self.board = TicTacToeBoard()

    # boardNum ignored since we only have one board
    def make_move(self, boardNum, row, col):
        if self.board.board[row][col] == " ":
            self.board.board[row][col] = self.current_player

            winner = self.get_winner()
            if winner != " ": # allow external reset
                pass
                # self.reset_game()
            elif self.is_full(): # allow external reset
                pass
                # self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

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


# Ultimate TicTacToe object
class UltimateTicTacToe:
    def __init__(self):

        self.boards = [[TicTacToeBoard() for col in range(3)] for row in range(3)] # Create our board of smaller boards
        self.boardWinners = [[" " for _ in range(3)] for _ in range(3)] # none of the sub-boards have winners yet. This is set to " " for ongoing or drawn (use is_3x3_full to find out if drawn), "X" or "O" for a win
        self.current_player = "X"
        self.nextBoard = None

    # bcoord is (brow, bcol) in the 3x3 board matrix
    def make_move(self, bcoord, row, col):

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

        self.boardWinners[bcoord[0]][bcoord[1]] = self.get_3x3_winner(self.boards[bcoord[0]][bcoord[1]]) # update if this board was won
        winner = self.get_real_winner()

        if winner != " ": # allow external reset
            pass
            # self.reset_game()
        elif self.is_full(): # allow external reset
            pass
            # self.reset_game()
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

        return " " # show board still in progress

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

        for brow in range(3):
            for bcol in range(3):
                if not self.is_3x3_full(self.boards[brow][bcol]) and self.boardWinners[brow][bcol] == " ": # we aren't full if any sub-board can still have moves played
                    return False
        return True
        # return all(cell != " " for row in self.boardWinners for cell in row)

    def reset_game(self) :
        for row in range(3):
            for col in range(3):
                self.boards[row][col].board = [[" " for _ in range(3)] for _ in range(3)] # resets the board
        self.boardWinners = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
