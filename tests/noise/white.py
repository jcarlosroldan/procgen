from os import chdir, path
from sys import path as spath
spath.append(path.abspath('../..'))

from procgen.noise import white, combined
import matplotlib.pyplot as plt
from random import randint, random, randrange
from time import time
from math import sin, pi
from scipy.stats import spearmanr

def white2D_functional():
	print("Testing correlation for 2D white noise")
	N = 100
	x1 = randrange(-1000, 1000, 1)
	y1 = randrange(-1000, 1000, 1)
	x2 = x1 + randrange(-1000, 1000, 1)
	y2 = y1 + randrange(-1000, 1000, 1)
	values1 = [[combined(white, x / N, y / N) for x in range(x1, x1 + N)] for y in range(y1, y1 + N)]
	values2 = [[combined(white, x / N, y / N) for x in range(x2, x2 + N)] for y in range(y2, y2 + N)]
	rho = spearmanr(values1, values2, axis=None)
	assert abs(rho[0]) < 0.5
	print("rho = %s" % rho[0])
	print("\tNot signifying correlation found")

def white3D_functional():
	print("Testing correlation for 3D white noise")
	N = 100
	x1 = randrange(-1000, 1000, 1)
	y1 = randrange(-1000, 1000, 1)
	z1 = randrange(-1000, 1000, 1)
	x2 = x1 + randrange(-1000, 1000, 1)
	y2 = y1 + randrange(-1000, 1000, 1)
	z2 = z1 + randrange(-1000, 1000, 1)
	values1 = [[[combined(white, x / N, y / N) for x in range(x1, x1 + N)] for y in range(y1, y1 + N)] for z in range(z1, z1 + N)]
	values2 = [[[combined(white, x / N, y / N) for x in range(x2, x2 + N)] for y in range(y2, y2 + N)] for z in range(z2, z2 + N)]
	rho = spearmanr(values1, values2, axis=None)
	assert abs(rho[0]) < 0.5
	print("rho = %s" % rho[0])
	print("\tNot signifying correlation found")

def white4D_functional():
	print("Testing correlation for 4D white noise")
	N = 20
	x1 = randrange(-1000, 1000, 1)
	y1 = randrange(-1000, 1000, 1)
	z1 = randrange(-1000, 1000, 1)
	w1 = randrange(-1000, 1000, 1)
	x2 = x1 + randrange(-1000, 1000, 1)
	y2 = y1 + randrange(-1000, 1000, 1)
	z2 = z1 + randrange(-1000, 1000, 1)
	w2 = w1 + randrange(-1000, 1000, 1)
	values1 = [[[[combined(white, x / N, y / N) for x in range(x1, x1 + N)] for y in range(y1, y1 + N)] for z in range(z1, z1 + N)] for w in range(w1, w1 + N)]
	values2 = [[[[combined(white, x / N, y / N) for x in range(x2, x2 + N)] for y in range(y2, y2 + N)] for z in range(z2, z2 + N)] for w in range(w2, w2 + N)]
	rho = spearmanr(values1, values2, axis=None)
	assert abs(rho[0]) < 0.5
	print("rho = %s" % rho[0])
	print("\tNot signifying correlation found")

def white2D_performance():
	print("Testing time to fill a 200x200 array with default parameters")
	base = time()
	N = 200
	pmap = [[combined(white, x / N, y / N) for x in range(N)] for y in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 0.5

def white2D_performance2():
	print("Testing time to fill a 70x70 array with 15 octaves")
	base = time()
	N = 70
	pmap = [[combined(white, x / N, y / N, octaves=50) for x in range(N)] for y in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def white3D_performance():
	print("Testing time to fill a 30x30x30 array with default parameters")
	base = time()
	N = 30
	pmap = [[[combined(white, x / N, y / N, z / N) for x in range(N)] for y in range(N)] for z in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1

def white4D_performance():
	print("Testing time to fill a 10x10x10x10 array with default parameters")
	base = time()
	N = 10
	pmap = [[[[combined(white, x / N, y / N, z / N, w / N) for x in range(N)] for y in range(N)] for z in range(N)] for w in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.5

def white2D_subjective():
	print("Displaying 2D white output")
	N = 100
	pmap = [[combined(white, x / N, y / N) for x in range(N)] for y in range(N)]

	plt.subplot(221)
	plt.title("6 octaves")
	plt.imshow(pmap, cmap='plasma', interpolation='nearest')

	plt.subplot(222)
	plt.title("1 octave")
	pmap = [[combined(white, 6 * x / N, 6 * y / N, octaves=1) for x in range(N)] for y in range(N)]
	plt.imshow(pmap, cmap='plasma', interpolation='nearest')

	plt.subplot(223)
	plt.title("4 octaves, marbled")
	mpmap = [[sin(1.6 * 2 * pi * combined(white, 6 * x / N, 6 * y / N, octaves=4)) for x in range(N)] for y in range(N)]
	plt.imshow(mpmap, cmap='plasma', interpolation='nearest')

	plt.subplot(224)
	plt.title("15 octaves, crinkled")
	cpmap = [[combined(white, 10 * x / N, 10 * y / N, octaves=15) for x in range(N)] for y in range(N)]
	plt.imshow(cpmap, cmap='plasma', interpolation='nearest')

	plt.show()

white2D_functional()
white3D_functional()
white4D_functional()
white2D_performance()
white2D_performance2()
white3D_performance()
white4D_performance()
white2D_subjective()