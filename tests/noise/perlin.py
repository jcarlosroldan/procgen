from os import chdir
chdir("../..")

from procgen.noise import perlin, combined
import matplotlib.pyplot as plt
from random import randint, random
from time import time
from math import sin, pi

def functional():
	print("Testing octave known values from original Java Improved Perlin")
	assert perlin(.5, .5, .5) == -0.25, "Midpoint values don't match"
	assert perlin(.0001, .001, .01) == 0.010109641532713891, "Small values don't match"
	assert perlin(1000.7, 1000.5, 1000.3) == 0.11639213824006686, "Big values don't match"
	for _ in range(100): # integer values
		assert perlin(randint(0, 100), randint(0, 100), randint(0, 100)) == 0, "Integer values don't match"
	assert perlin(-12.3, -4.56, -.789) == 0.6118981098223655, "Negative values don't match"

def performance1():
	print("Testing time to fill a 200x200 array with default parameters")
	base = time()
	N = 200
	pmap = [[combined(perlin, x/N, y/N, 0) for x in range(N)] for y in range(N)]
	assert time() - base < 3

def performance2():
	print("Testing time to fill a 70x70 array with 15 octaves")
	base = time()
	N = 70
	pmap = [[combined(perlin, x/N, y/N, 0, octaves = 50) for x in range(N)] for y in range(N)]
	assert time() - base < 3

def performance3():
	print("Testing time to fill a 30x30x30 array with default parameters")
	base = time()
	N = 30
	pmap = [[[combined(perlin, x/N, y/N, z/N) for x in range(N)] for y in range(N)] for z in range(N)]
	assert time() - base < 3

def subjective():
	print("Displaying 2D perlin output")
	N = 100
	pmap = [[combined(perlin, x/N, y/N, 0) for x in range(N)] for y in range(N)]
	
	plt.subplot(221)
	plt.title("6 octaves")
	plt.imshow(pmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(222)
	plt.title("1 octave")
	pmap = [[combined(perlin, 6*x/N, 6*y/N, 0, 1) for x in range(N)] for y in range(N)]
	plt.imshow(pmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(223)
	plt.title("4 octaves, marbled")
	mpmap = [[sin(1.6 * 2 * pi * combined(perlin, 6*x/N, 6*y/N, 0, 4)) for x in range(N)] for y in range(N)]
	plt.imshow(mpmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(224)
	plt.title("15 octaves, crinkled")
	cpmap = [[combined(perlin, 10*x/N, 10*y/N, .2, 15) for x in range(N)] for y in range(N)]
	plt.imshow(cpmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.show()

functional()
performance1()
performance2()
performance3()
subjective()