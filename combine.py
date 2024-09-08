import os
import cv2
import numpy as np
# from skimage import exposure
import math
import xml.etree.ElementTree as ET

def calculate_median_brightness(image):
    return np.median(image)


def adjust_brightness(image, target_brightness):
    current_brightness = calculate_trimmed_mean_brightness(image)
    brightness_ratio = target_brightness / current_brightness
    return cv2.convertScaleAbs(image, alpha=brightness_ratio, beta=0)


def calculate_trimmed_mean_brightness(image, trim_percentage=0.10):
    flattened_image = image.flatten()
    sorted_pixels = np.sort(flattened_image)
    trim_count = int(trim_percentage * len(sorted_pixels))
    trimmed_pixels = sorted_pixels[trim_count:-trim_count]
    return np.mean(trimmed_pixels)


# def adjust_gamma_to_target(image, target):
#     margin = 1
#     non_black_avg = calculate_average_non_black_pixels(image)
#     while abs(non_black_avg - target) > margin:
#         adjust = 1 - ((non_black_avg - target) / 250)
#         if non_black_avg < target:
#             image = exposure.adjust_gamma(image, gamma=adjust)
#         else:
#             image = exposure.adjust_gamma(image, gamma=adjust)
#         non_black_avg = calculate_average_non_black_pixels(image)
#     return image


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


brightnesses = []
brightnesses2 = []


# def combine(frame_num, image1, image2, image3, output_image):
#
#     # Load grayscale images
#     img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
#     img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)
#     img3 = cv2.imread(image3, cv2.IMREAD_GRAYSCALE)
#
#     # Check if images have the same dimensions
#     if img1.shape != img2.shape or img1.shape != img3.shape:
#         raise ValueError("All images must have the same dimensions")
#
#     # Normalize images to range [0, 255]
#     img1 = cv2.normalize(img1, None, 0, 255, cv2.NORM_MINMAX)
#     img2 = cv2.normalize(img2, None, 0, 255, cv2.NORM_MINMAX)
#     img3 = cv2.normalize(img3, None, 0, 255, cv2.NORM_MINMAX)
#
#     # brightness_values = [calculate_trimmed_mean_brightness(img) for img in [img1, img2, img3]]
#     # target_brightness = np.mean(brightness_values)
#     #
#     # img1, img2, img3 = [adjust_brightness(img, target_brightness) for img in [img1, img2, img3]]
#
#     # print(f"Adjusted brightnesses from {brightness_values} to {[calculate_trimmed_mean_brightness(img) for img in [img1, img2, img3]]} (target: {target_brightness})")
#
#     img1 = img1.astype(np.float64)
#     img2 = img2.astype(np.float64)
#     img3 = img3.astype(np.float64)
#     img2 = exposure.match_histograms(img2, img1)
#     img3 = exposure.match_histograms(img3, img1)
#
#     # img1 = exposure.adjust_gamma(img1, gamma=1.02)
#
#     # Stack images into an RGB image
#     rgb_image = cv2.merge((img1, img2, img3))
#     #
#     # if frame_num == 76:
#     #     rgb_image = exposure.adjust_gamma(rgb_image, gamma=1.08)
#     # if frame_num == 104:
#     #     rgb_image = exposure.adjust_gamma(rgb_image, gamma=1.03)
#     # if frame_num == 129:
#     #     rgb_image = exposure.adjust_gamma(rgb_image, gamma=0.95)
#     # if frame_num == 132:
#     #     rgb_image = exposure.adjust_gamma(rgb_image, gamma=1.02)
#     # if frame_num == 175:
#     #     rgb_image = exposure.adjust_gamma(rgb_image, gamma=1.03)
#     # if frame_num == 178:
#     #     rgb_image = exposure.adjust_gamma(rgb_image, gamma=1.03)
#
#     rgb_image = adjust_gamma_to_target(rgb_image, 80)
#
#     # if frame_num == 19:
#     #     rgb_image = exposure.adjust_gamma(rgb_image, gamma=0.99)
#
#     # brightness = calculate_trimmed_mean_brightness(rgb_image, trim_percentage=0.1)
#     # brightness = np.mean(rgb_image)
#     # non_black_avg = calculate_average_non_black_pixels(rgb_image)
#     # brightnesses.append(brightness)
#     # brightnesses2.append(non_black_avg)
#
#     # font = cv2.FONT_HERSHEY_SIMPLEX
#     # org = (50, 50)
#     # font_scale = 0.75
#     # # Blue color in BGR
#     # color = (255, 0, 0)
#     # thickness = 2
#
#     # rgb_image = cv2.putText(rgb_image, f"Brightness: {brightness}", (20, 20), font,
#     #                         font_scale, color, thickness, cv2.LINE_AA)
#     # rgb_image = cv2.putText(rgb_image, f"Non black avg: {non_black_avg}", (20, 50), font,
#     #                         font_scale, color, thickness, cv2.LINE_AA)
#     #
#     # x = 0
#     # for b in brightnesses2:
#     #     logb = math.log(b)
#     #     rgb_image = cv2.line(rgb_image, (x, int(512 - (logb * 50))), (x, 512), (0, 200, 200), 1)
#     #     x += 1
#     # x = 0
#     # for b in brightnesses:
#     #     logb = math.log(b)
#     #     rgb_image = cv2.line(rgb_image, (x, int(512 - (logb * 50))), (x, 512), (0, 0, 200), 1)
#     #     x += 1
#
# # Save or display the RGB image
#     cv2.imwrite(output_image, rgb_image)
#     # cv2.imshow('RGB Image', rgb_image)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#
#     return brightnesses


