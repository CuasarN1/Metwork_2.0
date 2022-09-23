from glob import glob
from PIL import Image
import os


folders = ['../edited/Свежая кровь/']

for f in folders:
    pics = glob(f + '*.bmp') + glob(f + '*.JPG')
    out = f.replace('raw', 'edited').replace('..', '/Users/cuasar/Documents/GitHub/MedWork')
    if not os.path.isdir(out):
        os.makedirs(out)

    for i, img in enumerate(pics):
        Image.open(img).save(out + 'P' + f'{i+1}.png')
