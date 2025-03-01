from openai import OpenAI

def take(user_message):
    try:
        client = OpenAI()
        stream = client.chat.completions.create(
            model="gpt-4o-mini",  # Fixed model name
            messages=[
                {"role": "system", "content": "You are an AI that strictly follows all instructions given by the user."},
                {"role": "user", "content": user_message}
            ],
            stream=True,
        )

        response_parts = []
        for chunk in stream:
            # Ensure the chunk has choices and a valid delta
            if not chunk.choices or len(chunk.choices) == 0:
                continue
            delta = chunk.choices[0].delta
            # Safely attempt to retrieve the "content" using dictionary access or attribute access
            if isinstance(delta, dict):
                content = delta.get("content", "")
            else:
                content = getattr(delta, "content", "")
            if content:
                response_parts.append(content)
        response = "".join(response_parts)
        return response.strip()
    except Exception as e:
        raise Exception(f"Error in LLM processing: {str(e)}")

if __name__ == "__main__":
    message = "Who is the father of AI?"
    print(take(message))
