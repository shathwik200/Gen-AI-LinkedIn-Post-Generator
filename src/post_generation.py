import json
import os
from llm import take  # changed from llm1 to llm
from data_analyzer import load_raw_data, get_post_recommendations

def save_post_data(file_path, post_data):
    """Save post data (only text) to the given file path."""
    with open(file_path, 'w') as file:
        json.dump(post_data, file, indent=4)

def main(user_idea, regenerate=False):
    if not user_idea or not isinstance(user_idea, str):
        raise ValueError("User idea must be a non-empty string")

    # Add temperature randomization for regeneration
    temperature = 0.9 if regenerate else 0.7
    
    # Get patterns and recommendations from raw data
    patterns = load_raw_data()
    recommendations = get_post_recommendations(patterns)
    
    # Prepare training examples from high-engagement posts (limit to 2 examples)
    high_engagement_posts = sorted(patterns, key=lambda x: x.get("engagement", 0), reverse=True)[:2]
    training_examples = ""
    for i, post in enumerate(high_engagement_posts, start=1):
        training_examples += f"Example {i}: {post['text']}\n"
    
    # Enhanced prompt with data-driven insights and training examples
    base_prompt = (
        "As a LinkedIn content optimization expert, create an engaging post following these data-driven guidelines:\n\n"
        f"TARGET METRICS:\n"
        f"- Optimal word count: {recommendations['optimal_length']} words\n"
        f"- Target readability score: {recommendations['target_readability']:.2f}\n"
        f"- Recommended tone: {recommendations['recommended_tone']}\n\n"
        "STRUCTURAL ELEMENTS:\n"
        "1. Hook: Start with an attention-grabbing first line\n"
        "2. Value: Clearly state the benefit or insight\n"
        "3. Story: Share a brief narrative or example\n"
        "4. CTA: End with an engaging question or call-to-action\n\n"
        "ENGAGEMENT RULES:\n"
        "- Use 5-6 relevant emojis strategically\n"
        "- Include line breaks for readability\n"
        "- Keep paragraphs short (5-6 lines)\n"
        "- Create curiosity and discussion\n\n"
        f"TRAINING EXAMPLES:\n{training_examples}\n"
        f"USER IDEA: {user_idea}\n\n"
        "Generate a LinkedIn post optimized for maximum engagement:"
    )
    
    if regenerate:
        prompt = base_prompt + "\n\nNOTE: Generate a fresh perspective with different wording and structure while maintaining the core message."
    else:
        prompt = base_prompt

    try:
        # Pass temperature to take() function
        generated_post = take(prompt, temperature=temperature)
        generated_post = (generated_post
            .replace('#', '')
            .strip()
            .replace('\n\n\n', '\n\n')
        )
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        post_data_path = os.path.join(script_dir, '..', 'data', 'post.json')
        
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
