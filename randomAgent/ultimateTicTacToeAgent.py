import sys 
import os
import random
import pandas as pd
from agentTicTacToeLib import *

columns = [
    'BoardTLSquareTL', 'BoardTLSquareTM', 'BoardTLSquareTR', 'BoardTLSquareML', 'BoardTLSquareMM', 'BoardTLSquareMR', 'BoardTLSquareBL', 'BoardTLSquareBM', 'BoardTLSquareBR',
    'BoardTMSquareTL', 'BoardTMSquareTM', 'BoardTMSquareTR', 'BoardTMSquareML', 'BoardTMSquareMM', 'BoardTMSquareMR', 'BoardTMSquareBL', 'BoardTMSquareBM', 'BoardTMSquareBR',
    'BoardTRSquareTL', 'BoardTRSquareTM', 'BoardTRSquareTR', 'BoardTRSquareML', 'BoardTRSquareMM', 'BoardTRSquareMR', 'BoardTRSquareBL', 'BoardTRSquareBM', 'BoardTRSquareBR', # First row of boards

    'BoardMLSquareTL', 'BoardMLSquareTM', 'BoardMLSquareTR', 'BoardMLSquareML', 'BoardMLSquareMM', 'BoardMLSquareMR', 'BoardMLSquareBL', 'BoardMLSquareBM', 'BoardMLSquareBR',
    'BoardMMSquareTL', 'BoardMMSquareTM', 'BoardMMSquareTR', 'BoardMMSquareML', 'BoardMMSquareMM', 'BoardMMSquareMR', 'BoardMMSquareBL', 'BoardMMSquareBM', 'BoardMMSquareBR',
    'BoardMRSquareTL', 'BoardMRSquareTM', 'BoardMRSquareTR', 'BoardMRSquareML', 'BoardMRSquareMM', 'BoardMRSquareMR', 'BoardMRSquareBL', 'BoardMRSquareBM', 'BoardMRSquareBR', # Second row of boards

    'BoardBLSquareTL', 'BoardBLSquareTM', 'BoardBLSquareTR', 'BoardBLSquareML', 'BoardBLSquareMM', 'BoardBLSquareMR', 'BoardBLSquareBL', 'BoardBLSquareBM', 'BoardBLSquareBR',
    'BoardBMSquareTL', 'BoardBMSquareTM', 'BoardBMSquareTR', 'BoardBMSquareML', 'BoardBMSquareMM', 'BoardBMSquareMR', 'BoardBMSquareBL', 'BoardBMSquareBM', 'BoardBMSquareBR',
    'BoardBRSquareTL', 'BoardBRSquareTM', 'BoardBRSquareTR', 'BoardBRSquareML', 'BoardBRSquareMM', 'BoardBRSquareMR', 'BoardBRSquareBL', 'BoardBRSquareBM', 'BoardBRSquareBR', # Third row of boards

    'class'] # Result
dataDFSameFormat = pd.DataFrame(columns=columns.copy())
dataDFThreeClass = pd.DataFrame(columns=columns.copy())

global game

def getRandomMove():
    moveList = [] # will contain ((brow, bcol), row, col)

    if game.nextBoard: # If we are limited to which board we can play on
        for row in range(3):
            for col in range(3):
                if game.boards[game.nextBoard[0]][game.nextBoard[1]].board[row][col] == " ":
                    moveList.append((game.nextBoard, row, col))
    else: # if we can play on any board
        for brow in range(3):
            for bcol in range(3):
                for row in range(3):
                    for col in range(3):
                        if game.boards[brow][bcol].board[row][col] == " ":
                            moveList.append(((brow, bcol), row, col))

    return random.choice(moveList)

def playGame():

    gamedf = pd.DataFrame(columns=columns)
    newRowsSameFormat = [] # used to store class/results as True if X wins and False otherwise
    newRowsThreeClass = [] # used to store class/results as "X", "O", or "D" for draw

    game.reset_game()

    while game.get_real_winner() == " " and not game.is_full():
        move = getRandomMove()
        # print(move)
        game.make_move(move[0], move[1], move[2])

        rowItem = {}

        # Populate the rowItems
        for brow in range(3):
            for bcol in range(3):
                for row in range(3):
                    for col in range(3):

                        # All of this to find the dict index str
                        if brow == 0:
                            indexStr = "BoardT"
                        if brow == 1:
                            indexStr = "BoardM"
                        if brow == 2:
                            indexStr = "BoardB"

                        if bcol == 0:
                            indexStr += "L"
                        if bcol == 1:
                            indexStr += "M"
                        if bcol == 2:
                            indexStr += "R"

                        if row == 0:
                            indexStr += "SquareT"
                        if row == 1:
                            indexStr += "SquareM"
                        if row == 2:
                            indexStr += "SquareB"

                        if col == 0:
                            indexStr += "L"
                        if col == 1:
                            indexStr += "M"
                        if col == 2:
                            indexStr += "R"

                        rowItem[indexStr] = game.boards[brow][bcol].board[row][col].lower() if game.boards[brow][bcol].board[row][col] != " " else "b"

        rowItem["class"] = None

        newRowsSameFormat.append(rowItem.copy()) # Need to replace the "None" for class later
        newRowsThreeClass.append(rowItem.copy()) # Need to replace the "None" for class later

    if game.get_real_winner() != " ":
        result = game.get_real_winner()
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

    game = UltimateTicTacToe() # pass None in for non-gui mode
    
    for i in range(10000):
        print(i)
        newRowsSameFormat, newRowsThreeClass = playGame()
        dataDFSameFormat = pd.concat([dataDFSameFormat, pd.DataFrame(newRowsSameFormat)], ignore_index=True)
        dataDFThreeClass = pd.concat([dataDFThreeClass, pd.DataFrame(newRowsThreeClass)], ignore_index=True)


    dataDFSameFormat.to_csv("ultimateTicTacToeDataDFSameFormat.csv", index=False)
    dataDFThreeClass.to_csv("ultimateTicTacToeDataDFThreeClass.csv", index=False)

