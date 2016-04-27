import Image, ImageDraw, time, math
from random import *

width = 900
height = 600
T = 50

def normalize(value, min0, max0, minF, maxF):
	return (((value - min0)*(maxF-minF))/(max0-min0))+minF
	
def mandela(exp):
	for x in range(width):
		for y in range(height):
			cpx_x = normalize(x, 0, width, -1, 1)
			cpx_y = normalize(y, 0, height, -1, 1)
			c = complex(-0.5,0.1)
			z = complex(cpx_x,cpx_y)
			for i in range(T):
				z = z**exp + c
				'''A more computationally complex method that detects escapes sooner, is to compute distance from the origin using the Pythagorean theorem, i.e., to determine the absolute value, or modulus, of the complex number '''
				if abs(z) >= 2:
					draw.point((x,y),fill="black")
					break

im = Image.new("RGB", (width,height), "white")
draw = ImageDraw.Draw(im)
mandela(2)
im.save("moko" + str(2) + ".jpg")