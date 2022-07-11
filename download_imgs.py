from fastbook import search_images_ddg, download_url
from fastprogress.fastprogress import progress_bar
import argparse
from PIL import Image
from os import remove, mkdir
from os.path import isdir

IMAGE_SUFF = 'jpeg,jpg,png,bmp,webp'.split(',')

parser = argparse.ArgumentParser(description='Search and download images from duckduckgo.com')
parser.add_argument('key', type=str, help='Term to search for')
parser.add_argument('max_n', type=int, help='Maximum number of images to download')
parser.add_argument('-f', '--folder', type=str, help='Destination folder', default='.')
args = parser.parse_args()

if __name__ == "__main__":
    key = args.key
    max_n = args.max_n
    folder = args.folder

    print(f"Get image urls for searchterm '{key}'...")
    urls = search_images_ddg(key, max_images = max_n)
    with open('sources.txt', 'w') as f:
        for line in urls:
            f.write(f"{line}\n")

    if not isdir(folder):
        print(f"Create destination folder {folder}...")
        mkdir(folder)

    print(f"Download {len(urls)} images...")
    p_bar = progress_bar(urls)
    for i, url in enumerate(p_bar):
        ## Some instances do pass queries in the url
        suffix = url.split('.')[-1].split('?')[0]
        ## Skip image formats that are not expected
        if suffix.lower() not in IMAGE_SUFF: 
            continue
        try:
            fn = f'{folder}/{key}_{i+1}'
            download_url(url, dest = fn, show_progress = False)
            ## Unify file format
            try:
                img = Image.open(fn)
                img.save(fn + '.jpg')
            except:
                print(f"Couldn't open image from {url}\n")
            finally:
                remove(fn)
        except:
            print(f"Couldn't download {url}\n")
    print('\nDone')