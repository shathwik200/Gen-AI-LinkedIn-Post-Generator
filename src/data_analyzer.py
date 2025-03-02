import json
import os
from collections import Counter
from collections import defaultdict  # added import for defaultdict

def load_raw_data():
    # Construct the path to the raw_data.json file
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw_data.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Return data with all keys except "hashtags"
    filtered_data = [
        {key: value for key, value in entry.items() if key != "hashtags"}
        for entry in data
    ]
    return filtered_data

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
    """
    Compute recommendations from the list of post dictionaries.
    
    Recommends:
    - optimal_length: average word count across all posts.
    - target_readability: average readability.
    - recommended_tone: most common tone.
    """
    if not patterns:
        return {'optimal_length': 100, 'target_readability': 0.8, 'recommended_tone': 'neutral'}

    total_words = 0
    total_readability = 0
    tones = []

    for entry in patterns:
        text = entry.get("text", "")
        total_words += len(text.split())
        total_readability += entry.get("readability", 0)
        tones.append(entry.get("tone", "neutral"))
    
    avg_words = round(total_words / len(patterns))
    avg_readability = total_readability / len(patterns)
    recommended_tone = Counter(tones).most_common(1)[0][0]

    return {
        'optimal_length': avg_words,
        'target_readability': avg_readability,
        'recommended_tone': recommended_tone
    }
