import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Set your API key

def generate_intuition():
    with open('inputs/theorem.txt', 'r') as f:
        theorem = f.read()
    
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    prompt = f"""
    Explain the intuition behind this theorem in a way suitable for creating a visual animation.
    Focus on geometric interpretations, key steps, or relationships between objects. 
    Clearly describe what the geometric objects are and how they interact with each other.
    Return the explanation in 2-3 paragraphs.
    
    Theorem: {theorem}
    """
    response = model.generate_content(prompt)
    intuition = response.text
    
    with open('inputs/intuition.txt', 'w') as f:
        f.write(intuition)
    return intuition

if __name__ == "__main__":
    intuition = generate_intuition()
    print("Generated Intuition:\n", intuition)
