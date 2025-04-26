import subprocess

def render_manim():
    command = "manim -ql -o theorem_animation theorem_animation.py TheoremScene"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    render_manim()
    print("Rendered animation at media/videos/theorem_animation/480p15/theorem_animation.mp4")