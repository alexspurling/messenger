
# For a tutorial on how to install this library see https://www.youtube.com/watch?v=8iCWUp7WaTk Unfortunately the
# original maintainer of that wheel archive took their website down but it's still available from archive.org I
# downloaded GDAL-3.4.3-cp310-cp310-win_amd64.whl from
# https://web.archive.org/web/20230601133709if_/https://download.lfd.uci.edu/pythonlibs/archived/GDAL-3.4.3-cp310
# -cp310-win_amd64.whl Then in my venv ran `pip install GDAL-3.4.3-cp310-cp310-win_amd64.whl`

from osgeo import gdal
import os
import numpy as np


def getminmax(image):
    ds = gdal.Open(image)
    myarray = np.array(ds.GetRasterBand(1).ReadAsArray())
    info = gdal.Info(image, options=gdal.InfoOptions(computeMinMax=True, format="json", reportHistograms=True))
    return info["bands"][0]["min"], info["bands"][0]["max"]


def translate(image):
    png_file = "images/" + image.removesuffix(".xml") + ".png"
    if os.path.exists(png_file):
        print("Already exists:", png_file)
        return
    min, max = getminmax(image)
    print(f"Translating {image} with min {min}, max {max} to {png_file}")
    gdal.Translate(png_file, image, options=gdal.TranslateOptions(format="PNG", outputType="UInt16",
                                                                  scaleParams=[min, max, 0, 65535]))


def process_dir(directory):
    for file in os.listdir(directory):
        if file.endswith(".xml") and not file.endswith(".xml.aux.xml"):
            xml_file = os.path.join(directory, file)
            translate(xml_file)


# minmax = getminmax("MSGRMDS_1001\\DATA\\2005_215\\EW0031520568C.xml")
# print("info", minmax)


process_dir("MSGRMDS_1001/DATA/2005_214")
process_dir("MSGRMDS_1001/DATA/2005_215")
