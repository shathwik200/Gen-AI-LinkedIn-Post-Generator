import json
import os
from llm1 import take

def load_post_data(file_path):
    """Load post data from the given file path."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist. Please create the file with the appropriate content.")
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    if isinstance(data, dict) and "text" in data:
        return data["text"], data
    else:
        raise ValueError("Invalid format for post.json. Expected a dict with a 'text' key.")

def generate_hashtags(post_text):
    """Generate optimized hashtags using enhanced prompt engineering."""
    prompt = (
        "As a LinkedIn hashtag optimization expert, analyze this post and:\n\n"
        "1. Generate 5-7 highly relevant professional hashtags\n"
        "2. Focus on trending industry-specific tags\n"
        "3. Include a mix of:\n"
        "   - High-volume hashtags (100k+ followers)\n"
        "   - Niche-specific hashtags\n"
        "   - Trending tech hashtags\n\n"
        "Rules:\n"
        "- No spaces in hashtags\n"
        "- No special characters except hyphens\n"
        "- Keep hashtags under 20 characters\n"
        "- No generic terms like 'success' or 'motivation'\n\n"
        f"Post text:\n{post_text}\n\n"
        "Return only the hashtags, separated by spaces:"
    )

    try:
        response = take(prompt)
        # Enhanced hashtag cleaning and validation
        hashtags = [
            f"#{tag.strip('#').lower()}" 
            for tag in response.split() 
            if tag.strip() and len(tag) <= 20
        ]
        
        # Remove duplicates while preserving order
        seen = set()
        hashtags = [
            tag for tag in hashtags 
            if not (tag.lower() in seen or seen.add(tag.lower()))
        ]
        
        return hashtags[:7]  # Limit to top 7 hashtags
    except Exception as e:
        print(f"Warning: Error generating hashtags: {str(e)}")
        return ["#NIAT", "#GENAI"]

def save_post_data(file_path, data):
    """Save the updated post data to the given file path."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    # Determine the project's root directory and relevant file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    post_data_path = os.path.join(project_root, 'data', 'post.json')

    # Load the new post text
    new_post_text, data = load_post_data(post_data_path)

    # Generate hashtags for the post
    base_hashtags = ["#NIAT", "#GENAI"]
    generated_hashtags = generate_hashtags(new_post_text)
    hashtags_list = base_hashtags + generated_hashtags

    # Remove duplicates while preserving order and limit to a maximum number of hashtags (e.g., 10)
    max_hashtags = 10
    unique_hashtags = list(dict.fromkeys(hashtags_list))[:max_hashtags]

    # Add the generated hashtags to the JSON data
    data["hashtag"] = unique_hashtags

    # Save the updated JSON data
    save_post_data(post_data_path, data)

if __name__ == "__main__":
    main()
