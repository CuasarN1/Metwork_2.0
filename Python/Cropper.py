from PIL import Image
from glob import glob
from shutil import copy


files = glob('../balanced/Нормальная слизистая желудка/' + '*.png')
for file in files:
    if 'V' in file:
        img = Image.open(file)
        img = img.crop((300, 30, 1650, 1080))
        name = '../balanced/Cropped normal/' + file.split('/')[-1]
        img.save(name)
    else:
        copy(file, file.replace('Нормальная слизистая желудка', 'Cropped normal'))
