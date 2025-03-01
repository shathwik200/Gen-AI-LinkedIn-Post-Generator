import json
import os
from collections import defaultdict

def load_raw_data():
    """Load and analyze raw data patterns"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_path = os.path.join(script_dir, '..', 'data', 'raw_data.json')
    
    with open(raw_data_path, 'r') as file:
        data = json.load(file)
    
    patterns = analyze_patterns(data)
    return patterns

def analyze_patterns(data):
    """Analyze successful post patterns"""
    patterns = {
        'high_engagement': [],
        'successful_hashtags': defaultdict(int),
        'optimal_length': 0,
        'tone_distribution': defaultdict(int),
        'best_readability': 0
    }
    
    # Analyze high-performing posts (engagement > 7)
    high_engagement_posts = [post for post in data if post['engagement'] > 7]
    patterns['high_engagement'] = high_engagement_posts
    
    # Collect successful hashtags
    for post in high_engagement_posts:
        for tag in post['hashtags']:
            patterns['successful_hashtags'][tag] += 1
    
    # Calculate optimal length and readability
    lengths = [len(post['text'].split()) for post in high_engagement_posts]
    patterns['optimal_length'] = sum(lengths) // len(lengths) if lengths else 0
    
    # Analyze tone distribution
    for post in data:
        patterns['tone_distribution'][post['tone']] += 1
        
    # Find best readability score
    patterns['best_readability'] = max(post['readability'] for post in data)
    
    return patterns

def get_post_recommendations(patterns):
    """Generate recommendations based on patterns"""
    return {
        'optimal_length': patterns['optimal_length'],
        'recommended_tone': max(patterns['tone_distribution'].items(), key=lambda x: x[1])[0],
        'top_hashtags': sorted(patterns['successful_hashtags'].items(), key=lambda x: x[1], reverse=True)[:5],
        'target_readability': patterns['best_readability']
    }
