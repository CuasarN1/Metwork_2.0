import numpy as np
import cv2


im = cv2.imread('./Snapshot.png')
a = np.asarray(im)
print(a[0][0])
