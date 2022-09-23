import json
from glob import glob
import cv2


files = glob('../Reduced blood/*.json')
print(len(files))
with open('./image (1).xml', 'r', encoding='UTF-8') as file:
    xml = ''.join(file.readlines())
for file in files:
    with open(file, 'r', encoding='UTF-8') as j:
        buff = json.load(j)
    name = buff['metadata']['name']
    class_name = buff['instances'][0]['className']
    xy = buff['instances'][0]['points']
    xmin, ymin = round(xy['x1']), round(xy['y1'])
    xmax, ymax = round(xy['x2']), round(xy['y2'])
    xmin = min(xmin, xmax)
    xmax = max(xmin, xmax)
    ymin = min(ymin, ymax)
    ymax = max(ymin, ymax)
    image = cv2.imread('../balanced/Редуцированная кровь/'+name)
    height, width = image.shape[0], image.shape[1]
    with open('./ReducedBloodXML/'+name+'.xml', 'w', encoding='UTF-8') as x:
        x.write(
            xml.replace('<filename>file_name</filename>', f'<filename>{name}</filename>')
                .replace('<width>0</width>', f'<width>{width}</width>')
                .replace('<height>0</height>', f'<height>{height}</height>')
                .replace('<name>class_name</name>', f'<name>{class_name}</name>')
                .replace('<xmin>0</xmin>', f'<xmin>{xmin}</xmin>')
                .replace('<ymin>0</ymin>', f'<ymin>{ymin}</ymin>')
                .replace('<xmax>0</xmax>', f'<xmax>{xmax}</xmax>')
                .replace('<ymax>0</ymax>', f'<ymax>{ymax}</ymax>')
        )
