import cv2
from skimage import data, io, feature, color, filters, morphology, measure, transform, draw
import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_ubyte
from skimage import img_as_float

from skimage.filters import try_all_threshold
'''
vidcap=cv2.VideoCapture('film.mp4')
while True:
    ret, frame=vidcap.read()

    s = img_as_float(frame)
    s = color.rgb2gray(s)
    s = filters.gaussian(s, 0.7)
    s_cut = s[:, 79:559]
    
    thresh = filters.threshold_yen(s_cut)
    s = s > thresh
    #s = morphology.closing(s,np.ones((1,1)))
    s=morphology.erosion(s)
    #s[:, :79] = 1
    #s[:, 559:] = 1
    #s = morphology.closing(s)

    # Uciencie bokow - zeby nie bylo widac cieni albo bokow zeszytu
    
    c = img_as_ubyte(s)
    cv2.imshow('frame' , c )
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
#cam.release()
cv2.destroyAllWindows()

'''

def adaptive_thresh():


    image = cv2.imread("/home/radziu/Desktop/KCK/projekt/test1.jpg")
    #image=color.rgb2gray(image)
    image = np.uint8(color.rgb2gray(image)*255)
    #image= data.page()
    s = filters.gaussian(image, 0.1)

    # obciecie zdjecia by skupic sie na planszy i znalezc dokladniej threshold
    

    s_cut = s[:, 79:559]
    global_thresh = filters.threshold_yen(s_cut)
    s = s > global_thresh
    
    binary_global = s > global_thresh

    block_size = 35
    local_thresh = filters.threshold_local(image, 165,offset=5)
    binary_local = image > local_thresh
    #binary_local=filters.median(binary_local);

    fig, axes = plt.subplots(nrows=3, figsize=(7, 8))
    ax = axes.ravel()
    plt.gray()

    ax[0].imshow(image)
    ax[0].set_title('Original')

    ax[1].imshow(binary_global)
    ax[1].set_title('Global thresholding')

    ax[2].imshow(binary_local)
    ax[2].set_title('Local thresholding')

    for a in ax:
        a.axis('off')


    plt.show()


def normal_thresh():
    image = cv2.imread("/home/radziu/Desktop/KCK/projekt/zle.jpg")
    image= color.rgb2gray(image)
    print(type(image))
    thresh = filters.threshold_otsu(image)
    binary = image > thresh

    fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
    ax = axes.ravel()
    ax[0] = plt.subplot(1, 3, 1)
    ax[1] = plt.subplot(1, 3, 2)
    ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0])

    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].set_title('Original')
    ax[0].axis('off')

    ax[1].hist(image.ravel(), bins=256)
    ax[1].set_title('Histogram')
    ax[1].axvline(thresh, color='r')

    ax[2].imshow(binary, cmap=plt.cm.gray)
    ax[2].set_title('Thresholded')
    ax[2].axis('off')

    plt.show()

adaptive_thresh()
'''

import cv2
import numpy as np
image = cv2.imread('stack.jpg',-1)
paper = cv2.resize(image,(500,500))
ret, thresh_gray = cv2.threshold(cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY),
                        200, 255, cv2.THRESH_BINARY)
image, contours, hier = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
for c in contours:
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    # convert all coordinates floating point values to int
    box = np.int0(box)
    # draw a green 'nghien' rectangle
    cv2.drawContours(paper, [box], 0, (0, 255, 0),1)

cv2.imshow('paper', paper)
cv2.imwrite('paper.jpg',paper)
cv2.waitKey(0)

'''