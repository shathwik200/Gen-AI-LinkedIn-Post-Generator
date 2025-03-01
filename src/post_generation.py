import json
import os
from llm import take

def save_post_data(file_path, post_data):
    """Save post data (only text) to the given file path."""
    with open(file_path, 'w') as file:
        json.dump(post_data, file, indent=4)

def main(user_idea):
    if not user_idea or not isinstance(user_idea, str):
        raise ValueError("User idea must be a non-empty string")

    # Determine the project's root directory and relevant file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    post_data_path = os.path.join(project_root, 'data', 'post.json')

    # Updated prompt with stricter rules
    prompt = (
        "Generate a professional LinkedIn post based on the idea below. Follow these rules strictly:\n"
        "1. DO NOT include any hashtags or # symbols\n"
        "2. DO NOT add any tags or mentions\n"
        "3. Include relevant emojis for engagement\n"
        "4. Keep the tone professional but friendly\n"
        "5. Focus only on the main message\n\n"
        f"Idea: {user_idea}\n\n"
        "Generate the post text only:"
    )

    try:
        generated_post = take(prompt)
        if '#' in generated_post:
            generated_post = generated_post.replace('#', '')
        
        post_data = {"text": generated_post.replace("\n", "\\n")}
        save_post_data(post_data_path, post_data)
    except Exception as e:
        raise Exception(f"Error generating post: {str(e)}")

if __name__ == "__main__":
    # Example usage
    user_idea = (
        "Unveiling the future of creativity: Our team’s latest generative AI model can compose music, "
        "design visuals, and draft content—all in seconds. Imagine the possibilities for streamlining workflows "
        "and sparking innovation. How do you see Gen AI reshaping your industry?"
    )
    main(user_idea)
