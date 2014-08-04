__author__ = 'David'

import matplotlib.pyplot as plt
import numpy
from skimage.feature import hog
from skimage import data, color, exposure

# Image is 512*512
# image = color.rgb2gray(data.lena())
image = data.lena();
image = color.rgb2gray(image);
pixels_per_cell = 64

patches = []

for y_start in range(0, len(image) - pixels_per_cell, pixels_per_cell):
    for x_start in range(0, len(image[0]) - pixels_per_cell, pixels_per_cell):
        cropped_image = image[y_start:y_start + pixels_per_cell, x_start:x_start + pixels_per_cell]
        patches.append(cropped_image)


# Show patches
# ===========================
for i in range(49):
    plt.subplot(7, 7, i)
    if i >= len(patches): break;
    plt.imshow(patches[i])
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.tight_layout()
plt.show()






# fd, hog_image = hog(image, orientations=31, pixels_per_cell=(64, 64),
#                     cells_per_block=(1, 1), visualise=True)
#
#
# numpy.savetxt('features.txt', fd)








# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
#
# ax1.axis('off')
# ax1.imshow(image, cmap=plt.cm.gray)
# ax1.set_title('Input image')
#
# # Rescale histogram for better display
# hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))
#
# ax2.axis('off')
# ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
# ax2.set_title('Histogram of Oriented Gradients')
# plt.show()