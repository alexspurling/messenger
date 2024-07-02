import requests
import xml.etree.ElementTree as ET
import os.path


cloudfront_url = "https://d3fhgbbgskqro0.cloudfront.net/"


def urls_in_directory(directory):

    rep = requests.get(directory + "&max-keys=1000&marker=MSGRMDS_1001%2FDATA%2F2005_215%2FEW0031594488C.xml")

    namespace = {'ns': 'http://s3.amazonaws.com/doc/2006-03-01/'}

    urls = []

    if rep.status_code == 200:
        print(rep.text)
        root = ET.fromstring(rep.text)
        for item in root.findall("ns:Contents", namespaces=namespace):
            key = item.find("ns:Key", namespace)
            print(key.text)
            urls.append(cloudfront_url + key.text)

        # print("Directory:", rep.text)
        return urls
    else:
        print("Error getting directory", rep.status_code, rep.text)
        return []


def download_urls(urls):
    for url in urls:
        rep = requests.get(url)
        if rep.status_code == 200:
            filepath = url.removeprefix(cloudfront_url)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(rep.content)
            print("Wrote", filepath)


# download_urls(urls_in_directory("https://d3fhgbbgskqro0.cloudfront.net/?delimiter=/&prefix=MSGRMDS_1001/DATA/2005_212/"))
# download_urls(urls_in_directory("https://d3fhgbbgskqro0.cloudfront.net/?delimiter=/&prefix=MSGRMDS_1001/DATA/2005_214/"))
download_urls(urls_in_directory("https://d3fhgbbgskqro0.cloudfront.net/?delimiter=/&prefix=MSGRMDS_1001/DATA/2005_215/"))

