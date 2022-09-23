from glob import glob
from PIL import Image as pil
from random import randint as rand

files = glob('../balanced/Cropped normal/' + '*.png')
with open('./image (1).xml', 'r', encoding='UTF-8') as file:
    xml = ''.join(file.readlines())
for file in files:
    name = file.split('/')[-1]
    class_name = 'Normal'
    original = pil.open(file)
    width, height = original.size
    for _ in range(10):
        bbox_h = rand(int(height * 0.33), int(height * 0.67))
        bbox_w = rand(int(width * 0.33), int(width * 0.67))
        xmin = rand(0, width - bbox_w)
        ymin = rand(0, height - bbox_h)
        xmax = xmin + bbox_w
        ymax = ymin + bbox_h
        img = original.crop((xmin, ymin, xmax, ymax)).convert('P', palette=pil.ADAPTIVE, colors=20).convert("RGB")
        arr = pil.Image.getcolors(img)
        arr = sorted(arr, key=lambda e: e[0], reverse=True)
        if sum(arr[0][1]) / 3 > 100:
            break

    with open('./NormalXML/' + name + '.xml', 'w', encoding='UTF-8') as out:
        out.write(
            xml.replace('<filename>file_name</filename>', f'<filename>{name}</filename>')
               .replace('<width>0</width>', f'<width>{width}</width>')
               .replace('<height>0</height>', f'<height>{height}</height>')
               .replace('<name>class_name</name>', f'<name>{class_name}</name>')
               .replace('<xmin>0</xmin>', f'<xmin>{xmin}</xmin>')
               .replace('<ymin>0</ymin>', f'<ymin>{ymin}</ymin>')
               .replace('<xmax>0</xmax>', f'<xmax>{xmax}</xmax>')
               .replace('<ymax>0</ymax>', f'<ymax>{ymax}</ymax>')
        )
