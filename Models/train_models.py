import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
# from ticTacToe.ticTacToeLib import GameDatabase
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

def create_decision_tree_model():
    return DecisionTreeClassifier(
        max_depth=5,
        min_samples_split=5,
        criterion='entropy'
    )

def create_random_forest_model():
    return RandomForestClassifier(
        n_estimators=1000,
        max_depth=20,
        min_samples_split=5,
        criterion='entropy',
        random_state=42,
        n_jobs=-1
    )

def prepare_data():
    import pandas as pd
    
    # Load the dataset - skip the first row which contains headers
    df = pd.read_csv('tic-tac-toe.csv', skiprows=1, names=[
        'TL', 'TM', 'TR',
        'ML', 'MM', 'MR',
        'BL', 'BM', 'BR',
        'class'
    ])
    
    # Convert board states to numerical values
    mapping = {'x': 1, 'o': -1, 'b': 0}
    X = df.iloc[:, :9].replace(mapping).values
    y = (df['class'] == True).astype(int)  
    
    print("First few rows after processing:")
    print("X:", X[:5])
    print("y:", y[:5])
    
    return X, y

def train_model(model_type="random_forest"):
    X, y = prepare_data()
    
    if len(X) == 0:
        print("No training data available!")
        return
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create and train model
    if model_type == "decision_tree":
        model = create_decision_tree_model()
        model_filename = 'tictactoe_dt_model.pkl'
    else:  # random_forest
        model = create_random_forest_model()
        model_filename = 'tictactoe_rf_model.pkl'
    
    # Train
    model.fit(X_train, y_train)
    
    # Evaluate
    train_accuracy = model.score(X_train, y_train)
    val_accuracy = model.score(X_val, y_val)
    
    print(f"\nModel Type: {model_type.replace('_', ' ').title()}")
    print(f"Training accuracy: {train_accuracy:.4f}")
    print(f"Validation accuracy: {val_accuracy:.4f}")
    
    # if model_type == "random_forest":
    #     # Print feature importance for random forest
    #     feature_importance = model.feature_importances_
    #     print("\nTop 5 most important board positions:")
    #     for idx in feature_importance.argsort()[-5:][::-1]:
    #         row, col = idx // 3, idx % 3
    #         print(f"Position ({row}, {col}): {feature_importance[idx]:.4f}")
    
    # Save model
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved as {model_filename}")

def train_and_save_model(model_type="random_forest"):
    X, y = prepare_data()
    model = create_random_forest_model() if model_type == "random_forest" else create_decision_tree_model()
    model.fit(X, y)
    
    with open('tictactoe_model.pkl', 'wb') as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    print("Training Decision Tree model...")
    train_model("decision_tree")
    
    print("\nTraining Random Forest model...")
    train_model("random_forest")
