# analyze_results.py
import matplotlib.pyplot as plt
import pandas as pd
import json
from pathlib import Path
import numpy as np
import seaborn as sns

# def analyze_and_plot_random_games():
#     current_dir = Path(__file__).parent
#     results_file = current_dir / 'analysis' / 'model_vs_random_results.csv'
    
#     if not results_file.exists():
#         print("No model vs random results file found")
#         return
        
#     df = pd.read_csv(results_file)
    
#     # 1. Overall Win Rates
#     plt.figure(figsize=(15, 8))
#     win_rates = df.groupby('model_type')['result'].apply(
#         lambda x: (x == 'win').mean() * 100
#     )
#     draw_rates = df.groupby('model_type')['result'].apply(
#         lambda x: (x == 'draw').mean() * 100
#     )
#     loss_rates = df.groupby('model_type')['result'].apply(
#         lambda x: (x == 'loss').mean() * 100
#     )
    
#     # Sort by win rate for better visualization
#     model_order = win_rates.sort_values(ascending=False).index
#     win_rates = win_rates[model_order]
#     draw_rates = draw_rates[model_order]
#     loss_rates = loss_rates[model_order]
    
#     bar_width = 0.25
#     r1 = np.arange(len(win_rates))
#     r2 = [x + bar_width for x in r1]
#     r3 = [x + bar_width for x in r2]
    
#     plt.bar(r1, win_rates, bar_width, label='Wins', color='green')
#     plt.bar(r2, draw_rates, bar_width, label='Draws', color='yellow')
#     plt.bar(r3, loss_rates, bar_width, label='Losses', color='red')
    
#     plt.xlabel('Model Type')
#     plt.ylabel('Percentage')
#     plt.title('Model Performance vs Random Agent')
#     plt.xticks([r + bar_width for r in range(len(win_rates))], 
#                model_order, 
#                rotation=45, 
#                ha='right')
#     plt.legend()
    
#     # Add value labels on bars
#     for i, v in enumerate(win_rates):
#         plt.text(r1[i], v, f'{v:.1f}%', ha='center', va='bottom')
#     for i, v in enumerate(draw_rates):
#         plt.text(r2[i], v, f'{v:.1f}%', ha='center', va='bottom')
#     for i, v in enumerate(loss_rates):
#         plt.text(r3[i], v, f'{v:.1f}%', ha='center', va='bottom')
    
#     plt.tight_layout()
#     plt.savefig(str(current_dir / 'analysis' / 'random_games_overall.png'))
#     plt.close()
    
#     # 2. Performance by Playing First vs Second
#     plt.figure(figsize=(15, 8))
#     first_vs_second = df.groupby(['model_type', 'model_played_first'])['result'].apply(
#         lambda x: (x == 'win').mean() * 100
#     ).unstack()
    
#     # Sort by overall performance
#     first_vs_second = first_vs_second.loc[model_order]
    
#     first_vs_second.plot(kind='bar', width=0.8)
#     plt.title('Win Rates: Playing First vs Second')
#     plt.xlabel('Model Type')
#     plt.ylabel('Win Rate (%)')
#     plt.legend(['Playing Second', 'Playing First'])
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.savefig(str(current_dir / 'analysis' / 'random_games_first_vs_second.png'))
#     plt.close()
    
#     # 3. Win Methods Distribution
#     plt.figure(figsize=(15, 8))
#     win_methods = df[df['result'] == 'win'].groupby(['model_type', 'win_method']).size().unstack(fill_value=0)
#     win_methods = win_methods.loc[model_order]
    
#     win_methods.plot(kind='bar', stacked=True)
#     plt.title('Distribution of Win Methods by Model Type')
#     plt.xlabel('Model Type')
#     plt.ylabel('Number of Wins')
#     plt.legend(title='Win Method')
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.savefig(str(current_dir / 'analysis' / 'random_games_win_methods.png'))
#     plt.close()
    
#     # 4. Game Length Analysis
#     plt.figure(figsize=(15, 8))
#     df_wins = df[df['result'] == 'win']
#     game_lengths = df_wins.groupby('model_type')['num_moves'].agg(['mean', 'std'])
#     game_lengths = game_lengths.loc[model_order]
    
