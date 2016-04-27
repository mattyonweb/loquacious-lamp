# -*- coding: UTF-8 -*-
import time, math, cmd
from PIL import Image, ImageDraw
from random import *
import colorazioni as clz

dimension = 400 # dimensioni file output in px
T = 300 #max numero di iterazioni per la divergenza
colors = [] #dizionario dei colori; cambia ad ogni nuovo avvio
E = 2

def mandela(draw, exp = 2, coordinates = (-2.5, 1.5, -2, 2) ): 
	''' Calcola l'appartenenza di ogni pizzel all'insieme di mandelbrot
	e colora di conseguenza il pizel. segue la formula z = z^2 + c.

	Per quanto riguarda la conversione da (x,y) a (c_Re, c_Im), ho usato due
	formule abbastanza semplici:
	
	c_Re = x / (dimension / (x_max - x_min)) + x_min;
	C_Im = y_max - y / (dimension / (y_max - x_min));

	dove x_min, max ecc sono i punti estremi del sistema di riferimento
	cartesiano, di norma x=(-2.5, 1.5) e y=(-2,2).

	L'ottimizzazione del processo avviene solo se l'esponente di Z è 2, e
	consiste nell'escludere a priori i calcoli su punti che già si sa che stanno
	nell'area interna del frattale.
	https://en.wikipedia.org/wiki/Mandelbrot_set#Cardioid_.2F_bulb_checking
	'''
	#estrae le coordinate massime e minime sul piano complesso
	x_min = coordinates[0]
	x_max = coordinates[1]
	y_min = coordinates[2]
	y_max = coordinates[3]
	
	start = time.time()

	#precalculations
	DENOMIN_X = dimension / float(x_max - x_min)
	DENOMIN_Y = dimension / float(y_max - y_min)

	#booleans
	STANDARD = (exp == 2) #se l'esponente è 2, il processo si può ottimizzare
	GO_ON = True #se è possibile saltare il calcolo di alcuni punti

	for x in xrange(dimension):
		
		#la parte reale di c.
		c_re = x_min + x / DENOMIN_X

		for y in xrange(dimension):
			
			#la parte immaginaria di c
			c_im = y_max - y / DENOMIN_Y

			#metodo per ottimizzare (non fa calcolare i punti del cardioide)
			#ottimizza solo se e==2 con la formula qui sotto, altrimenti
			#fa passare tutto normalmente
			if STANDARD:
				q = (c_re - 0.25)**2 + c_im**2 
				GO_ON = not(q**2 + q*(c_re - 0.25) < 0.25 * c_im**2)
			else:
				GO_ON = True

			if GO_ON:
				#rende complesso le componenti di c
				c = complex(c_re, c_im)
				z = 0
				
				for i in xrange(T):
					#la forumla ricorsiva
					z = z**exp + c

					#se divergente, colora di conseguenza
					if abs(z) >= 2:
						#draw.point((x,y), fill = clz.log_color(i, T))
						break
						
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


def prompt():
	''' gestore delle funzioni '''
	global dimension
	
	print "+---------------------------------+"
	print "|Fractals generator.              |"
	print "|Draw fractals with us!           |"
	print "+---------------------------------+"
	
	while True:
		#manca la gestione degli errori ma vabe... confido in voi
		#dimension = int(raw_input("dimensions: "))
		is_mandel = raw_input("(m)andelbrot or (j)ulia: ")
		starting_exp = int(raw_input("starting e: "))	#per generare più immagini
														#con exp diversi.
		final_exp = int(raw_input("final e: "))
		
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

class Fractaland(cmd.Cmd):
	""" Fractaland """
	cmd.Cmd.intro = "Fractal image render. MC 2016"

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


	def do_exponent(self, exp):
		global E
		
		E = int(exp)
		

	def do_mandela(self, args):
		im = Image.new("RGB", (dimension,dimension), "white")
		draw = ImageDraw.Draw(im)

		values = args.split(" ")

		# se non sono passati argomenti, lascia quelli di default
		if values != [""]:
			tokens = list()
			
			for parameter in values:
				tokens.append(float(parameter))
			
			mandela(draw, E, tokens)
		else:
			mandela(draw, E)
			
		im.save("mandelbrot_exp" + str(E) + ".jpg")

		
	def do_quit(self, *args):
		''' quit
		quit. '''
		return True

Fractaland().cmdloop()

