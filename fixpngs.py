import os
import png


total_pixels_changed = 0


def remove_noise(png_file):
    global total_pixels_changed
    r = png.Reader(png_file)
    width, height, pixels_iter, metadata = r.read()

    print("metadata:", metadata)

    threshold = 150

    pixels = list(pixels_iter)

    for row in pixels:
        for x in range(0, len(row), 4):
            red_value = row[x]
            green_value = row[x + 1]
            blue_value = row[x + 2]
            alpha_value = row[x + 3]

            avg_green_blue = (green_value + blue_value) / 2
            avg_red_blue = (red_value + blue_value) / 2
            avg_red_green = (red_value + green_value) / 2

            if red_value - avg_green_blue > threshold:
                row[x] = int(avg_green_blue)
                print(f"Changed red pixel from {red_value} to {avg_green_blue}")
                total_pixels_changed += 1
            if green_value - avg_red_blue > threshold:
                row[x + 1] = int(avg_red_blue)
                print(f"Changed green pixel from {green_value} to {avg_red_blue}")
                total_pixels_changed += 1
            if blue_value - avg_red_green > threshold:
                row[x + 2] = int(avg_red_green)
                print(f"Changed blue pixel from {blue_value} to {avg_red_green}")
                total_pixels_changed += 1

    output_file = "frames/" + os.path.basename(png_file)
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


for file in os.listdir("frames_noise"):
    remove_noise("frames_noise/" + file)

print(f"Fixed {total_pixels_changed} pixels")