#     plt.errorbar(range(len(game_lengths)), game_lengths['mean'], 
#                 yerr=game_lengths['std'], fmt='o', capsize=5)
#     plt.title('Average Game Length for Wins')
#     plt.xlabel('Model Type')
#     plt.ylabel('Number of Moves')
#     plt.xticks(range(len(game_lengths)), game_lengths.index, rotation=45, ha='right')
#     plt.tight_layout()
#     plt.savefig(str(current_dir / 'analysis' / 'random_games_length.png'))
#     plt.close()
    
#     # Print summary statistics
#     print("\nModel vs Random Agent Performance Summary:")
#     print("\nOverall Win Rates:")
#     print(win_rates)
#     print("\nWin Rates by Playing Order:")
#     print(first_vs_second)
#     print("\nWin Methods Distribution:")
#     print(win_methods)
#     print("\nAverage Game Length (Wins Only):")
#     print(game_lengths)

# def analyze_and_plot_random_games(filename='optimized_model_vs_random_results.csv'):
#     current_dir = Path(__file__).parent
#     results_file = current_dir / 'analysis' / filename
    
#     if not results_file.exists():
#         print(f"No results file found: {filename}")
#         return
        
#     df = pd.read_csv(results_file)
    
#     # Process move data if needed
#     # df['moves'] = df['moves'].apply(eval)  # Convert string to list if we need to analyze moves
    
#     # Basic Statistics
#     print("\nBasic Statistics:")
#     print(f"Total games played: {len(df)}")
#     for model in df['model_type'].unique():
#         model_games = df[df['model_type'] == model]
#         print(f"\n{model}:")
#         print(f"Total games: {len(model_games)}")
#         print(f"Wins: {(model_games['result'] == 'win').sum()}")
#         print(f"Average moves per game: {model_games['num_moves'].mean():.2f}")
#         win_method_dist = model_games[model_games['result'] == 'win']['win_method'].value_counts()
#         print("Win method distribution:")
#         print(win_method_dist)
    
#     # 1. Overall Performance Bar Plot
#     plt.figure(figsize=(12, 6))
#     win_rates = df.groupby('model_type')['result'].apply(
#         lambda x: (x == 'win').mean() * 100
#     ).sort_values(ascending=False)
    
#     plt.bar(range(len(win_rates)), win_rates)
#     plt.title('Win Rates by Model Type')
#     plt.xlabel('Model Type')
#     plt.ylabel('Win Rate (%)')
#     plt.xticks(range(len(win_rates)), win_rates.index, rotation=45, ha='right')
    
#     # Add percentage labels on bars
#     for i, v in enumerate(win_rates):
#         plt.text(i, v, f'{v:.1f}%', ha='center', va='bottom')
    
#     plt.tight_layout()
#     plt.savefig(str(current_dir / 'analysis' / 'optimized_win_rates.png'))
#     plt.close()
    
#     # 2. Game Length Distribution
#     plt.figure(figsize=(12, 6))
#     df_wins = df[df['result'] == 'win']
#     sns.boxplot(data=df_wins, x='model_type', y='num_moves')
#     plt.title('Distribution of Moves for Winning Games')
#     plt.xlabel('Model Type')
#     plt.ylabel('Number of Moves')
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.savefig(str(current_dir / 'analysis' / 'optimized_game_lengths.png'))
#     plt.close()
    
#     # 3. Win Method Distribution
#     plt.figure(figsize=(12, 6))
#     win_methods = df[df['result'] == 'win'].groupby(['model_type', 'win_method']).size().unstack(fill_value=0)
#     win_methods.plot(kind='bar', stacked=True)
#     plt.title('Win Methods by Model Type')
#     plt.xlabel('Model Type')
#     plt.ylabel('Number of Wins')
#     plt.legend(title='Win Method')
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.savefig(str(current_dir / 'analysis' / 'optimized_win_methods.png'))
#     plt.close()
    
#     # 4. First Move Analysis (if needed)
#     if df['moves'].dtype == str:
#         df['first_move'] = df['moves'].apply(lambda x: eval(x)[0][1] if len(eval(x)) > 0 else None)
#         first_moves = df.groupby('model_type')['first_move'].apply(list)
#         print("\nFirst Move Analysis:")
#         for model in first_moves.index:
#             moves = first_moves[model]
#             print(f"\n{model}:")
#             from collections import Counter
#             print(Counter(moves))
    
#     return df

