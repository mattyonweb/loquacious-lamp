import math
colorblind_colors = [(0,0,255),(0,255,255),(0,255,0),
(255,255,0),(255,0,0),(255,0,255)]


# metodi che vanno "a bbotta"
def cosine_color(iteration): #osceno
	r = int ( abs( math.cos(iteration) ) * 255)
	g = int ( abs( math.sin(iteration) ) * 255)
	b = int ( abs( math.cos(iteration)*math.sin(iteration) ) * 255)

	return (r,g,b)

def log_color(iteration, T): #bello
	num = int(255 * math.log(iteration+1) / math.log(T) )

	return (num, num, num)



def colorblind_color(iteration): #osceno
	return colorblind_colors[iteration % len(colorblind_colors)]


