import numpy as np
from scipy.fftpack import dct
from scipy.fftpack import idct
import cv2 as cv
import matplotlib.pyplot as plt
import random
import math
from PIL import Image
from Embed import Embedding
from Extract import extract_watermark
from util import *

img_name = "image9.jpg"
wm_name = "images.png"
watermarked_img = "Watermarked_Image.jpg"
watermarked_extracted = "watermarked_extracted.jpg"
key = 50
bs = 4
w1 = 64
w2= 64
alfa = 6
indx = 0
indy = 0
b_cut = 50
val1  = []
val2  = []


if __name__ == "__main__":

	print("Main image: " + img_name)
	print("Watermark: " + wm_name)

	print("EMBEDDING WATERMARK")
	img =  cv.imread(img_name, 0) 

	wm = cv.imread(wm_name, 0) 
	wm = cv.resize(wm, dsize=(64, 64), interpolation=cv.INTER_CUBIC)
	

	wmed = Embedding(img, wm)
	
	print("\nWatermarking Done!\n")
	
	print("EXTRACTING WATERMARK")


	wx = extract_watermark(wmed, watermarked_extracted)

	x = cv.imread(wm_name)
	y = cv.imread(watermarked_extracted)
	cv.waitKey()
	ch = 0

	
	