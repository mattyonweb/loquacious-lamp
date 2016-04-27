import time
import math

def cos(cpx):
	#real = math.cos(cpx.real)*math.cosh(cpx.imag)
	#imag = -math.sin(cpx.real)*math.sinh(cpx.imag)
	return complex(math.cos(cpx.real)*math.cosh(cpx.imag), -math.sin(cpx.real)*math.sinh(cpx.imag))
	#return result
	
def cos1(cpx):
	real = math.cos(cpx.real)*math.cosh(cpx.imag)
	imag = -math.sin(cpx.real)*math.sinh(cpx.imag)
	result =  complex(real, imag)
	return result
	
start = time.time()
for x in range(100):
	for y in range(100):
		cpx = complex(x,y)
		cos(cpx)
print time.time()-start

start = time.time()
for x in range(100):
	for y in range(100):
		cpx = complex(x,y)
		cos1(cpx)
print time.time()-start
