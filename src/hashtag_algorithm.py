import json
import os
from llm import take

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
    """Generate hashtags for the given post text using the LLM."""
    prompt = (
        "Generate 5-8 relevant, professional LinkedIn hashtags for the following post. "
        "Each hashtag should be a single word or compound word (no spaces). "
        "Return only the hashtags, separated by spaces:\n\n"
        f"\"{post_text}\"\n"
    )
    try:
        response = take(prompt)
        # Clean hashtags: remove any non-alphanumeric characters except #
        hashtags = [tag.strip() for tag in response.split() if tag.strip()]
        hashtags = [f"#{tag.strip('#')}" for tag in hashtags]
        return [tag for tag in hashtags if len(tag) > 1]  # Ensure no empty tags
    except Exception as e:
        print(f"Warning: Error generating hashtags: {str(e)}")
        return ["#NIAT", "#GENAI"]  # Fallback to default hashtags

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
