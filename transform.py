import os
import xml.etree.ElementTree as ET
import subprocess


def get_single_element_text(root, element_name, namespaces=None):
    items = root.findall(".//" + element_name, namespaces=namespaces)
    for item in items:
        return item.text
    return None


def process_dir(directory):

    namespace = {
        "ns": "http://pds.nasa.gov/pds4/pds/v1",
        "img": "http://pds.nasa.gov/pds4/img/v1"
    }

    for file in os.listdir(directory):
        if file.endswith(".xml") and not file.endswith(".xml.aux.xml"):
            xml_file = os.path.join(directory, file)
            png_file = "images/" + file.removesuffix(".xml") + ".tif"
            if os.path.exists(png_file):
                print("Already exists:", png_file)
                continue
            root = ET.parse(xml_file)
            start_date_time = get_single_element_text(root, "ns:start_date_time", namespaces=namespace)
            filter = get_single_element_text(root, "img:filter_name", namespaces=namespace)

            print("Transforming", file, start_date_time, filter)

            # subprocess.run(["C:\\Users\\alexs\\Downloads\\transform-1.13.2-bin\\transform-1.13.2\\bin\\transform.bat", xml_file, "-f", "png", "-o", "images"], check=True)
            # subprocess.run(["C:\\Users\\alexs\\miniconda3\\Library\\bin\\gdal_translate.exe", "-of", "GTiff", "-ot", "UInt16", "-scale", "0", "4095", "0", "65535", xml_file, png_file], check=True)
            subprocess.run(["gdal_translate", "-of", "GTiff", "-ot", "UInt16", "-scale", "0", "4095", "0", "65535", xml_file, png_file], check=True)

# EW0031520568C

# process_dir("MSGRMDS_1001/DATA/2005_212")
# process_dir("MSGRMDS_1001/DATA/2005_214")
process_dir("MSGRMDS_1001/DATA/2005_215")