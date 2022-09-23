from PIL import Image
from glob import glob
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


path = '../edited/Свежая кровь/'
pics = glob(path + '*.png')
for pic in pics:
    original_img = Image.open(pic)

    vertical_img = original_img.transpose(method=Image.FLIP_TOP_BOTTOM)
    horizontal_img = original_img.transpose(method=Image.FLIP_LEFT_RIGHT)
    both_img = original_img.transpose(method=Image.FLIP_LEFT_RIGHT).transpose(method=Image.FLIP_TOP_BOTTOM)
    vertical_img.save(pic.replace('png', 'ver.png'))
    horizontal_img.save(pic.replace('png', 'hor.png'))
    both_img.save(pic.replace('png', 'both.png'))

    original_img.close()
    vertical_img.close()
    horizontal_img.close()
    both_img.close()
