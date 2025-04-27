import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Set your API key

def generate_intuition():
    with open('inputs/theorem.txt', 'r') as f:
        theorem = f.read()
    
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    prompt = f"""
    Explain the intuition behind this theorem in a way specifically optimized for creating a visual animation.

    Focus on:
    - Geometric interpretations, spatial relationships, and dynamic movements.
    - Describing visual elements (points, lines, shapes, curves, vectors, areas, etc.) clearly.
    - Highlighting how these objects interact, transform, or evolve over time.
    - Emphasizing step-by-step visual clarity — avoid abstract descriptions without a clear visual counterpart.

    Write in 2–3 paragraphs.
    Keep the explanation intuitive, vivid, and easy to map to a visual sequence.

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
