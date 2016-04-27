# -*- coding: UTF-8 -*-
import time, math, cmd
from PIL import Image, ImageDraw
from random import *
import colorazioni as clz

dimension = 400 # dimensioni file output in px
T = 300 #max numero di iterazioni per la divergenza
colors = [] #dizionario dei colori; cambia ad ogni nuovo avvio

def mandela(draw, exp = 2, coordinates = (-2.5, 1.5, -2, 2) ): 
	''' Calcola l'appartenenza di ogni pizzel all'insieme di mandelbrot
	e colora di conseguenza il pizel. segue la formula z = z^2 + c.

	Per quanto riguarda la conversione da (x,y) a (c_Re, c_Im), ho usato due
	formule abbastanza semplici:
	
	c_Re = x / (dimension / (x_max - x_min)) + x_min;
	C_Im = y_max - y / (dimension / (y_max - x_min));

	dove x_min, max ecc sono i punti estremi del sistema di riferimento
	cartesiano, di norma x=(-2.5, 1.5) e y=(-2,2).
	'''

	x_min = coordinates[0]
	x_max = coordinates[1]
	y_min = coordinates[2]
	y_max = coordinates[3]
	
	start = time.time()

	#precalculations
	DENOMIN_X = dimension / float(x_max - x_min)
	DENOMIN_Y = dimension / float(y_max - y_min)
	 
	for x in xrange(dimension):
		c_re = x_min + x / DENOMIN_X	#la parte reale di c.
										#i parametri sono per centrare l'immagine.
		for y in xrange(dimension):
			c_im = y_max - y / DENOMIN_Y	#la parte immaginaria di c

			q = (c_re - 0.25)**2 + c_im**2
			if not (q**2 + q*(c_re - 0.25) < 0.25 * c_im**2):
				c = complex(c_re, c_im) #rende complesso c
				z = 0
				
				for i in xrange(T):
					z = z**exp + c #la forumla ricorsiva
					if abs(z) >= 2: #se divergente
						draw.point((x,y), fill = clz.cosine_color(i)) #colora in base a divergenza
						break	#sennò lascialo bianco (formerà la forma interna del frattale)
	print time.time() - start

	start = time.time()

	#precalculations
	DENOMIN_X = dimension / float(x_max - x_min)
	DENOMIN_Y = dimension / float(y_max - y_min)
	 
	for x in xrange(dimension):
		c_re = x_min + x / DENOMIN_X	#la parte reale di c.
										#i parametri sono per centrare l'immagine.
		for y in xrange(dimension):
			c_im = y_max - y / DENOMIN_Y	#la parte immaginaria di c
			c = complex(c_re, c_im) #rende complesso c
			z = 0
			
			for i in xrange(T):
				z = z**exp + c #la forumla ricorsiva
				if abs(z) >= 2: #se divergente
					draw.point((x,y), fill = clz.cosine_color(i)) #colora in base a divergenza
					break	#sennò lascialo bianco (formerà la forma interna del frattale)
	print time.time() - start

	
def julia(draw, exp = 2):
	''' julia set. disponibili presets... '''
	
	presets = {
	"wandering star" : (-0.7,-0.3),
	"double star" : (0.4,0.1),
	"explosion in the sky" : (0.3,0.8) }
	
	real_c = raw_input("\nJULIA\ndigit real c or (p) to see presets: ")
	if real_c == "p":
		print "*********PRESETS*********" #stampa i presets
		for el in presets:
			print el, presets[el]
		print "*********PRESETS*********"
		preset = raw_input("digit your preset, else to insert custom c: ")
		if preset in presets.keys(): #se esiste il preset digitato
			real_c = presets[preset][0]
			imag_c = presets[preset][1]
		else: #altrimenti ricomincia
			julia(exp,draw)
			return
	else:
		real_c = float(real_c)
		imag_c = float(raw_input("imag c: "))
		
	c = complex(real_c,imag_c)
	
	start = time.time()
	for x in range(dimension):
		t = x/(dimension/3.0) - 2 #temporary var. per risparmiare calcolo
		for y in range(dimension):
			z = complex(t, y /(dimension/3.0) - 1.5)
			for i in range(T):
				z = z**exp + c #la forumla ricorsiva
				if abs(z) >= 2: #se divergente
					draw.point((x,y),fill=color(i)) #colora in base a divergenza
					break
				#sennò lascialo bianco (formerà la forma interna del frattale)
	print time.time()-start, "\n\nNUOVO FRATTALE:"

def gen_cols(colorblind = False):
	''' genera la lista di colori simili. '''
	global colors
	colors = []
	r = randint(0,255)
	g = randint(0,255)
	b = randint(0,255)
	if not colorblind:
		for _ in range(20):
			colors.append((r,g,b))
			r += randint(-25,20) #per fare un cambiamento graduale di colore
			g += randint(-25,20)
			b += randint(-25,20)
	else: #colori orribili
		list = [(0,0,255),(0,255,255),(0,255,0),(255,255,0),(255,0,0),(255,0,255)]
		for col in list:
			colors.append(col)
					
def color(valeu):
	'''ritorna sempre nel medesimo ordine un colore . '''
	return colors[valeu%len(colors)]

def prompt():
	''' gestore delle funzioni '''
	global dimension
	
	print "+---------------------------------+"
	print "|Fractals generator.              |"
	print "|Draw fractals with us!           |"
	print "+---------------------------------+"
	
	while True:
		#manca la gestione degli errori ma vabe... confido in voi
		dimension = int(raw_input("dimensions: "))
		is_mandel = raw_input("(m)andelbrot or (j)ulia: ")
		starting_exp = int(raw_input("starting e: "))	#per generare più immagini
														#con exp diversi.
		final_exp = int(raw_input("final e: "))
		x_min = float(raw_input("x_min: "))
		x_max = float(raw_input("x_max: "))
		y_min = float(raw_input("y_min: "))
		y_max = float(raw_input("y_max: "))
		
		if is_mandel == "m":
			mandel = True
		else:
			mandel = False
		
		gen_cols()
		
		for e in range(starting_exp, final_exp+1): #crea le immagini. 
			im = Image.new("RGB", (dimension,dimension), "white")
			draw = ImageDraw.Draw(im) #necessari per disegnare un'immagine
			if mandel:
				mandela(draw, e, (x_min, x_max, y_min, y_max) )
				im.save("mandelbrot_exp" + str(e) + ".jpg") 
			else:
				julia(draw, e)
				im.save("julia_exp" + str(e) + ".jpg") 
					
#prompt()

class StaticIbnizer(cmd.Cmd):
	""" Ibnizer!!! Matt """
	cmd.Cmd.intro = "Slow ibniz. MC 2015"

	#def __init__(self):
	#	gen_cols()
		
	def emptyline(self):
		return
		
	def do_bailout(self, value):
		''' draw [expr]
		draw the expression in x and y '''
		global T

		try:
			T = int(value)
		except:
			pass

	def do_size(self, value):
		global dimension

		dimension = int(value)

	def do_mandela(self, args):
		im = Image.new("RGB", (dimension,dimension), "white")
		draw = ImageDraw.Draw(im) #necessari per disegnare un'immagine

		values = args.split(" ")
		print values
		
		if values != []:
			tokens = list()
			
			for parameter in values:
				tokens.append(float(parameter))
			
			mandela(draw, 2, tokens)
		else:
			mandela(draw, 2)
		im.save("mandelbrot_exp" + str(2) + ".jpg") 
		
	def do_quit(self, *args):
		''' quit
		quit. '''
		return True

StaticIbnizer().cmdloop()

