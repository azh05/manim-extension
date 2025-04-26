import re

def extract_theorem(tex_file):
    with open(tex_file, 'r') as f:
        content = f.read()
    theorem_pattern = re.compile(r'\\begin{theorem}(.*?)\\end{theorem}', re.DOTALL)
    match = theorem_pattern.search(content)
    if match:
        theorem = match.group(1).strip()
        with open('inputs/theorem.txt', 'w') as f:
            f.write(theorem)
        return theorem
    else:
        raise ValueError("No theorem found in the .tex file.")

if __name__ == "__main__":
    theorem = extract_theorem("inputs/theorem.tex")
    print("Extracted Theorem:\n", theorem)