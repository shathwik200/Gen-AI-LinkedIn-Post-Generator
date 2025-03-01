from flask import Flask, request, jsonify, render_template
import os
import json
import sys

# Add the backend directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import post_generation
import hashtag_algorithm

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_post', methods=['POST'])
def generate_post():
    data = request.json
    user_idea = data.get('idea')
    
    if not user_idea:
        return jsonify({"error": "No idea provided"}), 400
    
    try:
        post_generation.main(user_idea)
        hashtag_algorithm.main()  # Ensure hashtags are generated and saved
        return jsonify({"message": "Post generated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_hashtags', methods=['POST'])
def generate_hashtags():
    try:
        hashtag_algorithm.main()
        return jsonify({"message": "Hashtags generated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_post', methods=['GET'])
def get_post():
    post_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'post.json')
    
    if not os.path.exists(post_data_path):
        return jsonify({"error": "Post data not found"}), 404
    
    with open(post_data_path, 'r') as file:
        post_data = json.load(file)
    
    return jsonify(post_data), 200

if __name__ == "__main__":
    app.run(debug=True)