def write_detailed_stats(df, model_order, current_dir):
    stats_file = current_dir / 'analysis' / 'training_metrics.md'
    metrics_file = current_dir / 'analysis' / 'training_history.csv'

    # Load metrics and handle missing values
    metrics_df = pd.read_csv(metrics_file)
    metrics_df.fillna(0, inplace=True)  # Replace missing values with 0

    # Get the latest training results for each model type
    latest_metrics = metrics_df.sort_values('timestamp').groupby('model_type').last()
    latest_metrics.reset_index(inplace=True)  # Ensure model_type is accessible as a column

    # Prepare data for plotting
    plot_data = []
    for model in model_order:
        if model in latest_metrics['model_type'].values:
            metrics = latest_metrics[latest_metrics['model_type'] == model].iloc[0]
            plot_data.append({
                'Model': model,
                'Training Accuracy': metrics['train_accuracy'],
                'Validation Accuracy': metrics['val_accuracy'],
                'CV Score': metrics['cv_score_mean']
            })
        else:
            print(f"Model {model} is missing in the metrics data.")

    # Ensure plot data is not empty
    if not plot_data:
        print("No data available for plotting. Please check the CSV content.")
        return

    plot_df = pd.DataFrame(plot_data)

    # Plot
    plt.figure(figsize=(15, 8))
    x = np.arange(len(plot_df))
    width = 0.25

    plt.bar(x - width, plot_df['Training Accuracy'], width, label='Training Accuracy')
    plt.bar(x, plot_df['Validation Accuracy'], width, label='Validation Accuracy')
    plt.bar(x + width, plot_df['CV Score'], width, label='CV Score')

    plt.xlabel('Model Type')
    plt.ylabel('Score')
    plt.title('Model Training Metrics Comparison')
    plt.xticks(x, plot_df['Model'], rotation=45, ha='right')
    plt.legend()

    # Add value labels
    for i, row in plot_df.iterrows():
        plt.text(i - width, row['Training Accuracy'], f"{row['Training Accuracy']:.3f}", ha='center', va='bottom')
        plt.text(i, row['Validation Accuracy'], f"{row['Validation Accuracy']:.3f}", ha='center', va='bottom')
        plt.text(i + width, row['CV Score'], f"{row['CV Score']:.3f}", ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'training_metrics_comparison.png'))
    plt.close()

    # Write metrics to markdown
    with open(stats_file, 'w') as f:
        f.write('# Model Training Metrics\n\n')

        for model in model_order:
            if model in latest_metrics['model_type'].values:
                metrics = latest_metrics[latest_metrics['model_type'] == model].iloc[0]
                f.write(f"## {model}\n\n")
                f.write(f"- Training Accuracy: {metrics['train_accuracy']:.4f}\n")
                f.write(f"- Validation Accuracy: {metrics['val_accuracy']:.4f}\n")
                f.write(f"- CV Score: {metrics['cv_score_mean']:.4f}\n")
                f.write(f"- Dataset Size: {int(metrics['dataset_size'])}\n")
                if metrics['training_time'] > 0:
                    f.write(f"- Training Time: {metrics['training_time']:.2f} seconds\n")
                if metrics['model_size'] > 0:
                    f.write(f"- Model Size: {metrics['model_size']:.2f} MB\n")
                f.write('\n---\n\n')

