#!/usr/bin/env python
import sys
import os
import re
import google.generativeai as genai
from manim.__main__ import main as manim_main


def main():
    # Usage: python generate_manim.py "<latex>" <out_dir>
    if len(sys.argv) < 3:
        print("Usage: generate_manim.py \"<latex>\" <out_dir>", file=sys.stderr)
        sys.exit(1)

    latex_input = sys.argv[1]
    out_dir     = sys.argv[2]

    # Ensure output folder exists
    os.makedirs(out_dir, exist_ok=True)

    # Configure API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set in environment", file=sys.stderr)
        sys.exit(1)
    genai.configure(api_key=api_key)

    # Step 1: Generate intuition text
    intuition = generate_intuition(latex_input)
    intuition_path = os.path.join(out_dir, "intuition.txt")
    with open(intuition_path, "w", encoding="utf-8") as f:
        f.write(intuition)

    # Step 2: Draft and refine the Manim script
    final_code = generate_manim_script(latex_input, intuition)
    script_name = "theorem_animation.py"
    script_path = os.path.join(out_dir, script_name)
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(final_code)

    # Step 3: Render the Manim scene with retry logic
    max_render_attempts = 4
    for attempt in range(1, max_render_attempts + 1):
        try:
            render_manim(script_path, out_dir)
            break
        except Exception as e:
            print(f"Render attempt {attempt} failed: {e}", file=sys.stderr)
            if attempt < max_render_attempts:
                # Attempt to fix the script and retry
                fixed_code = fix_render_errors(final_code, str(e))
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(fixed_code)
                final_code = fixed_code
            else:
                print("ERROR: Exceeded maximum render retries", file=sys.stderr)
                sys.exit(1)


def generate_intuition(latex: str) -> str:
    """Call Gemini to explain the intuition behind the given LaTeX theorem/formula."""
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    prompt = f"""
Explain the intuition behind this theorem or formula in a way suitable for creating a visual animation.
Focus on geometric interpretations, spatial relationships, and dynamic movements.
Describe visual elements (points, lines, shapes, curves, vectors) clearly, emphasizing step-by-step visual clarity.
Return the explanation in 2–3 paragraphs.

Theorem/Formula: {latex}
"""
    response = model.generate_content(prompt)
    return response.text.strip()


def extract_code_block(text: str) -> str:
    """Extract Python code from markdown ```python ...``` fences or return raw text."""
    match = re.search(r'```python\s*(.*?)\s*```', text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


def generate_with_retry(model, prompt: str, max_retries: int = 3):
    """Generates content with retry logic on empty parts."""
    for attempt in range(max_retries):
        response = model.generate_content(prompt)
        if getattr(response, 'parts', None):
            return response
    raise RuntimeError("Failed to generate valid response after multiple attempts")


def fix_manim_imports(code: str) -> str:
    """Ensure a single wildcard import from manim at the top."""
    lines = code.strip().splitlines()
    # Remove any existing manim imports
    lines = [l for l in lines if not l.strip().startswith('from manim import')]
    return "from manim import *\n" + "\n".join(lines) + "\n"


def check_syntax_errors(code: str) -> str or None:
    """Compile code to catch syntax errors, returning error message or None."""
    try:
        compile(code, '<string>', 'exec')
        return None
    except Exception as e:
        return str(e)


def generate_manim_script(latex: str, intuition: str) -> str:
    """Use Gemini to draft and refine a Manim CE v0.18.0 script."""
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Initial generation prompt
    gen_prompt = f"""
You are writing a Manim Community Edition (v0.18.0) script to animate this theorem's intuition.

1. Import every Manim class you intend to use and print dir() for each as comments.
2. Write a Scene subclass TheoremScene with construct() using self.play() and self.add().
3. Use RGB hex colors and string-based color names.
4. Output introspection comments followed by final code in ```python fences```.

Theorem: {latex}
Intuition: {intuition}
"""
    response = generate_with_retry(model, gen_prompt)
    initial_code = extract_code_block(response.text)

    # Review & fix prompt
    review_prompt = f"""
Review and fix this Manim code for syntax, imports, and API correctness.
List dir() introspection again as comments before your fixes.
Return only the corrected code in ```python fences```.

Code to fix:
{initial_code}
"""
    reviewed = generate_with_retry(model, review_prompt)
    final_code = extract_code_block(reviewed.text)

    # Ensure correct imports
    final_code = fix_manim_imports(final_code)

    # Retry on syntax errors
    error = check_syntax_errors(final_code)
    attempts = 0
    while error and attempts < 5:
        attempts += 1
        fix_prompt = f"""
The following syntax error occurred: {error}
Please fix the code accordingly, output only corrected code in ```python fences```.```\n{final_code}```
"""
        reviewed = generate_with_retry(model, fix_prompt)
        final_code = extract_code_block(reviewed.text)
        final_code = fix_manim_imports(final_code)
        error = check_syntax_errors(final_code)

    if error:
        raise RuntimeError(f"Unresolved syntax errors after retries: {error}")
    
    return final_code


def fix_render_errors(code: str, error_msg: str) -> str:
    """Use Gemini to fix Manim script after a rendering failure."""
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = f"""
The following error occurred during Manim rendering: {error_msg}
Please fix the Manim Community Edition script so that it renders correctly.
Return only the corrected code in ```python fences```.

Original code:
```python
{code}
```"""
    response = generate_with_retry(model, prompt)
    new_code = extract_code_block(response.text)
    return fix_manim_imports(new_code)


def render_manim(script_path: str, out_dir: str) -> str:
    """Render the generated Manim script into an MP4 using the Manim CLI programmatically and return its filepath."""
    # Backup sys.argv and set new args for Manim
    original_argv = sys.argv.copy()
    sys.argv = [
        'manim', '-ql',
        '-o', out_dir,
        script_path,
        'TheoremScene'
    ]
    try:
        manim_main()
    except Exception as e:
        raise RuntimeError(f"Manim rendering failed: {e}")
    finally:
        sys.argv = original_argv

    # Build expected output path
    base = os.path.splitext(os.path.basename(script_path))[0]
    video_path = os.path.join(
        out_dir,
        'media',
        'videos',
        base,
        '480p15',
        f"{base}.mp4"
    )
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Rendered video not found at {video_path}")
    return video_path

if __name__ == '__main__':
    main()
