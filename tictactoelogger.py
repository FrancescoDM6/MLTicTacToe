import os
import json
from datetime import datetime
import time
import psutil
from pathlib import Path
import pandas as pd
import numpy as np

class TicTacToeLogger:
    def __init__(self):
        """
        Creates clear, readable performance analysis files
        MLTicTacToe/
        └── analysis/
            ├── model_performance.md      # Overall model performance
            ├── training_history.csv      # History of all training runs
            ├── game_statistics.csv       # Statistics from gameplay
            ├── performance_metrics.md    # Detailed performance analysis
            └── game_patterns.md         # Analysis of gameplay patterns
        """
        self.base_path = Path('analysis')
        self.base_path.mkdir(exist_ok=True)
        
    def log_training_results(self, results):
        """Log training results with expanded metrics"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        model_type = results['model_type']

        # Update performance history CSV
        history_file = self.base_path / 'training_history.csv'
        history_row = {
            'timestamp': timestamp,
            'model_type': model_type,
            'train_accuracy': results['train_accuracy'],
            'val_accuracy': results['val_accuracy'],
            'cv_score_mean': results['cv_score_mean'],
            'dataset_size': results['dataset_size'],
            'training_time': results.get('training_time', 0),
            'model_size': results.get('model_size', 0)
        }
        
        if history_file.exists():
            df = pd.read_csv(history_file)
            df = pd.concat([df, pd.DataFrame([history_row])], ignore_index=True)
        else:
            df = pd.DataFrame([history_row])
        df.to_csv(history_file, index=False)

        # Create/Update readable performance report
        performance_file = self.base_path / 'model_performance.md'
        with open(performance_file, 'a') as f:
            f.write(f"\n## {model_type.replace('_', ' ').title()} Performance - {timestamp}\n\n")
            
            # f.write("### Training Information\n")
            # f.write(f"- Training Duration: {results.get('training_time', 'N/A')} seconds\n")
            # f.write(f"- Model Size: {results.get('model_size', 'N/A')} MB\n")
            # f.write(f"- Average Prediction Time: {results.get('avg_prediction_time', 'N/A')} ms\n\n")
            
            f.write("### Performance Metrics\n")
            f.write(f"- Training Accuracy: {results['train_accuracy']:.2%}\n")
            f.write(f"- Validation Accuracy: {results['val_accuracy']:.2%}\n")
            f.write(f"- Cross-validation Score: {results['cv_score_mean']:.2%} (std: {results['cv_score_std']*2:.2%})\n\n")
            
            f.write("### Confusion Matrix Analysis\n")
            conf_matrix = results['confusion_matrix']
            true_neg, false_pos, false_neg, true_pos = conf_matrix.ravel()
            total = sum(conf_matrix.ravel())
            
            f.write(f"- Total Predictions: {total:,}\n")
            f.write(f"- Correct Predictions: {true_pos + true_neg:,} ({(true_pos + true_neg)/total:.2%})\n")
            f.write(f"- False Positives: {false_pos:,} ({false_pos/total:.2%})\n")
            f.write(f"- False Negatives: {false_neg:,} ({false_neg/total:.2%})\n")
            f.write(f"- Precision: {true_pos/(true_pos + false_pos):.2%}\n")
            f.write(f"- Recall: {true_pos/(true_pos + false_neg):.2%}\n\n")
            
            if results.get('feature_importances'):
                f.write("### Feature Importance Analysis\n")
                f.write("Most Important Features:\n")
                sorted_features = sorted(
                    results['feature_importances'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
                for feature, importance in sorted_features:
                    f.write(f"- {feature}: {importance:.2%}\n")
                f.write("\n")
            
            f.write("### Model Configuration\n")
            if results.get('model_params'):
                for param, value in results['model_params'].items():
                    f.write(f"- {param}: {value}\n")
            f.write("\n")
            
            f.write("### Dataset Information\n")
            f.write(f"- Total Samples: {results['dataset_size']:,}\n")
            f.write(f"- Training Set: {results['train_size']:,}\n")
            f.write(f"- Validation Set: {results['val_size']:,}\n")
            # f.write(f"- Memory Usage Peak: {results.get('peak_memory', 'N/A')} MB\n\n")
            f.write("-" * 80 + "\n\n")

    def log_game_results(self, game_data):
        """Log gameplay results with expanded analysis"""
        stats_file = self.base_path / 'game_statistics.csv'
        
        # Calculate additional metrics
        total_moves = len(game_data['moves'])
        center_moves = sum(1 for move in game_data['moves'] if move == (1,1))
        corner_moves = sum(1 for move in game_data['moves'] 
                         if move in [(0,0), (0,2), (2,0), (2,2)])
        
        stats_row = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'model_type': game_data['model_type'],
            'result': game_data['result'],
            'total_moves': total_moves,
            'center_moves': center_moves,
            'corner_moves': corner_moves,
            'model_played_first': game_data.get('model_played_first', True),
            'avg_move_time': game_data.get('avg_move_time', 0),
            'game_duration': game_data.get('game_duration', 0)
        }
        
        if stats_file.exists():
            df = pd.read_csv(stats_file)
            df = pd.concat([df, pd.DataFrame([stats_row])], ignore_index=True)
        else:
            df = pd.DataFrame([stats_row])
        df.to_csv(stats_file, index=False)
        
        # Update game patterns analysis
        self._update_game_patterns(df)

    def _update_game_patterns(self, df):
        """Generate comprehensive game pattern analysis"""
        patterns_file = self.base_path / 'game_patterns.md'
        with open(patterns_file, 'w') as f:
            f.write("# TicTacToe AI Game Pattern Analysis\n\n")
            f.write(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall statistics
            total_games = len(df)
            wins = (df['result'] == 'win').sum()
            losses = (df['result'] == 'loss').sum()
            draws = (df['result'] == 'draw').sum()
            
            f.write("## Overall Performance\n")
            f.write(f"- Total Games: {total_games:,}\n")
            f.write(f"- Wins: {wins:,} ({wins/total_games:.2%})\n")
            f.write(f"- Losses: {losses:,} ({losses/total_games:.2%})\n")
            f.write(f"- Draws: {draws:,} ({draws/total_games:.2%})\n\n")
            
            # Movement patterns
            avg_moves = df['total_moves'].mean()
            avg_center = df['center_moves'].mean()
            avg_corners = df['corner_moves'].mean()
            
            f.write("## Movement Patterns\n")
            f.write(f"- Average Moves per Game: {avg_moves:.1f}\n")
            f.write(f"- Average Center Moves: {avg_center:.1f}\n")
            f.write(f"- Average Corner Moves: {avg_corners:.1f}\n\n")
            
            # Performance by starting position
            f.write("## Performance by Starting Position\n")
            first_move = df[df['model_played_first']]
            second_move = df[~df['model_played_first']]
            
            if len(first_move) > 0:
                first_wr = (first_move['result'] == 'win').sum() / len(first_move)
                f.write(f"- Playing First: {first_wr:.2%} win rate ({len(first_move)} games)\n")
            
            if len(second_move) > 0:
                second_wr = (second_move['result'] == 'win').sum() / len(second_move)
                f.write(f"- Playing Second: {second_wr:.2%} win rate ({len(second_move)} games)\n\n")
            
            # Recent performance trends
            recent = df.tail(20)
            recent_wr = (recent['result'] == 'win').sum() / len(recent)
            f.write("## Recent Performance (Last 20 Games)\n")
            f.write(f"- Win Rate: {recent_wr:.2%}\n")
            f.write(f"- Average Game Duration: {recent['game_duration'].mean():.1f} seconds\n")
            f.write(f"- Average Move Time: {recent['avg_move_time'].mean():.3f} seconds\n\n")
            
            # Performance by model type
            f.write("## Performance by Model Type\n")
            for model in df['model_type'].unique():
                model_games = df[df['model_type'] == model]
                model_wins = (model_games['result'] == 'win').sum()
                f.write(f"\n### {model.replace('_', ' ').title()}\n")
                f.write(f"- Games Played: {len(model_games):,}\n")
                f.write(f"- Win Rate: {model_wins/len(model_games):.2%}\n")
                f.write(f"- Average Game Length: {model_games['total_moves'].mean():.1f} moves\n")

    def _update_win_rate_analysis(self, df):
        """
        Generate win rate analysis
        """
        analysis_file = self.base_path / 'win_rate_analysis.md'
        with open(analysis_file, 'w') as f:
            f.write("# TicTacToe AI Win Rate Analysis\n\n")
            
            # Overall statistics
            total_games = len(df)
            wins = (df['result'] == 'win').sum()
            losses = (df['result'] == 'loss').sum()
            draws = (df['result'] == 'draw').sum()
            
            f.write(f"## Overall Performance (Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
            f.write(f"- Total Games: {total_games:,}\n")
            f.write(f"- Wins: {wins:,} ({wins/total_games:.2%})\n")
            f.write(f"- Losses: {losses:,} ({losses/total_games:.2%})\n")
            f.write(f"- Draws: {draws:,} ({draws/total_games:.2%})\n\n")
            
            # Recent performance (last 20 games)
            recent = df.tail(20)
            recent_wins = (recent['result'] == 'win').sum()
            f.write("## Recent Performance (Last 20 Games)\n")
            f.write(f"- Win Rate: {recent_wins/len(recent):.2%}\n\n")
            
            # Performance by model type
            f.write("## Performance by Model Type\n")
            for model in df['model_type'].unique():
                model_games = df[df['model_type'] == model]
                model_wins = (model_games['result'] == 'win').sum()
                f.write(f"### {model.replace('_', ' ').title()}\n")
                f.write(f"- Games: {len(model_games):,}\n")
                f.write(f"- Win Rate: {model_wins/len(model_games):.2%}\n\n")