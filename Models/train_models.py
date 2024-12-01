import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import pickle
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tictactoelogger import TicTacToeLogger
from sklearn.model_selection import GridSearchCV



def create_decision_tree_model():
    return DecisionTreeClassifier(
        max_depth=5,          # Increased to learn more complex patterns
        min_samples_split=5,   # Reduced to allow more specific pattern learning
        criterion='entropy',    # Could also try 'gini'
        class_weight='balanced',  # Help with any class imbalance
        random_state=42          # Ensure reproducibility

    )



def create_random_forest_model():
    return RandomForestClassifier(
        n_estimators=1000,     # More trees for better pattern recognition
        max_depth=20,          # Deeper trees for complex patterns
        min_samples_split=5,   # Allow more specific pattern learning
        min_samples_leaf=2,
        criterion='entropy',
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )

# def grid_search_for_model(model_type, X_train, y_train):
#     if model_type == "decision_tree":
#         param_grid = {
#             'max_depth': [5, 6, 7],  # More focused around known good value
#             'min_samples_split': [3, 4, 5],
#             'criterion': ['entropy'],  # Stick with what worked
#             'class_weight': ['balanced']
#         }
#         model = DecisionTreeClassifier(random_state=42)
#     else:  # random_forest
#         param_grid = {
#             'n_estimators': [400, 500, 600],
#             'max_depth': [7, 8, 9],
#             'min_samples_split': [3, 4, 5],
#             'min_samples_leaf': [1, 2],
#             'criterion': ['entropy'],
#             'class_weight': ['balanced']
#         }
#         model = RandomForestClassifier(random_state=42, n_jobs=-1)

#     grid_search = GridSearchCV(
#         estimator=model,
#         param_grid=param_grid,
#         cv=5,  # 5-fold cross-validation
#         scoring='accuracy',
#         n_jobs=-1
#     )

#     grid_search.fit(X_train, y_train)
#     print(f"Best parameters for {model_type}: {grid_search.best_params_}")
#     return grid_search.best_estimator_


def create_enhanced_features(board_state):
    """
    Creates additional features beyond raw board positions
    board_state: numpy array of shape (9,) with 1 (X), -1 (O), 0 (blank)
    """
    features = list(board_state)  # Start with raw positions
    
    # Reshape to 3x3 for easier analysis
    board = board_state.reshape(3, 3)
    
    # Add winning threat features
    for player in [1, -1]:  # X and O
        # Count pieces in each row
        for row in board:
            features.append(sum(1 for x in row if x == player))
        
        # Count pieces in each column
        for col in board.T:
            features.append(sum(1 for x in col if x == player))
        
        # Count pieces in diagonals
        diag = sum(1 for i in range(3) if board[i,i] == player)
        anti_diag = sum(1 for i in range(3) if board[i,2-i] == player)
        features.append(diag)
        features.append(anti_diag)
        
        # Count winning threats
        threats = 0
        # Check rows
        for row in board:
            if sum(row == player) == 2 and sum(row == 0) == 1:
                threats += 1
        # Check columns
        for col in board.T:
            if sum(col == player) == 2 and sum(col == 0) == 1:
                threats += 1
        # Check diagonals
        diag = board.diagonal()
        if sum(diag == player) == 2 and sum(diag == 0) == 1:
            threats += 1
        anti_diag = np.diag(np.fliplr(board))
        if sum(anti_diag == player) == 2 and sum(anti_diag == 0) == 1:
            threats += 1
        features.append(threats)
    
    # Add strategic position features
    features.append(board[1,1])  # Center control
    features.append(board[0,0] + board[0,2] + board[2,0] + board[2,2])  # Corner control
    
    return np.array(features)
    
    # features = list(board_state)  # Start with raw board positions
    # board = board_state.reshape(3, 3)

    # # Winning and blocking opportunities
    # for player in [1, -1]:  # 1 = X, -1 = O
    #     # Count pieces in rows, columns, and diagonals
    #     for row in board:
    #         features.append(sum(1 for cell in row if cell == player))
    #     for col in board.T:
    #         features.append(sum(1 for cell in col if cell == player))
    #     features.append(sum(1 for i in range(3) if board[i, i] == player))  # Main diagonal
    #     features.append(sum(1 for i in range(3) if board[i, 2 - i] == player))  # Anti-diagonal

    #     # Immediate win/block threat detection
    #     threats = 0
    #     for row in board:
    #         if sum(row == player) == 2 and sum(row == 0) == 1:
    #             threats += 1
    #     for col in board.T:
    #         if sum(col == player) == 2 and sum(col == 0) == 1:
    #             threats += 1
    #     diag = board.diagonal()
    #     if sum(diag == player) == 2 and sum(diag == 0) == 1:
    #         threats += 1
    #     anti_diag = np.diag(np.fliplr(board))
    #     if sum(anti_diag == player) == 2 and sum(anti_diag == 0) == 1:
    #         threats += 1
    #     features.append(threats)

    # # Positional strategy
    # features.append(board[1, 1])  # Center control
    # features.append(board[0, 0] + board[0, 2] + board[2, 0] + board[2, 2])  # Corners
    # features.append(board[0, 1] + board[1, 0] + board[1, 2] + board[2, 1])  # Edges

    # return np.array(features)

