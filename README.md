## MESSENGER Earth View Timeplase

![image](EarthMessenger.gif)

I wrote this set of python scripts to download and then process the raw image data to produce this timelapse of NASA's MESSENGER's spacecraft as it flew by Earth on its way to Mercury.

I wanted to do this because the original video produced by NASA back in 2005 was heavily compressed and of very low quality. Today's video compression codecs are much more efficient resulting in the high quality version you see above.

## Challenges

Every frame is made up of three separate greyscale photos taken filtered at different wavelengths. Each image also had a different exposure time which means the brightness of each frame has to be normalised in order to produce an RGB frame with the correct colour.

```python
    # Load grayscale images
    img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)
    img3 = cv2.imread(image3, cv2.IMREAD_GRAYSCALE)

    # Check if images have the same dimensions
    if img1.shape != img2.shape or img1.shape != img3.shape:
        raise ValueError("All images must have the same dimensions")

    # Normalize images to range [0, 255]
    img1 = cv2.normalize(img1, None, 0, 255, cv2.NORM_MINMAX)
    img2 = cv2.normalize(img2, None, 0, 255, cv2.NORM_MINMAX)
    img3 = cv2.normalize(img3, None, 0, 255, cv2.NORM_MINMAX)

    # Adjust images 2 and 3 to match the histogram of image1
    img2 = exposure.match_histograms(img2, img1)
    img3 = exposure.match_histograms(img3, img1)
```

Next, I had to normalise the brightness from one frame to the next. I did this by measuring the average brightness of all non-black pixels and using an iterative algorithm to adjust the gamma of each frame to match a given target:

```python

def adjust_gamma_to_target(image, target):
    margin = 1
    non_black_avg = calculate_average_non_black_pixels(image)
    # Iterate until we reach the target brightness
    while abs(non_black_avg - target) > margin:
        adjust = 1 - ((non_black_avg - target) / 250)
        if non_black_avg < target:
            image = exposure.adjust_gamma(image, gamma=adjust)
        else:
            image = exposure.adjust_gamma(image, gamma=adjust)
        non_black_avg = calculate_average_non_black_pixels(image)
    return image


def calculate_average_non_black_pixels(image):
    flattened_image = image.flatten()
    sum = 0
    count = 0
    for p in flattened_image:
        if p > 25:
            sum += p
            count += 1
    if count > 0:
        return sum / count
    return 0
```