"""
===================
Canny edge detector
===================

The Canny filter is a multi-stage edge detector. It uses a filter based on the
derivative of a Gaussian in order to compute the intensity of the gradients.The
Gaussian reduces the effect of noise present in the image. Then, potential
edges are thinned down to 1-pixel curves by removing non-maximum pixels of the
gradient magnitude. Finally, edge pixels are kept or removed using hysteresis
thresholding on the gradient magnitude.

The Canny has three adjustable parameters: the width of the Gaussian (the
noisier the image, the greater the width), and the low and high threshold for
the hysteresis thresholding.

"""
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import os

from skimage import feature, io, morphology

dirpath = os.getcwd()
files = ['samolot01.jpg', 'samolot10.jpg',
         'samolot08.jpg','samolot09.jpg',
         'samolot17.jpg','samolot19.jpg']
edges = []
for file in files:
    image = io.imread(file, True)
    edge = feature.canny(image, sigma=1.7)
    edges.append(edge)

# display results
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(50, 50))

for axis, edge in zip(axes.flatten(), edges):
    axis.imshow(edge, cmap=plt.cm.gray)
    axis.axis('off')

fig.tight_layout()

#plt.show()

fig.savefig('result.png', bbox_inches='tight')
