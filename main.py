from sys import argv
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# Constants
FONT = ImageFont.truetype("nerd_font.ttf", 10)
CHAR_WIDTH = FONT.getlength("W")     # Get the width of a single character
ascent, descent = FONT.getmetrics()  # Get the height of a character
CHAR_HEIGHT = ascent + descent
ASPECT_RATIO = 0.5
FONT_ASPECT_RATIO = CHAR_WIDTH / CHAR_HEIGHT
ASCII_CHAR_MODES = {
    "1": "@%#*+=-:. ",  # Bitmap
    "L": None,          # Grayscale
    "RGB": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
}
ASCII_CHAR_MODES["L"] = ASCII_CHAR_MODES["RGB"]


def evaulate_img(img):
    """
    Image analysis. Evaulating if image is
    'overexposed' or 'underexposed'
    """
    histogram_np = np.array(img.histogram())
    intensity_np = np.arange(len(histogram_np))
    # Weighted avg
    average = np.sum(histogram_np * intensity_np) // np.sum(histogram_np)

    if average < 60:  # Underexposed
        # Apply 'normalize' filters
        modified_img = img
    elif average > 190:  # Overexposed
        # Apply 'normalize' filters
        modified_img = img
    else:
        # Default filters
        # No Chain of fools possible in Pillow?
        modified_img = img.filter(ImageFilter.DETAIL)
        modified_img = modified_img.filter(ImageFilter.SHARPEN)

    return modified_img


def gen_ascii(pixels, w, file, ascii_chars):
    """
    ...
    """
    ascii_str = ''

    for i, pixel in enumerate(pixels):
        ascii_str += ascii_chars[min(
            pixel // (255 // (len(ascii_chars) - 1)),
            len(ascii_chars) - 1)]
        if (i + 1) % w == 0:
            ascii_str += '\n'

    txt_file = f"{file}-ascii.txt"
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(ascii_str)
    print(f"ASCII text file saved to {txt_file}.")

    return ascii_str


def draw_ascii_img(w, h, file_name, ascii_str):
    """
    Draw and save ASCII image
    """
    ascii_img_width = int(round(w * CHAR_WIDTH))
    ascii_img_height = int(round(h * CHAR_HEIGHT))
    ascii_img = Image.new("L", (ascii_img_width, ascii_img_height), 255)
    draw = ImageDraw.Draw(ascii_img)

    x, y = 0, 0
    for char in ascii_str:
        if char == "\n":
            x = 0             # Reset X
            y += CHAR_HEIGHT  # Move to next line
        else:
            draw.text((x, y), char, fill=0, font=FONT)
            x += CHAR_WIDTH

    file_name = f"{file_name}-ascii.png"
    ascii_img.save(file_name)
    print(f"ASCII image file saved to {file_name}.")


def main():
    """
    Function that generates ascii from input image
    ----------------------------------------------------------------
    TODO:
        - Add Sequences on img gen to create ascii animation (ascii image)
        - Test with Numpy for better performace and for image analysis
        - Introduce palette for RGB/color images to get better results
    """

    try:
        file_input = argv[1:]
        file = None
        if not file_input:
            print("Please provide a filename with path as an argument")
            exit()
        elif len(file_input) > 1:
            print("Please provide single file including the path to the file")
            exit()
        else:
            file = file_input[0]

        file_name = file.split(".", maxsplit=1)[0]
        image = Image.open(file)
        # Default to grayscale set if mode is not found
        ascii_chars = ASCII_CHAR_MODES.get(image.mode, ASCII_CHAR_MODES["L"])
        gray_img = image.convert("L")

        orig_width, orig_height = gray_img.size
        # Font thingy
        new_height = int(orig_height * FONT_ASPECT_RATIO)

        new_width = int(orig_width * ASPECT_RATIO)
        new_height = int(new_height * ASPECT_RATIO)
        # Resize the image
        resized_img = gray_img.resize((new_width, new_height))

        modified_img = evaulate_img(resized_img)

        pixels = modified_img.getdata()

        ascii_str = gen_ascii(pixels, new_width, file_name, ascii_chars)
        draw_ascii_img(new_width, new_height, file_name, ascii_str)

    except (IOError, OSError) as e:
        print("Something went wrong:", e)


if __name__ == '__main__':
    main()
