import os
from PIL import Image

def display_image():
    image_path = "media/videos/theorem_animation/480p15/theorem_animation.png"  # Or .mp4
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img.show()
    else:
        print("Render the animation first!")

if __name__ == "__main__":
    display_image()