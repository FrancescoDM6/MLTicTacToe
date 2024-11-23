import sys 
import os
import random
import pandas as pd
from agentTicTacToeLib import *

columns = ['TL', 'TM', 'TR', 'ML', 'MM',
           'MR', 'BL', 'BM', 'BR', 'class']
dataDFSameFormat = pd.DataFrame(columns=columns.copy())
dataDFThreeClass = pd.DataFrame(columns=columns.copy())

global game

def getRandomMove():
    moveList = [] # will contain (None, row, col)
    for row in range(3):
        for col in range(3):
            if game.board.board[row][col] == " ":
                moveList.append((None, row, col))

    return random.choice(moveList)

def playGame():

    gamedf = pd.DataFrame(columns=columns)
    newRowsSameFormat = [] # used to store class/results as True if X wins and False otherwise
    newRowsThreeClass = [] # used to store class/results as "X", "O", or "D" for draw

    game.reset_game()

    while game.get_winner() == " " and not game.is_full():
        move = getRandomMove()
        # print(move)
        game.make_move(move[0], move[1], move[2])

        rowItem = {}

        rowItem["TL"] = game.board.board[0][0].lower() if game.board.board[0][0] != " " else "b"
        rowItem["TM"] = game.board.board[0][1].lower() if game.board.board[0][1] != " " else "b"
        rowItem["TR"] = game.board.board[0][2].lower() if game.board.board[0][2] != " " else "b"
        rowItem["ML"] = game.board.board[1][0].lower() if game.board.board[1][0] != " " else "b"
        rowItem["MM"] = game.board.board[1][1].lower() if game.board.board[1][1] != " " else "b"
        rowItem["MR"] = game.board.board[1][2].lower() if game.board.board[1][2] != " " else "b"
        rowItem["BL"] = game.board.board[2][0].lower() if game.board.board[2][0] != " " else "b"
        rowItem["BM"] = game.board.board[2][1].lower() if game.board.board[2][1] != " " else "b"
        rowItem["BR"] = game.board.board[2][2].lower() if game.board.board[2][2] != " " else "b"
        rowItem["class"] = None

        newRowsSameFormat.append(rowItem.copy()) # Need to replace the "None" later
        newRowsThreeClass.append(rowItem.copy()) # Need to replace the "None" later

    if game.get_winner() != " ":
        result = game.get_winner()
    else:
        result = "D"

    for i in range(len(newRowsSameFormat)):
         
        newRowsSameFormat[i]["class"] = "True" if result == "X" else "False"
        newRowsThreeClass[i]["class"] = result

    # print(result)
    # print(newRowsSameFormat)
    # print(newRowsThreeClass)

    return newRowsSameFormat, newRowsThreeClass


if __name__ == "__main__":

    game = TicTacToe() # pass None in for non-gui mode
    
    for i in range(10000):
        print(i)
        newRowsSameFormat, newRowsThreeClass = playGame()
        dataDFSameFormat = pd.concat([dataDFSameFormat, pd.DataFrame(newRowsSameFormat)], ignore_index=True)
        dataDFThreeClass = pd.concat([dataDFThreeClass, pd.DataFrame(newRowsThreeClass)], ignore_index=True)


    dataDFSameFormat.to_csv("ticTacToeDataDFSameFormat.csv", index=False)
    dataDFThreeClass.to_csv("ticTacToeDataDFThreeClass.csv", index=False)

