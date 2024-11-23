import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix, classification_report
import pickle
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
    

    print("\nDataset Information:")
    print(f"Total samples: {len(df)}")
    print("\nClass distribution:")
    print(df['class'].value_counts(normalize=True))

    duplicates = df.duplicated().sum()
    print(f"\nNumber of duplicate rows: {duplicates}")

    # convert board states to numerical values
    mapping = {'x': 1, 'o': -1, 'b': 0}
    X = df.iloc[:, :9].replace(mapping).values
    y = (df['class'] == True).astype(int)  
    
    print("First few rows after processing:")
    print("X:", X[:5])
    print("y:", y[:5])
    
    return X, y

def evaluate_model(model, X_train, X_val, y_train, y_val, model_type):
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
    
    if model_type == "random_forest":
        feature_importance = model.feature_importances_
        print("\nTop 5 most important board positions:")
        positions = ['TL', 'TM', 'TR', 'ML', 'MM', 'MR', 'BL', 'BM', 'BR']
        importance_pairs = list(zip(positions, feature_importance))
        importance_pairs.sort(key=lambda x: x[1], reverse=True)
        for pos, imp in importance_pairs[:5]:
            print(f"Position {pos}: {imp:.4f}")

def train_model(model_type="random_forest"):
    X, y = prepare_data()
    
    if len(X) == 0:
        print("No training data available!")
        return
    
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    if model_type == "decision_tree":
        model = create_decision_tree_model()
        # model_filename = 'tictactoe_random_dt_model.pkl'
        model_filename = 'tictactoe_dt_model.pkl'
    else:  # random_forest
        model = create_random_forest_model()
        # model_filename = 'tictactoe_random_rf_model.pkl'
        model_filename = 'tictactoe_rf_model.pkl'
    
    model.fit(X_train, y_train)
    
    evaluate_model(model, X_train, X_val, y_train, y_val, model_type)
    
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved as {model_filename}")



if __name__ == "__main__":
    print("Training Decision Tree model...")
    train_model("decision_tree")
    
    print("\nTraining Random Forest model...")
    train_model("random_forest")
