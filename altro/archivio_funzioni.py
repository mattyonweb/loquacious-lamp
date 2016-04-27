''' archivio di funzioni obsolete o non utili '''

def slighty_faster_sometimes_mandelbrot(draw, exp = 2):

	start = time.time()

	matrix = [[0 for x in xrange(dimension)] for y in xrange(dimension)]

	dim_4 = dimension / 4.0

	for x in xrange(dimension):
		c_re = x / dim_4 - 2.5
		
		for y in xrange(dimension):
			c_im = y / dim_4 - 2
			
			c = complex(c_re, c_im) 
			z = 0
			
			for i in xrange(T):
				z = z**exp + c 
				if abs(z) >= 2: 
					matrix[x][y] = i
					break
			else:
				matrix[x][y] = T

	for x in xrange(dimension):
		for y in xrange(dimension):
			color_int = int(abs(math.cos(matrix[x][y])*255))
			draw.point((x,y), fill = (color_int,color_int,color_int))
					
	print time.time() - start

