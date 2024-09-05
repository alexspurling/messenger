# Since ISIS is only supported in linux, this script must be run in Linux or WSL
import math
import os
import re
import subprocess
from osgeo import gdal


def convert(img_file):
    # Convert IMG file to an ISIS cube file
    os.makedirs("isis/cub/", exist_ok=True)
    cub_file = "isis/cub/" + os.path.basename(img_file.removesuffix(".IMG")) + ".cub"
    if not os.path.exists(cub_file):
        print(f"Converting {img_file} to {cub_file}")
        subprocess.run(["mdis2isis", f"FROM={img_file}", f"TO={cub_file}"], check=True)
    return cub_file


def calibrate(cub_file):
    os.makedirs("isis/cal/", exist_ok=True)
    cal_file = "isis/cal/" + os.path.basename(cub_file)
    if not os.path.exists(cal_file):
        print(f"Calibrating {cub_file} to {cal_file}")
        subprocess.run(["mdiscal", f"FROM={cub_file}", f"TO={cal_file}", "RADIOMETRIC=FALSE"], check=True)
    return cal_file


def stats(cal_file):
    print(f"Getting stats for {cal_file}")
    result = subprocess.run(["stats", f"FROM={cal_file}"], check=True, capture_output=True, text=True)
    average = float(re.search(r" {2}Average\s*= (.*)", result.stdout).group(1))
    std_dev = float(re.search(r" {2}StandardDeviation\s*= (.*)", result.stdout).group(1))
    minimum = float(re.search(r" {2}Minimum\s*= (.*)", result.stdout).group(1))
    maximum = float(re.search(r" {2}Maximum\s*= (.*)", result.stdout).group(1))

    percentage = 99.5
    k = math.sqrt(1 / (1 - percentage / 100))
    chebyshev_min = average - k * std_dev
    chebyshev_max = average + k * std_dev
    best_min = max(minimum, chebyshev_min)
    best_max = min(maximum, chebyshev_max)
    return best_min, best_max


def process_dir(directory, start_file=None):
    rgb_files = []
    rgb_stats = []
    dir_files = os.listdir(directory)
    if start_file is not None:
        dir_files = dir_files[dir_files.index(start_file):]
    for file in dir_files:
        if file.endswith(".IMG"):
            img_file = os.path.join(directory, file)
            cub_file = convert(img_file)
            cal_file = calibrate(cub_file)
            fix_cosmic_rays(cal_file)
            img_stats = stats(cal_file)
            rgb_files.append(cal_file)
            rgb_stats.append(img_stats)
            if file.endswith("E.IMG"):
                combine_and_export(rgb_files, rgb_stats)
                rgb_files.clear()
                rgb_stats.clear()


def combine_and_export(rgb_files, rgb_stats):

    os.makedirs("isis/frames/", exist_ok=True)

    frame_num = 1
    png_image = f"isis/frames/frame{frame_num}.png"

    while os.path.exists(png_image):
        frame_num += 1
        png_image = f"isis/frames/frame{frame_num}.png"

    print("Combining", rgb_files[0], rgb_files[1], rgb_files[2], "into", png_image)
    subprocess.run(["isis2std", f"RED={rgb_files[2]}", f"GREEN={rgb_files[1]}", f"BLUE={rgb_files[0]}",
                    f"RMIN={rgb_stats[2][0]}", f"RMAX={rgb_stats[2][1]}",
                    f"GMIN={rgb_stats[1][0]}", f"GMAX={rgb_stats[1][1]}",
                    f"BMIN={rgb_stats[0][0]}", f"BMAX={rgb_stats[0][1]}",
                    "MODE=RGB", "FORMAT=PNG", f"TO={png_image}", "STRETCH=MANUAL"], check=True)


# process_dir("MSGRMDS_1001/DATA/2005_214", "EW0031509048C.IMG")
# process_dir("MSGRMDS_1001/DATA/2005_215")
process_dir("MSGRMDS_1001/DATA/2005_215", "EW0031571928C.IMG")
