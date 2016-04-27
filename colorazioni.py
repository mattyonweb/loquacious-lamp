import math

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

def cosine_color(iteration):
	r = int ( abs( math.cos(iteration) ) * 255)
	g = int ( abs( math.sin(iteration) ) * 255)
	b = int ( abs( math.cos(iteration)*math.sin(iteration) ) * 255)

	return (r,g,b)

#stronzo
