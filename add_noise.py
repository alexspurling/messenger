import os
import random
import png

total_pixels_changed = 0


def add_noise(png_file):
    global total_pixels_changed
    r = png.Reader(png_file)
    width, height, pixels_iter, metadata = r.read()

    pixels = list(pixels_iter)

    row_length = metadata['planes'] * width

    num_pixels = random.randint(0, 100)

    x_values = random.sample(range(0, row_length), num_pixels)
    y_values = random.sample(range(0, height), num_pixels)

    for p in range(0, num_pixels):
        x = x_values[p]
        y = y_values[p]
        if x % 4 != 3:
            noise_value = random.randint(200, 255)
            print(f"Updated ({x},{y}) from {pixels[y][x]} to {noise_value}")
            pixels[y][x] = noise_value
            total_pixels_changed += 1

    print("metadata:", metadata)

    output_file = "frames_noise/" + os.path.basename(png_file)
    with open(output_file, "wb") as f:
        writer = png.Writer(width, height,
                            size=metadata['size'],
                            greyscale=metadata['greyscale'],
                            alpha=metadata['alpha'],
                            bitdepth=metadata['bitdepth'],
                            interlace=metadata['interlace'],
                            planes=metadata['planes'])
        wrote = writer.write(f, pixels)
        print(f"Wrote {wrote} lines to {output_file}")


for file in os.listdir("frames_orig"):
    add_noise("frames_orig/" + file)

print(f"Changed {total_pixels_changed} pixels")

# changed 13135 RGB pixels
