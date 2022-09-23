from glob import glob
import os


pic_path = '../balanced/'
classes = [('Свежая кровь/', 'FreshBlood'),
           ('Застойное содержимое/', 'Stagnant'),
           ('Нормальная слизистая желудка/', 'Normal'),
           ('Редуцированная кровь/', 'ReducedBlood')]

for class_name in classes:
    files = glob(pic_path + class_name[0] + '*.png')
    for file in files:
        name = file.split('/')[-1]
        newname = class_name[1] + name
        xmlpath = f'./{class_name[1]}XML/{name}.xml'
        with open(xmlpath, 'r', encoding='UTF-8') as xml:
            text = ''.join(xml.readlines()).replace(name, newname)
        with open(xmlpath, 'w', encoding='UTF-8') as xml:
            xml.write(text)
        os.rename(xmlpath, xmlpath.replace(name, newname))
        os.rename(file, file.replace(name, newname))
