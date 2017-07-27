from os import chdir
chdir("../..")

from procgen.noise import combined, simplex2D, simplex3D, simplex4D
import matplotlib.pyplot as plt
from random import randint, random
from time import time
from math import sin, pi

def simplex2D_functional():
	print("Testing octave known values from Simplex 2D")
	assert simplex2D(.5, .5) == -0.3071565136272162, "Midpoint values don't match"
	assert simplex2D(.01, .0001) == -0.04371500700069976, "Small values don't match"
	assert simplex2D(1000.7, 1000.5) == 0.17147330450984027, "Big values don't match"
	assert simplex2D(18, 27) == 0.29237504347338594, "Integer values don't match"
	assert simplex2D(-12.3, -4.56) == -0.4989217198112214, "Negative values don't match"
	print("\tAll values working properly")

def simplex3D_functional():
	print("Testing octave known values from Simplex 3D")
	assert simplex3D(.5, .5, .5) == 0.0, "Midpoint values don't match"
	assert simplex3D(.0001, .001, .01) == 0.00455884877874096, "Small values don't match"
	assert simplex3D(1000.7, 1000.5, 1000.3) == 0.4804158933337156, "Big values don't match"
	assert simplex3D(18, 27, 31) == -0.10787818930040446, "Integer values don't match"
	assert simplex3D(-12.3, -4.56, -.789) == -0.3476189050698857, "Negative values don't match"
	print("\tAll values working properly")

def simplex4D_functional():
	print("Testing octave known values from Simplex 4D")
	assert simplex4D(.5, .5, .5, .5) == -0.17136317120636763, "Midpoint values don't match"
	assert simplex4D(.0001, .001, .01, .1) == 0.00455884877874096, "Small values don't match"
	assert simplex4D(1000.7, 1000.5, 1000.3, 1000.1) == -0.5058875159738829, "Big values don't match"
	assert simplex4D(18, 27, 31, 501) == -0.2979980307818446, "Integer values don't match"
	assert simplex4D(-12.3, -4.56, -.789, .818) == 0.09439190689205242, "Negative values don't match"
	print("\tAll values working properly")

def simplex2D_performance():
	print("Testing time to fill a 200x200 array with default parameters")
	base = time()
	N = 200
	pmap = [[combined(simplex2D, x/N, y/N) for x in range(N)] for y in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def simplex2D_performance2():
	print("Testing time to fill a 70x70 array with 15 octaves")
	base = time()
	N = 70
	pmap = [[combined(simplex2D, x/N, y/N, octaves = 50) for x in range(N)] for y in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def simplex3D_performance():
	print("Testing time to fill a 30x30x30 array with default parameters")
	base = time()
	N = 30
	pmap = [[[combined(simplex3D, x/N, y/N, z/N) for x in range(N)] for y in range(N)] for z in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 2.5

def simplex4D_performance():
	print("Testing time to fill a 10x10x10x10 array with default parameters")
	base = time()
	N = 10
	pmap = [[[[combined(simplex4D, x/N, y/N, z/N, w/N) for x in range(N)] for y in range(N)] for z in range(N)] for w in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def simplex2D_subjective():
	print("Displaying 2D simplex output")
	N = 100
	pmap = [[combined(simplex2D, x/N, y/N) for x in range(N)] for y in range(N)]
	
	plt.subplot(221)
	plt.title("6 octaves")
	plt.imshow(pmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(222)
	plt.title("1 octave")
	pmap = [[combined(simplex2D, 6*x/N, 6*y/N, octaves = 1) for x in range(N)] for y in range(N)]
	plt.imshow(pmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(223)
	plt.title("4 octaves, marbled")
	mpmap = [[sin(1.6 * 2 * pi * combined(simplex2D, 6*x/N, 6*y/N, octaves = 4)) for x in range(N)] for y in range(N)]
	plt.imshow(mpmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(224)
	plt.title("15 octaves, crinkled")
	cpmap = [[combined(simplex2D, 10*x/N, 10*y/N, octaves = 15) for x in range(N)] for y in range(N)]
	plt.imshow(cpmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.show()

simplex2D_functional()
simplex3D_functional()
simplex4D_functional()
simplex2D_performance()
simplex2D_performance2()
simplex3D_performance()
simplex4D_performance()
simplex2D_subjective()