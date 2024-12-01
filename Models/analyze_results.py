# analyze_results.py
import matplotlib.pyplot as plt
import pandas as pd
import json
from pathlib import Path
import numpy as np
import seaborn as sns

def analyze_and_plot_random_games():
    """Analyze and plot results of models vs random agents"""
    current_dir = Path(__file__).parent
    results_file = current_dir / 'analysis' / 'model_vs_random_results.csv'
    
    if not results_file.exists():
        print("No model vs random results file found")
        return
        
    df = pd.read_csv(results_file)
    
    # 1. Overall Win Rates
    plt.figure(figsize=(10, 6))
    win_rates = df.groupby('model_type')['result'].apply(
        lambda x: (x == 'win').mean() * 100
    )
    draw_rates = df.groupby('model_type')['result'].apply(
        lambda x: (x == 'draw').mean() * 100
    )
    loss_rates = df.groupby('model_type')['result'].apply(
        lambda x: (x == 'loss').mean() * 100
    )
    
    bar_width = 0.25
    r1 = np.arange(len(win_rates))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    
    plt.bar(r1, win_rates, bar_width, label='Wins', color='green')
    plt.bar(r2, draw_rates, bar_width, label='Draws', color='yellow')
    plt.bar(r3, loss_rates, bar_width, label='Losses', color='red')
    
    plt.xlabel('Model Type')
    plt.ylabel('Percentage')
    plt.title('Model Performance vs Random Agent')
    plt.xticks([r + bar_width for r in range(len(win_rates))], win_rates.index)
    plt.legend()
    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'random_games_overall.png'))
    plt.close()
    
    # 2. Performance by Playing First vs Second
    plt.figure(figsize=(10, 6))
    first_vs_second = df.groupby(['model_type', 'model_played_first'])['result'].apply(
        lambda x: (x == 'win').mean() * 100
    ).unstack()
    
    first_vs_second.plot(kind='bar', width=0.8)
    plt.title('Win Rates: Playing First vs Second')
    plt.xlabel('Model Type')
    plt.ylabel('Win Rate (%)')
    plt.legend(['Playing Second', 'Playing First'])
    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'random_games_first_vs_second.png'))
    plt.close()
    
    # 3. Game Length Distribution
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='model_type', y='num_moves', hue='result')
    plt.title('Game Length Distribution by Outcome')
    plt.xlabel('Model Type')
    plt.ylabel('Number of Moves')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'random_games_length.png'))
    plt.close()
    
    # Print summary statistics
    print("\nModel vs Random Agent Performance Summary:")
    print("\nOverall Win Rates:")
    print(win_rates)
    print("\nWin Rates by Playing Order:")
    print(first_vs_second)
    print("\nAverage Game Length:")
    print(df.groupby('model_type')['num_moves'].mean())

def analyze_and_plot_results():
    # Get the current script's directory (Models)
    current_dir = Path(__file__).parent
    analysis_dir = current_dir / 'analysis'
    
    print("Looking for data files in:", analysis_dir.absolute())
    
    results = {}
    
    # Read CSV files
    training_history = analysis_dir / 'training_history.csv'
    game_statistics = analysis_dir / 'game_statistics.csv'
    
    if training_history.exists():
        print("Reading training history...")
        df = pd.read_csv(training_history)
        
        # Create model comparison plot
        plt.figure(figsize=(12, 6))
        
        # Group by model type and calculate mean metrics
        model_metrics = df.groupby('model_type').agg({
            'train_accuracy': 'mean',
            'val_accuracy': 'mean',
            'cv_score_mean': 'mean'
        }).reset_index()
        
        # Bar plot for different metrics
        x = range(len(model_metrics))
        width = 0.25
        
        plt.bar(x, model_metrics['train_accuracy'], width, label='Training Accuracy', color='blue')
        plt.bar([i + width for i in x], model_metrics['val_accuracy'], width, label='Validation Accuracy', color='green')
        plt.bar([i + width*2 for i in x], model_metrics['cv_score_mean'], width, label='CV Score', color='red')
        
        plt.xlabel('Model Type')
        plt.ylabel('Score')
        plt.title('Model Performance Comparison')
        plt.xticks([i + width for i in x], model_metrics['model_type'], rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.savefig(str(analysis_dir / 'model_comparison.png'))
        plt.close()

    if game_statistics.exists():
        print("Reading game statistics...")
        results['games'] = pd.read_csv(game_statistics)
        
        # Create game statistics plots
        plt.figure(figsize=(12, 6))
        win_rates = results['games'].groupby('model_type')['result'].apply(lambda x: (x == 'win').mean())
        win_rates.plot(kind='bar')
        plt.title('Win Rates by Model Type')
        plt.xlabel('Model Type')
        plt.ylabel('Win Rate')
        plt.tight_layout()
        plt.savefig(str(analysis_dir / 'win_rates.png'))
        plt.close()
    
    # Print summary statistics
    if 'training' in results:
        print("\nModel Performance Summary:")
        print(model_metrics)


    print("\nAnalyzing model vs random agent games...")
    analyze_and_plot_random_games()
    
    return results

    
    

if __name__ == "__main__":
    try:
        df = analyze_and_plot_results()
    except Exception as e:
        print(f"Error during analysis: {str(e)}")