from sys import argv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, \
    ImageOps, ImageEnhance
import numpy as np
from ascii_statistics import gen_img_statistic

# Constants
FONT = ImageFont.truetype("nerd_font.ttf", 10)
CHAR_WIDTH = FONT.getlength("W")     # Get the width of a single character
ascent, descent = FONT.getmetrics()  # Get the height of a character
CHAR_HEIGHT = ascent + descent
ASPECT_RATIO = 0.5
FONT_ASPECT_RATIO = CHAR_WIDTH / CHAR_HEIGHT
ASCII_CHAR_MODES = {
    "1": "@%#*+=-:. ",
    "L": (
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
    ),
    "RGB": (
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
    )
}


def evaulate_img(img):
    """
    Image analysis. Evaulating if image is
    'overexposed' or 'underexposed'
    """
    histogram_np = np.array(img.histogram())
    intensity_np = np.arange(len(histogram_np))
    # Weighted avg
    average = np.sum(histogram_np * intensity_np) // np.sum(histogram_np)

    modified_img = ImageOps.autocontrast(img)

    # Underexposed < 60; Overexposed > 190
    # Attempt to 'normalize' image
    if average < 60:
        print("Image is underexposed")
        enh = ImageEnhance.Brightness(modified_img)
        modified_img = enh.enhance(4.0)
    elif average > 190:
        print("Image is overexposed")
        enh = ImageEnhance.Brightness(modified_img)
        modified_img = enh.enhance(0.7)
    else:
        # Nice, chain of fools is possible
        modified_img = (
            modified_img
            .filter(ImageFilter.DETAIL)
            .filter(ImageFilter.SHARPEN)
        )
        enh = ImageEnhance.Brightness(modified_img)
        modified_img = enh.enhance(1.4)

    enh = ImageEnhance.Contrast(modified_img)
    modified_img = enh.enhance(1.8)

    return modified_img


def ascii_version_path(file_input, ext):
    file_path = Path(file_input)
    file_basename = f"{file_path.stem}-ascii.{ext}"

    return f"{file_path.parent}/{file_basename}"


def gen_ascii(pixels, w, file, ascii_chars):
    """
    ::::;,,;^;,,,,,,,,,,,,,,,,,,,,,`^^^^^^^^^^^^^^^^,````````````````````:,I
    .........;]-[l+<-.~,<i;]_}zY-)\_!..'......^I.:......;I^^.`^'''''''''''''
    """
    ascii_str = ""

    for i, pixel in enumerate(pixels):
        ascii_str += ascii_chars[min(
            pixel // (255 // (len(ascii_chars) - 1)),
            len(ascii_chars) - 1)]
        if (i + 1) % w == 0:
            ascii_str += "\n"

    text_file = ascii_version_path(file, "txt")

    with open(text_file, "w", encoding="utf-8") as f:
        f.write(ascii_str)
    print(f"ASCII text file saved to {text_file}")

    return ascii_str


def draw_ascii_img(w, h, file, ascii_str):
    """
    Draw and save ASCII image
    """
    ascii_img_width = int(round(w * CHAR_WIDTH))
    ascii_img_height = int(round(h * CHAR_HEIGHT))
    ascii_img = Image.new("L", (ascii_img_width, ascii_img_height), 255)
    draw = ImageDraw.Draw(ascii_img)

    lines = ascii_str.split("\n")

    y = 0
    for line in lines:
        draw.text((0, y), line, fill=0, font=FONT)
        y += CHAR_HEIGHT

    img_file = ascii_version_path(file, "png")

    ascii_img.show()
    ascii_img.save(img_file)
    print(f"ASCII image file saved to {img_file}")

    return ascii_img


def main():
    """
    Function that generates ascii from input image
    """

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

    image = Image.open(file)
    # Default to grayscale set if mode is not found
    ascii_chars = ASCII_CHAR_MODES.get(image.mode, ASCII_CHAR_MODES["L"])
    gray_img = image.convert("L")

    orig_width, orig_height = gray_img.size
    # Font thingy
    new_height = int(orig_height * FONT_ASPECT_RATIO)

    new_width = int(orig_width * ASPECT_RATIO)
    new_height = int(new_height * ASPECT_RATIO)
    resized_img = gray_img.resize((new_width, new_height))

    modified_img = evaulate_img(resized_img)

    pixels = modified_img.getdata()

    ascii_str = gen_ascii(pixels, new_width, file, ascii_chars)
    ascii_img = draw_ascii_img(new_width, new_height, file, ascii_str)
    gen_img_statistic(resized_img, ascii_img)


if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print(e)
