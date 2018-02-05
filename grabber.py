__author__ = 'matthias'

# A very little script to download the pic of the day from nasa and set it as background

import os
from datetime import date
import urllib.request
import ssl
import shutil
import subprocess
import lxml.html


def set_background(image_path):
    # Nasty hack because xfce on my xubuntu 14.04 only applies background changes for the active workspace,
    # but it will affect all workspaces.
    for mon in ['monitoreDP1', 'monitorDP2']:
        for idx in range(5):
            cmd = ["xfconf-query",
                   "-c", "xfce4-desktop",
                   "-p", "/backdrop/screen0/{}/workspace{}/last-image".format(mon,idx),
                   "-s", image_path]
            subprocess.Popen(cmd)


def get_background(path_to_store):
    ctx = ssl._create_unverified_context()

    today = date.today().strftime("%m%d%Y")
    image_name = "image{}_500m.jpg".format(today)
    base_url = "http://modis.gsfc.nasa.gov/gallery/images/"
    image_url = base_url + image_name

    image_path = path_to_store + image_name

    if not os.path.isfile(image_path):
        with urllib.request.urlopen(image_url, context=ctx) as response, \
                open(image_path, 'wb') as out_file:

            shutil.copyfileobj(response, out_file)
            try:
                os.remove(path_to_store + 'current.jpg')
            except FileNotFoundError:
                pass
            os.symlink(image_path, path_to_store + 'current.jpg')
            print(image_path)

        os.system('notify-send -u critical "New MODIS Image"')


def get_description(path_to_store):
    ctx = ssl._create_unverified_context()
    today = date.today().strftime("%Y-%m-%d")

    page = urllib.request.urlopen("https://modis.gsfc.nasa.gov/gallery/individual.php?db_date={}".format(today),
                                  context=ctx)
    tree = lxml.html.fromstring(page.read())

    header = tree.xpath("/html/body/div/div/div[2]/div[2]/div[2]/h5/b/text()")[0].strip()
    div1 = tree.xpath("/html/body/div/div/div[2]/div[2]/div[2]/p[4]/text()")[0].strip()
    div2 = tree.xpath("/html/body/div/div/div[2]/div[2]/div[2]/p[3]/text()")[0].strip()

    desc_filename = path_to_store + "description-{}.txt".format(today)

    with open(desc_filename, "w") as out_file:
        out_file.write(header + "\n")
        out_file.write(div1 + " ")
        out_file.write(div2)

    try:
        os.remove(path_to_store + 'description.txt')
    except FileNotFoundError:
        pass
    os.symlink(desc_filename, path_to_store + 'description.txt')


path_to_store = "/home/matthias/Pictures/PicOfDay/"

get_description(path_to_store)
get_background(path_to_store)
set_background(path_to_store + 'current.jpg')

