from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import requests
import time
import shutil
from PIL import Image

def FindImages(url):
    '''
    Find Image URLS
    '''
    html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    tiles = soup.find_all("div", class_="tile")

    for t in tiles:
        painting = t.find("img")
        image_link = painting.get("src")
        image_name = painting.get("alt")

        try:
            filename = 'paintings/' + image_link.strip().split('/')[-1].strip().split("?")[0]
            src = BASE_URL + image_link
            response = requests.get(src, stream=True)
            # delay to avoid corrupted previews
            time.sleep(1)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        except:
            print('Error occured with', image_name)

    print("Added", str(len(tiles)), "images")

if __name__ == '__main__':
    BASE_URL = 'https://www.frida-kahlo-foundation.org'
    URLS = [ BASE_URL + "/the-complete-works.html?pageno=" + str(n) for n in range(1, 10) ]

    for url in URLS:
        FindImages(url)
    print("DONE")
