import numpy as np
from scipy.fftpack import dct
from scipy.fftpack import idct
import cv2 as cv
import math
img_name = "image9.jpg"
wm_name = "images.png"
watermarked_img = "Watermarked_Image.jpg"
watermarked_extracted = "watermarked_extracted.jpg"
key = 50
bs = 8
w1 = 64
w2= 64
alfa = 1
indx = 0
indy = 0
b_cut = 50
val1  = []
val2  = []

def psnr(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
    	return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


def dct2(a):
	return cv.dct(a)
   
def idct2(a):
	return cv.idct(a)