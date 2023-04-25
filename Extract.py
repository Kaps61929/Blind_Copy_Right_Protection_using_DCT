import numpy as np
from scipy.fftpack import dct
from scipy.fftpack import idct
import cv2 as cv
import matplotlib.pyplot as plt
import random
import math
from PIL import Image
from util import dct2,idct2,psnr


img_name = "image9.jpg"
wm_name = "images.png"
watermarked_img = "Watermarked_Image.jpg"
watermarked_extracted = "watermarked_extracted.jpg"
key = 50
bs = 4
w1 = 64
w2= 64
alfa = 1
indx = 0
indy = 0
b_cut = 50
val1  = []
val2  = []


def extract_watermark(img, ext_name):
	c1x, c2x = np.size(img,0), np.size(img,1)
	
	if(c1x!=1000 or c2x != 1000):
		img = cv.resize(img, (1000, 1000))
		c1x = 1000
		c2x = 1000
	c1 = c1x - b_cut*2
	c2 = c2x-b_cut*2
	blocks = (c1//bs)*(c2//bs)
	blocks_needed = w1*w2

	wm = [[0 for x in range(w1)] for y in range(w2)]
	st = set()
	random.seed(key)
	i = 0
	cnt = 0
	while(i<blocks_needed):
		curr = 0
		x = random.randint(1, blocks)
		if(x in st):
			continue
		st.add(x)
		n = c1//bs
		m = c2//bs
		ind_i = (x//m)*bs + b_cut
		ind_j = (x%m)*bs + b_cut
		dct_block = cv.dct(img[ind_i:ind_i+bs, ind_j:ind_j+bs]/1.0)
		
		elem = dct_block[indx][indy]
		elem = math.floor(elem+0.5)
		elem /= alfa
		
		if(elem%2 == 0):
			curr = 0
		else:
			curr = 255
		val2.append( (elem, bool(curr)))
		
		wm[i//w2][i%w2] = curr
		i+=1
		
		

	wm = np.array(wm)
	cv.imwrite(ext_name , wm)
	print("Watermark extracted and saved in", ext_name)
	return wm