def prepare_data(game_type="regular"):
    

    if game_type == "regular":
        df = pd.read_csv('tic-tac-toe.csv', skiprows=1, names=[
            'TL', 'TM', 'TR',
            'ML', 'MM', 'MR',
            'BL', 'BM', 'BR',
            'class'
        ])

        # df = pd.read_csv('ticTacToeDataDFSameFormat.csv', skiprows=1, names=[
        #     'TL', 'TM', 'TR',
        #     'ML', 'MM', 'MR',
        #     'BL', 'BM', 'BR',
        #     'class'
        # ])
    else:  # Ultimate Tic Tac Toe
        df = pd.read_csv('tic-tac-toe.csv', skiprows=1, names=[
            'TL', 'TM', 'TR',
            'ML', 'MM', 'MR',
            'BL', 'BM', 'BR',
            'class'
        ])
        
        # Duplicate the data 9 times to represent each small board
        df = pd.concat([df] * 9, ignore_index=True)
        
        # Add a column to identify the small board index
        df['board_index'] = np.repeat(np.arange(9), len(df) // 9)



    duplicates = df.duplicated().sum()
    print(f"\nNumber of duplicate rows: {duplicates}")

    # Convert board states to numerical values
    mapping = {'x': 1, 'o': -1, 'b': 0}
    # raw_board_states = df.iloc[:, :9].replace(mapping).infer_objects(copy=False).values
    
    # Create enhanced features
    # X = np.array([create_enhanced_features(board) for board in raw_board_states])
    # y = (df['class'] == True).astype(int)

    # X = df.iloc[:, :9].replace(mapping).values
    X = df.iloc[:, :-2].replace(mapping).values
    y = (df['class'] == True).astype(int)

    print("\nDataset Information:")
    print(f"Total samples: {len(df)}")
    print("\nFeature matrix shape:", X.shape)
    print("First few rows after processing:")
    print("X:", X[:2])
    print("y:", y[:2])
    
    return X, y

# def prepare_data():
#     # Select the dataset by commenting/uncommenting the desired dataset
#     # Dataset 1: Random Agent Dataset
#     df_random = pd.read_csv('ticTacToeDataDFSameFormat.csv', skiprows=1, names=[
#         'TL', 'TM', 'TR',
#         'ML', 'MM', 'MR',
#         'BL', 'BM', 'BR',
#         'class'
#     ])

#     # Dataset 2: X Win Dataset
#     df_xwin = pd.read_csv('tic-tac-toe.csv', skiprows=1, names=[
#         'TL', 'TM', 'TR',
#         'ML', 'MM', 'MR',
#         'BL', 'BM', 'BR',
#         'class'
#     ])

#     df = pd.concat([df_random, df_xwin]).drop_duplicates()


#     print("\nDataset Information:")
#     print(f"Total samples: {len(df)}")
#     print("\nClass distribution:")
#     print(df['class'].value_counts(normalize=True))

#     # Check for and remove duplicate rows
#     # duplicates = df.duplicated().sum()
#     # print(f"\nNumber of duplicate rows: {duplicates}")
#     # if duplicates > 0:
#     #     df = df.drop_duplicates()
#     #     print(f"Duplicates removed. Total samples after cleaning: {len(df)}")

#     # Map board state values to numerical format
#     mapping = {'x': 1, 'o': -1, 'b': 0}
#     raw_board_states = df.iloc[:, :9].replace(mapping).values

#     # Create enhanced features from raw board states
#     X = np.array([create_enhanced_features(board) for board in raw_board_states])
#     y = (df['class'] == True).astype(int)

#     print("\nFeature matrix shape:", X.shape)
#     print("First few rows after processing:")
#     print("X:", X[:2])
#     print("y:", y[:2])

#     return X, y


def evaluate_model(model, X_train, X_val, y_train, y_val, model_type, logger):
    train_accuracy = model.score(X_train, y_train)
    val_accuracy = model.score(X_val, y_val)
    
    print(f"\nModel Type: {model_type.replace('_', ' ').title()}")
    print(f"Training accuracy: {train_accuracy:.4f}")
    print(f"Validation accuracy: {val_accuracy:.4f}")
    
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print("\nCross-validation scores:", cv_scores)
    print(f"Mean CV score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    y_pred = model.predict(X_val)
    conf_matrix = confusion_matrix(y_val, y_pred)
    print("\nConfusion Matrix:")
    print(conf_matrix)
    
    class_report = classification_report(y_val, y_pred)
    print("\nClassification Report:")
    print(class_report)
    
    # Get feature importances for random forest
    feature_importances = None
    if model_type == "random_forest":
        feature_importance = model.feature_importances_
        print("\nFeature Importances:")
        positions = ['TL', 'TM', 'TR', 'ML', 'MM', 'MR', 'BL', 'BM', 'BR']
        feature_importances = dict(zip(positions, feature_importance))
        for pos, imp in feature_importances.items():
            print(f"Position {pos}: {imp:.4f}")

    # Log results - keep confusion matrix as numpy array
    logger.log_training_results({
        'model_type': model_type,
        'train_accuracy': train_accuracy,
        'val_accuracy': val_accuracy,
        'cv_scores': cv_scores.tolist(),
        'cv_score_mean': cv_scores.mean(),
        'cv_score_std': cv_scores.std(),
        'confusion_matrix': conf_matrix,  # Don't convert to list
        'feature_importances': feature_importances,
        'dataset_size': len(X_train) + len(X_val),
        'train_size': len(X_train),
        'val_size': len(X_val)
    })

def train_model(game_type="regular", model_type="random_forest", logger=None):
    X, y = prepare_data()
    
    if len(X) == 0:
        print("No training data available!")
        return
    
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    if model_type == "decision_tree":
        model = create_decision_tree_model()
        model_filename = 'tictactoe_enhanced_dt_model.pkl'
    else:  # random_forest
        model = create_random_forest_model()
        model_filename = 'tictactoe_enhanced_rf_model.pkl'
    
    model.fit(X_train, y_train)

    # print(f"Performing grid search for {model_type}...")
    # model = grid_search_for_model(model_type, X_train, y_train)

    # model_filename = f'tictactoe_enhanced_{model_type}_model.pkl'

    evaluate_model(model, X_train, X_val, y_train, y_val, model_type, logger)
    
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved as {model_filename}")

if __name__ == "__main__":
    logger = TicTacToeLogger()
    
    print("Training Decision Tree model...")
    train_model("decision_tree", logger)
    
    print("\nTraining Random Forest model...")
    train_model("random_forest", logger)