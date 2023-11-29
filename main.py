from PIL import Image, ImageDraw, ImageFont

# Constants
FONT = ImageFont.truetype("nerd_font.ttf", 10)
ASPECT_RATIO = 0.5
ASCII_CHARS = "@%#*+=-:. "  # Simplified ASCII
ASCII_CHARS_BIG = (
    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
)

char_width = FONT.getlength("W")     # Get the width of a single character
ascent, descent = FONT.getmetrics()  # Get the height of a character
char_height = ascent + descent


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

    ascii_img.save(f"{file_name}-ascii.png")


def main():
    """
    Function that generates ascii from input image
    --------------
    TODO:
        - Implement a dictionary to map image modes (BMP, RGB, Grayscale)
          to corresponding ASCII character sets.
        - Define different ASCII character sets for varying resolutions:
            - Low-resolution set for BMP (fewer characters, less detail).
            - Mid-resolution set for Grayscale images (moderate level of detail).
            - High-resolution set for RGB images (more characters, higher detail).
        - The ASCII character set selection should be based on the image mode
          of the input image.
    """
    try:
        file = input("Enter the path including filename with extension: ")
        image = Image.open(file)
        gray_img = image.convert("L")

        orig_width, orig_height = gray_img.size
        # aspect_ratio = ASPECT_RATIO
        new_width = int(orig_width * ASPECT_RATIO)
        # new_height = int(aspect_ratio * orig_height)
        # Squash image verticaly.
        # Adjusting the height calculation has improved the appearance
        # of ASCII art probably due to the font
        new_height = int((ASPECT_RATIO * orig_height) *
                         (new_width / orig_width))

        ascii_str = ''
        resized_img = gray_img.resize((new_width, new_height))
        pixels = resized_img.getdata()
        for i, pixel in enumerate(pixels):
            ascii_str += ASCII_CHARS_BIG[min(
                pixel // (255 // (len(ASCII_CHARS_BIG) - 1)),
                len(ASCII_CHARS_BIG) - 1)]
            if (i + 1) % new_width == 0:
                ascii_str += '\n'

        file_name = file.rsplit(".")[0]
        txt_file = f"{file_name}-ascii.txt"
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(ascii_str)

        draw_ascii_img(new_width, new_height, file_name, ascii_str)

        print(f"ASCII art saved to {txt_file}.")

    except (IOError, OSError) as e:
        print("Something went wrong:", e)


if __name__ == '__main__':
    main()
