import os
import imagehash
from PIL import Image
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def alpharemover(image):
    if image.mode != 'RGBA':
        return image
    canvas = Image.new('RGBA', image.size, (255, 255, 255, 255))
    canvas.paste(image, mask=image)
    return canvas.convert('RGB')


def with_ztransform_preprocess(hashfunc, hash_size=8):
    def function(path):
        image = alpharemover(Image.open(path))
        image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
        data = image.getdata()
        quantiles = np.arange(100)
        quantiles_values = np.percentile(data, quantiles)
        zdata = (np.interp(data, quantiles_values, quantiles) / 100 * 255).astype(np.uint8)
        image.putdata(zdata)
        return hashfunc(image)

    return function


def Duplicates(in_arr):
    dhash_z_transformed = with_ztransform_preprocess(imagehash.dhash, hash_size=8)
    hashs = []
    for i in range(len(in_arr)-1, 0, -1):
        pic = in_arr[i]
        hash = dhash_z_transformed(pic)
        if hash not in hashs:
            hashs.append(hash)
        else:
            os.unlink(pic)

    size = len(hashs)
    return size, len(in_arr) - size