def analyze_and_plot_random_games(filename='final_model_vs_random_results.csv'):
    current_dir = Path(__file__).parent
    results_file = current_dir / 'analysis' / filename
    
    if not results_file.exists():
        print(f"No results file found: {filename}")
        return
        
    df = pd.read_csv(results_file)
    
    # Data Verification
    print("\nData Distribution:")
    model_counts = df.groupby(['model_type', 'model_played_first']).size().unstack(fill_value=0)
    print("\nGames per model and position:")
    print(model_counts)
    
    # 1. Split Performance by First/Second Player
    plt.figure(figsize=(15, 8))
    
    first_data = df[df['model_played_first']]
    second_data = df[~df['model_played_first']]
    
    # Calculate win rates for each condition
    first_wins = first_data.groupby('model_type')['result'].apply(
        lambda x: (x == 'win').mean() * 100
    )
    second_wins = second_data.groupby('model_type')['result'].apply(
        lambda x: (x == 'win').mean() * 100
    )
    
    # Sort by overall performance
    overall_wins = df.groupby('model_type')['result'].apply(
        lambda x: (x == 'win').mean() * 100
    ).sort_values(ascending=False)
    model_order = overall_wins.index
    
    x = np.arange(len(model_order))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(15, 8))
    rects1 = ax.bar(x - width/2, [first_wins[model] for model in model_order], width, 
                    label='Playing First', color='skyblue')
    rects2 = ax.bar(x + width/2, [second_wins[model] for model in model_order], width,
                    label='Playing Second', color='lightgreen')
    
    ax.set_ylabel('Win Rate (%)')
    ax.set_title('Model Win Rates by Playing Position')
    ax.set_xticks(x)
    ax.set_xticklabels(model_order, rotation=45, ha='right')
    ax.legend()
    
    # Add value labels on bars
    for rect in rects1 + rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                   xy=(rect.get_x() + rect.get_width()/2, height),
                   xytext=(0, 3),
                   textcoords="offset points",
                   ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'win_rates_by_position.png'))
    plt.close()
    
    # 2. Win Method Distribution
    plt.figure(figsize=(15, 8))
    win_methods = df[df['result'] == 'win'].groupby(['model_type', 'win_method']).size().unstack(fill_value=0)
    win_methods = win_methods.reindex(model_order)
    
    win_methods.plot(kind='bar', stacked=True)
    plt.title('Win Methods Distribution by Model Type')
    plt.xlabel('Model Type')
    plt.ylabel('Number of Wins')
    plt.legend(title='Win Method')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'win_methods_distribution.png'))
    plt.close()
    
    # # Print detailed statistics
    # print("\nDetailed Performance Statistics:")
    # for model in model_order:
    #     model_data = df[df['model_type'] == model]
    #     print(f"\n{model}")
    #     print(f"Total games: {len(model_data)}")
    #     print(f"Overall win rate: {(model_data['result'] == 'win').mean():.2%}")
    #     print(f"Win rate as first: {(model_data[model_data['model_played_first']]['result'] == 'win').mean():.2%}")
    #     print(f"Win rate as second: {(model_data[~model_data['model_played_first']]['result'] == 'win').mean():.2%}")
    #     print(f"Average moves per game: {model_data['num_moves'].mean():.2f}")
    #     print("\nWin methods:")
    #     print(model_data[model_data['result'] == 'win']['win_method'].value_counts())
    #     print(f"\nFirst move distribution:")
    #     print(model_data['first_move'].value_counts())
    #     print(f"\nWin rates by game length:")
    #     print(model_data.groupby('game_length_cat')['result'].apply(
    #         lambda x: (x == 'win').mean()
    #     ).round(3))



    # Add after existing plots
    plt.figure(figsize=(15, 8))
    sns.boxplot(data=df, x='model_type', y='num_moves', order=model_order)
    plt.title('Distribution of Game Lengths by Model Type')
    plt.xlabel('Model Type')
    plt.ylabel('Number of Moves')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'game_length_distribution.png'))
    plt.close()

    # Add function to extract first move from moves string
    def get_first_move(moves_str):
        moves = eval(moves_str)
        if moves:
            return moves[0][1]
        return None

    # Analyze first moves
    df['first_move'] = df['moves'].apply(get_first_move)
    plt.figure(figsize=(15, 8))
    first_move_dist = df.groupby(['model_type', 'first_move']).size().unstack(fill_value=0)
    first_move_dist = first_move_dist.reindex(model_order)

    first_move_dist.plot(kind='bar', stacked=True)
    plt.title('First Move Distribution by Model Type')
    plt.xlabel('Model Type')
    plt.ylabel('Count')
    plt.legend(title='First Move Position')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'first_move_distribution.png'))
    plt.close()

    # Create game length categories
    df['game_length_cat'] = pd.cut(df['num_moves'], 
                                bins=[0, 5, 7, 9, float('inf')],
                                labels=['Quick (≤5)', 'Medium (6-7)', 'Long (8-9)', 'Extended (>9)'])

    plt.figure(figsize=(15, 8))
    length_win_rates = df.groupby(['model_type', 'game_length_cat'], observed=True)['result'].apply(
        lambda x: (x == 'win').mean() * 100
    ).unstack()

    length_win_rates = length_win_rates.reindex(model_order)
    length_win_rates.plot(kind='bar', width=0.8)
    plt.title('Win Rates by Game Length')
    plt.xlabel('Model Type')
    plt.ylabel('Win Rate (%)')
    plt.legend(title='Game Length')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'win_rates_by_game_length.png'))
    plt.close()

    # Regular win rates (simpler bar chart)
    plt.figure(figsize=(15, 8))
    win_rates = df.groupby('model_type')['result'].apply(
        lambda x: (x == 'win').mean() * 100
    ).reindex(model_order)

    plt.bar(range(len(win_rates)), win_rates, color='blue')
    plt.title('Overall Win Rates by Model Type')
    plt.xlabel('Model Type')
    plt.ylabel('Win Rate (%)')
    plt.xticks(range(len(win_rates)), win_rates.index, rotation=45, ha='right')

    # Add percentage labels on bars
    for i, v in enumerate(win_rates):
        plt.text(i, v, f'{v:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'overall_win_rates.png'))
    plt.close()

    # Model metrics comparison (using multiple metrics)
    plt.figure(figsize=(15, 8))

    # Calculate various metrics
    metrics = pd.DataFrame({
        'Win Rate': df.groupby('model_type')['result'].apply(lambda x: (x == 'win').mean() * 100),
        'Avg Game Length': df.groupby('model_type')['num_moves'].mean(),
        'First Player WR': df[df['model_played_first']].groupby('model_type')['result'].apply(lambda x: (x == 'win').mean() * 100)
    }).reindex(model_order)

    # Normalize metrics to 0-1 scale for comparison
    metrics_normalized = (metrics - metrics.min()) / (metrics.max() - metrics.min())

    # Plot normalized metrics
    metrics_normalized.plot(kind='bar', width=0.8)
    plt.title('Normalized Model Metrics Comparison')
    plt.xlabel('Model Type')
    plt.ylabel('Normalized Score')
    plt.legend(title='Metrics')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(str(current_dir / 'analysis' / 'model_metrics_comparison.png'))
    plt.close()

    def write_comparative_stats(df, model_order, current_dir):
        stats_file = current_dir / 'analysis' / 'comparative_analysis.md'
        
        with open(stats_file, 'w') as f:
            f.write('# Comparative Model Analysis\n\n')

            # Overall Rankings
            f.write('## Overall Rankings\n\n')
            
            # Win Rate Ranking
            f.write('### Win Rate Rankings\n')
            win_rates = df.groupby('model_type')['result'].apply(
                lambda x: (x == 'win').mean() * 100
            ).sort_values(ascending=False)
            
            for i, (model, rate) in enumerate(win_rates.items(), 1):
                f.write(f"{i}. {model}: {rate:.2f}%\n")
            
            f.write('\n')

            # Average Game Length Comparison
            f.write('### Average Game Length Rankings\n')
            avg_moves = df.groupby('model_type')['num_moves'].mean().sort_values()
            
            for i, (model, moves) in enumerate(avg_moves.items(), 1):
                f.write(f"{i}. {model}: {moves:.2f} moves\n")
            
            f.write('\n')

            # Performance Comparisons
            f.write('## Performance Comparisons\n\n')

            # First vs Second Player Performance
            f.write('### First vs Second Player Advantage\n')
            for model in model_order:
                model_data = df[df['model_type'] == model]
                first_wr = model_data[model_data['model_played_first']]['result'].apply(
                    lambda x: x == 'win'
                ).mean() * 100
                second_wr = model_data[~model_data['model_played_first']]['result'].apply(
                    lambda x: x == 'win'
                ).mean() * 100
                difference = first_wr - second_wr
                
                f.write(f"**{model}**\n")
                f.write(f"- First player advantage: {abs(difference):.2f}% ")
                f.write(f"({'higher' if difference > 0 else 'lower'} as first player)\n\n")

            # Win Method Preferences
            f.write('### Win Method Preferences\n')
            win_methods = df[df['result'] == 'win'].groupby('model_type')['win_method'].value_counts(normalize=True)
            
            for model in model_order:
                if model in win_methods:
                    f.write(f"\n**{model}**\n")
                    model_methods = win_methods[model].sort_values(ascending=False)
                    for method, pct in model_methods.items():
                        f.write(f"- {method}: {pct:.1%}\n")

            # Efficiency Analysis
            f.write('\n## Efficiency Analysis\n\n')
            winning_moves = df[df['result'] == 'win']['num_moves']
            fastest_wins = df[df['result'] == 'win'].groupby('model_type')['num_moves'].agg(['min', 'mean', 'max'])
            
            f.write('### Fastest Wins\n')
            for model in model_order:
                if model in fastest_wins.index:
                    stats = fastest_wins.loc[model]
                    f.write(f"\n**{model}**\n")
                    f.write(f"- Fastest win: {stats['min']} moves\n")
                    f.write(f"- Average winning game: {stats['mean']:.1f} moves\n")
                    f.write(f"- Longest win: {stats['max']} moves\n")

            # Model Similarities
            f.write('\n## Model Similarities\n\n')
            f.write('### First Move Preferences\n')
            first_moves = df.groupby('model_type')['first_move'].value_counts(normalize=True)
            
            for model in model_order:
                if model in first_moves:
                    f.write(f"\n**{model}**\n")
                    model_moves = first_moves[model].sort_values(ascending=False)
                    for move, pct in model_moves.items():
                        f.write(f"- Position {move}: {pct:.1%}\n")

    # Add this to your main analysis function just before return df:
    write_comparative_stats(df, model_order, current_dir)


    model_order = [
        'decision_tree', 'random_forest', 'decision_tree_base_dt',
        'decision_tree_deep_dt', 'decision_tree_gini_dt',
        'random_forest_base_rf', 'random_forest_light_rf', 'random_forest_heavy_rf'
    ]

    write_detailed_stats(df, model_order, current_dir)


    return df

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

# def write_detailed_stats(df, model_order, current_dir):
#     stats_file = current_dir / 'analysis' / 'training_metrics.md'
    
#     metrics_df = pd.read_csv(current_dir / 'analysis' / 'training_history.csv')
    
#     # Get the latest training results for each model type
#     latest_metrics = metrics_df.sort_values('timestamp').groupby('model_type').last()
    
#     # Create visualization
#     plt.figure(figsize=(15, 8))
    
#     # Prepare data for plotting
#     plot_data = []
#     for model in model_order:
#         if model in latest_metrics.index:
#             metrics = latest_metrics.loc[model]
#             if not pd.isnull(metrics['train_accuracy']) and not pd.isnull(metrics['val_accuracy']):
#                 plot_data.append({
#                     'Model': model,
#                     'Training Accuracy': metrics['train_accuracy'],
#                     'Validation Accuracy': metrics['val_accuracy'],
#                     'CV Score': metrics['cv_score_mean']
#                 })
#         else:
#             print(f"Skipping model {model}: Not found in metrics data.")

    
#     plot_df = pd.DataFrame(plot_data)
    
#     # Plot
#     x = np.arange(len(plot_df))
#     width = 0.25
    
#     plt.bar(x - width, plot_df['Training Accuracy'], width, label='Training Accuracy')
#     plt.bar(x, plot_df['Validation Accuracy'], width, label='Validation Accuracy')
#     plt.bar(x + width, plot_df['CV Score'], width, label='CV Score')
    
#     plt.xlabel('Model Type')
#     plt.ylabel('Score')
#     plt.title('Model Training Metrics Comparison')
#     plt.xticks(x, plot_df['Model'], rotation=45, ha='right')
#     plt.legend()
    
#     # Add value labels
#     for i, row in plot_df.iterrows():
#         plt.text(i - width, row['Training Accuracy'], f"{row['Training Accuracy']:.3f}", 
#                 ha='center', va='bottom')
#         plt.text(i, row['Validation Accuracy'], f"{row['Validation Accuracy']:.3f}", 
#                 ha='center', va='bottom')
#         plt.text(i + width, row['CV Score'], f"{row['CV Score']:.3f}", 
#                 ha='center', va='bottom')
    
#     plt.tight_layout()
#     plt.savefig(str(current_dir / 'analysis' / 'training_metrics_comparison.png'))
#     plt.close()
    
#     # Write metrics to markdown
#     with open(stats_file, 'w') as f:
#         f.write('# Model Training Metrics\n\n')
        
#         for model in model_order:
#             if model in latest_metrics.index:
#                 metrics = latest_metrics.loc[model]
#                 f.write(f"## {model}\n\n")
#                 f.write(f"- Training Accuracy: {metrics['train_accuracy']:.4f}\n")
#                 f.write(f"- Validation Accuracy: {metrics['val_accuracy']:.4f}\n")
#                 f.write(f"- CV Score: {metrics['cv_score_mean']:.4f}\n")
#                 f.write(f"- Dataset Size: {int(metrics['dataset_size'])}\n")
#                 if pd.notnull(metrics['training_time']):
#                     f.write(f"- Training Time: {metrics['training_time']:.2f} seconds\n")
#                 if pd.notnull(metrics['model_size']):
#                     f.write(f"- Model Size: {metrics['model_size']:.2f} MB\n")
#                 f.write('\n---\n\n')





if __name__ == "__main__":
    try:
        df = analyze_and_plot_results()
    except Exception as e:
        print(f"Error during analysis: {str(e)}")

    