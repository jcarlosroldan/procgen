from os import chdir
chdir("../..")

from procgen.noise import perlin2D, perlin3D, combined
import matplotlib.pyplot as plt
from random import randint, random
from time import time
from math import sin, pi

def perlin3D_functional():
	print("Testing octave known values from Perlin 3D")
	assert perlin3D(.5, .5, .5) == -0.25, "Midpoint values don't match"
	assert perlin3D(.0001, .001, .01) == 0.010109641532713891, "Small values don't match"
	assert perlin3D(1000.7, 1000.5, 1000.3) == 0.11639213824006686, "Big values don't match"
	for _ in range(100):
		assert perlin3D(randint(0, 100), randint(0, 100), randint(0, 100)) == 0, "Integer values don't match"
	assert perlin3D(-12.3, -4.56, -.789) == 0.6118981098223655, "Negative values don't match"
	print("\tAll values working properly")

def perlin2D_functional():
	print("Testing octave known values using Perlin 3D coherency")
	assert perlin2D(.5, .5) == perlin3D(.5, .5, 0), "Midpoint values don't match"
	assert perlin2D(.01, .0001) == perlin3D(.01, .0001, 0), "Small values don't match"
	assert perlin2D(1000.7, 1000.5) == perlin3D(1000.7, 1000.5, 0), "Big values don't match"
	assert perlin2D(18, 27) == perlin3D(18, 27, 0), "Integer values don't match"
	assert perlin2D(-12.3, -4.56) == perlin3D(-12.3, -4.56, 0), "Negative values don't match"
	print("\tAll values working properly")

"""def perlin4D_functional():
	print("Testing octave known values from Perlin 4D")
	assert perlin4D(.5, .5, .5, .5) == 0.2853462173341185, "Midpoint values don't match"
	assert perlin4D(.0001, .001, .01, .1) == 0.057808284276409806, "Small values don't match"
	assert perlin4D(1000.7, 1000.5, 1000.3, 1000.1) == -0.02126810949214044, "Big values don't match"
	assert perlin4D(18, 27, 31, 501) == -0.03761175258869856, "Integer values don't match"
	assert perlin4D(-12.3, -4.56, -.789, .818) == -0.32345225144839684, "Negative values don't match"
	print("\tAll values working properly")"""

def perlin2D_performance():
	print("Testing time to fill a 200x200 array with default parameters")
	base = time()
	N = 200
	pmap = [[combined(perlin2D, x/N, y/N) for x in range(N)] for y in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def perlin2D_performance2():
	print("Testing time to fill a 70x70 array with 15 octaves")
	base = time()
	N = 70
	pmap = [[combined(perlin2D, x/N, y/N, octaves = 50) for x in range(N)] for y in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def perlin3D_performance():
	print("Testing time to fill a 30x30x30 array with default parameters")
	base = time()
	N = 30
	pmap = [[[combined(perlin3D, x/N, y/N, z/N) for x in range(N)] for y in range(N)] for z in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 2.5

def perlin4D_performance():
	print("Testing time to fill a 10x10x10x10 array with default parameters")
	base = time()
	N = 10
	pmap = [[[[combined(perlin4D, x/N, y/N, z/N, w/N) for x in range(N)] for y in range(N)] for z in range(N)] for w in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def perlin2D_subjective():
	print("Displaying 2D perlin output")
	N = 100
	pmap = [[combined(perlin2D, x/N, y/N) for x in range(N)] for y in range(N)]
	
	plt.subplot(221)
	plt.title("6 octaves")
	plt.imshow(pmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(222)
	plt.title("1 octave")
	pmap = [[combined(perlin2D, 6*x/N, 6*y/N, octaves = 1) for x in range(N)] for y in range(N)]
	plt.imshow(pmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(223)
	plt.title("4 octaves, marbled")
	mpmap = [[sin(1.6 * 2 * pi * combined(perlin2D, 6*x/N, 6*y/N, octaves = 4)) for x in range(N)] for y in range(N)]
	plt.imshow(mpmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(224)
	plt.title("15 octaves, crinkled")
	cpmap = [[combined(perlin2D, 10*x/N, 10*y/N, octaves = 15) for x in range(N)] for y in range(N)]
	plt.imshow(cpmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.show()

perlin2D_functional()
perlin3D_functional()
#perlin4D_functional()
perlin2D_performance()
perlin2D_performance2()
perlin3D_performance()
#perlin4D_performance()
perlin2D_subjective()