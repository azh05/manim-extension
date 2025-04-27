#!/usr/bin/env python
import sys
import os
import google.generativeai as genai

def main():
    # Expect: python make_intuition.py "<latex>" <out_dir>
    if len(sys.argv) < 3:
        print("Usage: make_intuition.py \"<latex>\" <out_dir>", file=sys.stderr)
        sys.exit(1)

    latex_input = sys.argv[1]
    out_dir     = sys.argv[2]

    # 1) Ensure output folder exists
    os.makedirs(out_dir, exist_ok=True)

    # 2) Configure Gemini API key from ENV
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set in environment", file=sys.stderr)
        sys.exit(1)
    genai.configure(api_key=api_key)

    # 3) Generate intuition text
    intuition = generate_intuition(latex_input)

    # 4) Write to file in out_dir
    out_path = os.path.join(out_dir, "intuition.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(intuition)

    # 5) Print to stdout so your JS can capture it
    print(intuition)


def generate_intuition(latex: str) -> str:
    """Call Gemini to explain the intuition behind the given LaTeX theorem/formula."""
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

    prompt = f"""
Explain the intuition behind this theorem or formula in a way suitable for creating a visual animation.
Focus on geometric interpretations, key steps, or relationships between objects.
Clearly describe what the geometric objects are and how they interact with each other.
Return the explanation in 2-3 paragraphs.

Theorem/Formula: {latex}
"""
    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    main()
