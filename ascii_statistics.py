import io
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def gen_img_statistic(original_image, ascii_img):
    MARGIN = 30
    # Draw text with copy
    ascii_img_c = ascii_img.crop(
        (0, 0, ascii_img.width // 2, ascii_img.height))
    font = ImageFont.truetype("nerd_font.ttf", 30)
    draw = ImageDraw.Draw(ascii_img_c)
    txt = "Hide the pain Harold"
    # Get the bounding box of the text i.e. (0, 4, 324, 29)
    _, _, bbx, bby = draw.textbbox((0, 0), txt, font=font)
    draw.rectangle(
        [(MARGIN, MARGIN),
         ((MARGIN + bbx), (MARGIN + bby))], fill=255)
    draw.text((MARGIN, MARGIN), txt, font=font, fill=0)

    # Graphs
    # 1/4 of the original width and height.
    # Matplotlib is using inches as units
    new_width = (ascii_img_c.width - MARGIN * 2) // 96
    new_height = (ascii_img_c.height // 4 - MARGIN) // 96

    orig_img_hist = original_image.histogram()
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(new_width, new_height))

    # 1st Histogram
    ax1.bar(range(len(orig_img_hist)), orig_img_hist, width=1.4, color="black")
    ax1.set_title('Image Histogram')
    ax1.set_xlabel('Pixel Value')
    ax1.set_ylabel('Frequency')

    # 2nd Histogram
    data_normalized = (orig_img_hist - np.mean(orig_img_hist)
                       ) / np.std(orig_img_hist)

    # Generate circular data
    theta = np.linspace(0, 2 * np.pi, len(orig_img_hist))
    x = data_normalized * np.cos(theta)
    y = data_normalized * np.sin(theta)

    ax2.scatter(x, y, s=0.8, c="black")
    ax2.set_title("Circular Scatter Plot of Normalized Data")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    chart_img = Image.open(buf)
    ascii_img_c.paste(chart_img, (MARGIN, 70), chart_img)
    ascii_img_c.show()
