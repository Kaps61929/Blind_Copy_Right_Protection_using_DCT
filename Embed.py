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



def Embedding(img, wm):
	
	c1, c2 = np.size(img,0), np.size(img,1)
	c1x = c1
	c2x = c2
	c1-= b_cut*2
	c2-= b_cut*2
	w1, w2 = np.size(wm,0), np.size(wm, 1)
	
	print(c1, c2, w1, w2)

	if(c1*c2//(bs*bs) < w1*w2):
		print("watermark too large.")
		return img

	st = set()
	blocks = (c1//bs)*(c2//bs)
	print("Blocks availaible", blocks)
	blocks_needed = w1*w2
	
	i = 0
	j = 0
	imf = np.float32(img)
	while(i<c1x):
		while(j<c2x):
			#print(i, j)		
			dst = cv.dct(imf[i:i+bs, j:j+bs]/1.0)
			imf[i:i+bs, j:j+bs] = cv.idct(dst)
			j+=bs
		j = 0
		i+=bs
	final = img
	random.seed(key)
	i = 0
	print("Blocks needed", blocks_needed)
	cnt = 0
	while(i < blocks_needed):				
		to_embed = wm[i//w2][i%w2]
		ch = 0
		if(to_embed >= 127):
			to_embed = 1
			ch = 255
		else:
			to_embed = 0
		
		wm[i//w2][i%w2] = ch
		x = random.randint(1, blocks)
		if(x in st):
			continue
		st.add(x)
		n = c1//bs
		m = c2//bs
		ind_i = (x//m)*bs + b_cut
		ind_j = (x%m)*bs + b_cut
		dct_block = cv.dct(imf[ind_i:ind_i+bs, ind_j:ind_j+bs]/1.0)
		elem = dct_block[indx][indy]
		elem /= alfa
		ch = elem
		if(to_embed%2==1):	
			if(math.ceil(elem)%2==1):
				elem = math.ceil(elem)
			else:
				elem = math.ceil(elem)-1
		else:
			if(math.ceil(elem)%2==0):
				elem = math.ceil(elem)
			else:
				elem = math.ceil(elem)-1

		
		dct_block[indx][indy] = elem*alfa
		val1.append((elem*alfa, to_embed))
		if(cnt < 5):
			cnt+=1
		
		final[ind_i:ind_i+bs, ind_j:ind_j+bs] = cv.idct(dct_block)
		imf[ind_i:ind_i+bs, ind_j:ind_j+bs] = cv.idct(dct_block)
		i += 1

	final = np.uint8(final)
	print("PSNR is:", psnr(imf, img))
	# cv.imshow("Final", final)
	cv.imwrite(watermarked_img , final)
	return imf