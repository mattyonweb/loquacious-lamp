''' logistic map. Per information: https://it.wikipedia.org/wiki/Mappa_logistica'''
# -*- coding: UTF-8 -*-
from PIL import Image, ImageDraw
import time


WIDTH = int(raw_input("width: "))
HEIGHT = int(raw_input("height: "))

def normalize(value, min0, max0, minF, maxF):
	''' rinormalizza un valore (come map in processing) '''
	return (((value - min0)*(maxF-minF))/(max0-min0))+minF

y = 0.8 #valore iniziale, y0 = ...
r = r_in = 1 #valore della variabile r (come una x in una f(x))
r_max = 4 #valore max r (limite intrinseco della formula)

im = Image.new("RGB", (WIDTH, HEIGHT), "black")
draw = ImageDraw.Draw(im)

while r < 4: #for non ammette step di valori non integer.......
	
	for _ in range(400):
		y = r * y * (1-y) #la formula y(n+1) = r*y(n)*(1-y(n))
	
	minilist = []	#per velocizzare il calcolo, se un punto e' gia' stato disegnato
					#lo si appende qui e non si ridisegna.
	for _ in range(200):
		y = r * y * (1-y)
		
		if y not in minilist:
			minilist.append(y) #vedi sopra
			
			screen_x = normalize(r,r_in,r_max+0.01,0,WIDTH) #converti r ad una x in px
			screen_y = normalize(y,0,1,0,HEIGHT)
			draw.point((screen_x, screen_y), fill = "white")
	r += 0.001

im.save("cazzo.jpg")
