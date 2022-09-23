from glob import glob
from shutil import copy
import os


ratio = 5  # 80 : 20
if not os.path.isdir('../VOC/train/images'):
    os.makedirs('../VOC/train/images')
    os.mkdir('../VOC/train/annotations')
    os.makedirs('../VOC/validation/images')
    os.mkdir('../VOC/validation/annotations')

classes = [('Свежая кровь', 'FreshBloodXML'),
           ('Застойное содержимое', 'StagnantXML'),
           ('Нормальная слизистая желудка', 'NormalXML'),
           ('Редуцированная кровь', 'ReducedBloodXML')]

for class_name in classes:
    xmls = glob(f'../XMLs/{class_name[1]}/'+'*.xml')

    for i, xml in enumerate(xmls):
        image = f'../balanced/{class_name[0]}/'+xml.split('/')[-1].replace('.xml', '')
        if i % 5 == 0:
            copy(xml, '../VOC/validation/annotations/' + xml.split('/')[-1])
            copy(image, '../VOC/validation/images/' + image.split('/')[-1])
        else:
            copy(xml, '../VOC/train/annotations/' + xml.split('/')[-1])
            copy(image, '../VOC/train/images/' + image.split('/')[-1])

