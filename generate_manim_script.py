import google.generativeai as genai
import os
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_code_block(text):
    """Extracts Python code from markdown code blocks."""
    match = re.search(r'```python\s*(.*?)\s*```', text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

def generate_with_retry(model, prompt, max_retries=3):
    """Generates content with error checking and retries."""
    for _ in range(max_retries):
        print("Trying")
        response = model.generate_content(prompt)
        if response.parts:
            return response
    raise RuntimeError("Failed to generate valid response after multiple attempts")

def fix_manim_imports(code: str) -> str:
    """Removes any existing 'from manim import ...' and adds 'from manim import *' at the top."""
    lines = code.strip().splitlines()
    # Remove existing 'from manim import' lines
    lines = [line for line in lines if not line.strip().startswith("from manim import")]
    # Prepend correct import
    fixed_code = ["from manim import *"] + lines
    return "\n".join(fixed_code)

def generate_manim_script():
    with open('inputs/theorem.txt', 'r') as f:
        theorem = f.read()
    with open('inputs/intuition.txt', 'r') as f:
        intuition = f.read()
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    # 1) Generation prompt
    gen_prompt = f"""
    You’re writing a Manim Community Edition (v0.18.0) script to animate this theorem’s intuition. 
    Follow these strict guidelines:

    1. **Introspection**  
       Before emitting any animation code, import EVERY Manim class you intend to use (Scene, Circle, Polygon, etc.)  
       and then print out `dir(…)` for each to LIST their available methods and attributes.  
       Only after confirming those names exist, proceed to write your final script.

    2. **Manim code style**  
       • Use proper Manim syntax (CE v0.18.0)  
       • Include all necessary imports  
       • Inherit from `Scene` and name your class `TheoremScene`  
       • Sequence animations with `self.play()`  
       • Add objects to the scene with `self.add()` or via animations  
       • Use RGB hex colors and are strings types 

    3. **Output format**  
       First, show the introspection blocks (the `dir()` outputs) as comments.  
       Then return **only** the final, cleaned Python code within ```python fences``` using this template:

       ```python
       from manim import *
       import numpy as np

       class TheoremScene(Scene):
           def construct(self):
               # … your verified code …
       ```

    Theorem: {theorem}
    Intuition: {intuition}
    """
    response = generate_with_retry(model, gen_prompt)
    initial_code = extract_code_block(response.text)

    # 2) Review prompt
    review_prompt = f"""
    Review and fix this Manim code. **But before** changing anything, re-import each class you’re using  
    and once again list their available methods/attributes to CONFIRM that every call in the code is valid.  
    If a method isn’t present, replace it with the correct one from the Manim v0.18.0 API.  

    Check for:  
    - Syntax errors  
    - Missing imports  
    - Incorrect object construction (e.g. `Triangle.__init__()` takes 1 positional argument, but 4 were given)
    - Incorrect method usage (e.g. `Polygon` has no `.angle` attribute)  
    - Objects not added to the scene  
    - Animation sequencing issues  
    - Deprecated features  
        - For example, ShowCreation has been replaced by Create
    - `class TheoremScene(Scene):` is in the program
    - Constants like UP, DOWN, LEFT, RIGHT, IN, OUT, and DEGREES are imported
    - Correct method calls on numpy ndarrays

    **Output**: only the corrected Python code within ```python``` markers,  
    preceded (as comments) by your new introspection snippets.
    
    Code to fix:
    {initial_code}
    """
    reviewed_response = generate_with_retry(model, review_prompt)
    final_code = extract_code_block(reviewed_response.text)

    # Validate basic structure
    if "class TheoremScene(Scene):" not in final_code:
        print(final_code)
        raise ValueError("Generated code is missing required class structure")

    # Fix imports
    final_code = fix_manim_imports(final_code)

    with open('theorem_animation.py', 'w') as f:
        f.write(final_code)

    return final_code

if __name__ == "__main__":
    generated_code = generate_manim_script()
    print("Manim script generated and validated successfully!")