# def generate_frames(start_image):
#
#     all_images = os.listdir("images")
#
#     red_image_idx = all_images.index(start_image)
#     green_image_idx = red_image_idx + 1
#     blue_image_idx = red_image_idx + 2
#
#     frame_num = 0
#
#     while red_image_idx < len(all_images):
#
#         red_image = "images/" + all_images[red_image_idx]
#         green_image = "images/" + all_images[green_image_idx]
#         blue_image = "images/" + all_images[blue_image_idx]
#
#         frame_num += 1
#         output_image = f"frames/frame{frame_num}.png"
#
#         # if os.path.exists(output_image):
#         #     print("Already exists", red_image, green_image, blue_image, ":", output_image)
#         # else:
#         print("Combining", red_image, green_image, blue_image, "into", output_image)
#         combine(frame_num, red_image, green_image, blue_image, output_image)
#
#         red_image_idx += 3
#         green_image_idx += 3
#         blue_image_idx += 3


# start_image = "EW0031509048C.png"
# generate_frames("EW0031509048C.tif")

def get_exposure(xml_file):
    namespaces = {"img": "http://pds.nasa.gov/pds4/img/v1"}
    root = ET.parse(xml_file)
    return float(root.findall(".//img:exposure_duration", namespaces=namespaces)[0].text)


def adjust_exposure(image, actual_exposure_time, target_exposure_time):
    exposure_ratio = target_exposure_time / actual_exposure_time
    adjusted_image = cv2.convertScaleAbs(image, alpha=exposure_ratio, beta=0)
    return adjusted_image


def combine2(frame_num, image1, image1exposure, image2, image2exposure, image3, image3exposure, output_image):

    # Load grayscale images
    img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)
    img3 = cv2.imread(image3, cv2.IMREAD_GRAYSCALE)

    # img1 = adjust_exposure(img1, image1exposure, 40)
    # img2 = adjust_exposure(img2, image2exposure, 40)
    # img3 = adjust_exposure(img3, image3exposure, 40)

    # if frame_num == 19:
    #     cv2.imshow('Adjusted image', img1)
    #     cv2.waitKey(0)

    # cv2.imwrite(output_image.removesuffix(".png") + "_r.png", img1)
    # cv2.imwrite(output_image.removesuffix(".png") + "_g.png", img2)
    # cv2.imwrite(output_image.removesuffix(".png") + "_b.png", img3)

    rgb_image = cv2.merge((img1, img2, img3))
    cv2.imwrite(output_image, rgb_image)


def generate_frames2(start_image):

    all_images = sorted(os.listdir("images"))

    red_image_idx = all_images.index(start_image)
    green_image_idx = red_image_idx + 1
    blue_image_idx = red_image_idx + 2

    frame_num = 0

    while red_image_idx < len(all_images):

        red_image = "images/" + all_images[red_image_idx]
        green_image = "images/" + all_images[green_image_idx]
        blue_image = "images/" + all_images[blue_image_idx]

        frame_num += 1
        output_image = f"frames_combine/frame{frame_num:03}.png"

        red_xml = "MSGRMDS_1001/DATA/2005_215/" + all_images[red_image_idx].removesuffix(".tif") + ".xml"
        green_xml = "MSGRMDS_1001/DATA/2005_215/" + all_images[green_image_idx].removesuffix(".tif") + ".xml"
        blue_xml = "MSGRMDS_1001/DATA/2005_215/" + all_images[blue_image_idx].removesuffix(".tif") + ".xml"

        red_exposure = get_exposure(red_xml)
        green_exposure = get_exposure(green_xml)
        blue_exposure = get_exposure(blue_xml)

        # if os.path.exists(output_image):
        #     print("Already exists", red_image, green_image, blue_image, ":", output_image)
        # else:
        print(f"Combining {red_image} {red_exposure}, {green_image} {green_exposure}, {blue_image} {blue_exposure} into {output_image}")
        combine2(frame_num, red_image, red_exposure, green_image, green_exposure, blue_image, blue_exposure, output_image)

        red_image_idx += 3
        green_image_idx += 3
        blue_image_idx += 3


# generate_frames2("EW0031509048C.tif")
generate_frames2("EW0031514568C.tif")

# combine("EW0031520568C.png", "EW0031520571D.png", "EW0031520574E.png", "frame49.png")
# combine("EW0031520808C.png", "EW0031520811D.png", "EW0031520814E.png", "frame50.png")
# combine("EW0031520808C_gdal.png", "EW0031520811D_gdal.png", "EW0031520814E_gdal.png", "frame50_gdal.png")
