from PIL import Image, ImageDraw, ImageFont

# Constants
FONT = ImageFont.truetype("nerd_font.ttf", 10)
ASPECT_RATIO = 0.5
ASCII_CHAR_MODES = {
    "1": "@%#*+=-:. ",
    "L": "...",
    "RGB": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
}

char_width = FONT.getlength("W")     # Get the width of a single character
ascent, descent = FONT.getmetrics()  # Get the height of a character
char_height = ascent + descent


def gen_ascii(pixels, new_width, file, ascii_chars):
    """
    ...
    """
    ascii_str = ''

    for i, pixel in enumerate(pixels):
        ascii_str += ascii_chars[min(
            pixel // (255 // (len(ascii_chars) - 1)),
            len(ascii_chars) - 1)]
        if (i + 1) % new_width == 0:
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
    ascii_img_width = int(round(w * char_width))
    ascii_img_height = int(round(h * char_height))
    ascii_img = Image.new("L", (ascii_img_width, ascii_img_height), 255)
    draw = ImageDraw.Draw(ascii_img)

    x, y = 0, 0
    for char in ascii_str:
        if char == "\n":
            x = 0             # Reset X
            y += char_height  # Move to next line
        else:
            draw.text((x, y), char, fill=0, font=FONT)
            x += char_width

    file_name = f"{file_name}-ascii.png"
    ascii_img.save(file_name)
    print(f"ASCII image file saved to {file_name}.")


def main():
    """
    Function that generates ascii from input image
    --------------
    TODO:
        - Retouch image using filters to generate more quality ascii
        - Add Sequences on img gen to create ascii animation
        - Define different ASCII character sets for varying resolutions:
            - Low-resolution set for BMP (fewer characters, less detail).
            - Mid-resolution set for Grayscale images (moderate level of detail).
            - High-resolution set for RGB images (more characters, higher detail).
        - The ASCII character set selection should be based on the image mode
          of the input image.
    """

    try:
        file = input("Enter the path including filename with extension: ")
        file_name = file.rsplit(".")[0]

        image = Image.open(file)
        # Default to grayscale set if mode is not foun
        ascii_chars = ASCII_CHAR_MODES.get(image.mode, ASCII_CHAR_MODES["L"])
        gray_img = image.convert("L")

        orig_width, orig_height = gray_img.size
        new_width = int(orig_width * ASPECT_RATIO)
        # new_height = int(aspect_ratio * orig_height)
        # Squash image verticaly.
        # Adjusting the height calculation has improved the appearance
        # of ASCII art probably due to the font
        new_height = int((ASPECT_RATIO * orig_height) *
                         (new_width / orig_width))

        resized_img = gray_img.resize((new_width, new_height))
        pixels = resized_img.getdata()

        ascii_str = gen_ascii(pixels, new_width, file_name, ascii_chars)

        draw_ascii_img(new_width, new_height, file_name, ascii_str)

    except (IOError, OSError) as e:
        print("Something went wrong:", e)


if __name__ == '__main__':
    main()
