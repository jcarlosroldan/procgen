from os import chdir
chdir("../..")

from procgen.noise import opensimplex2D, opensimplex3D, opensimplex4D, combined
import matplotlib.pyplot as plt
from random import randint, random
from time import time
from math import sin, pi

def opensimplex2D_functional():
	print("Testing octave known values from original Java OpenSimplex 2D")
	assert opensimplex2D(.5, .5) == 0.2693285536052808, "Midpoint values don't match"
	assert opensimplex2D(.01, .0001) == 0.017085976025220266, "Small values don't match"
	assert opensimplex2D(1000.7, 1000.5) == -0.10185548597257466, "Big values don't match"
	assert opensimplex2D(18, 27) == -0.20056969610219666, "Integer values don't match"
	assert opensimplex2D(-12.3, -4.56) == -0.39668813509262996, "Negative values don't match"
	print("\tAll values working properly")

def opensimplex3D_functional():
	print("Testing octave known values from original Java OpenSimplex 3D")
	assert opensimplex3D(.5, .5, .5) == -0.3555445995145634, "Midpoint values don't match"
	assert opensimplex3D(.0001, .001, .01) == -0.005761907273547035, "Small values don't match"
	assert opensimplex3D(1000.7, 1000.5, 1000.3) == -0.39421579873144946, "Big values don't match"
	assert opensimplex3D(18, 27, 31) == -0.231411562587398, "Integer values don't match"
	assert opensimplex3D(-12.3, -4.56, -.789) == 0.14991986672314964, "Negative values don't match"
	print("\tAll values working properly")

def opensimplex4D_functional():
	print("Testing octave known values from original Java OpenSimplex 4D")
	assert opensimplex4D(.5, .5, .5, .5) == 0.2853462173341185, "Midpoint values don't match"
	assert opensimplex4D(.0001, .001, .01, .1) == 0.057808284276409806, "Small values don't match"
	assert opensimplex4D(1000.7, 1000.5, 1000.3, 1000.1) == -0.02126810949214044, "Big values don't match"
	assert opensimplex4D(18, 27, 31, 501) == -0.03761175258869856, "Integer values don't match"
	assert opensimplex4D(-12.3, -4.56, -.789, .818) == -0.32345225144839684, "Negative values don't match"
	print("\tAll values working properly")

def opensimplex2D_performance():
	print("Testing time to fill a 200x200 array with default parameters")
	base = time()
	N = 200
	pmap = [[combined(opensimplex2D, x/N, y/N) for x in range(N)] for y in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def opensimplex2D_performance2():
	print("Testing time to fill a 70x70 array with 15 octaves")
	base = time()
	N = 70
	pmap = [[combined(opensimplex2D, x/N, y/N, octaves = 50) for x in range(N)] for y in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def opensimplex3D_performance():
	print("Testing time to fill a 30x30x30 array with default parameters")
	base = time()
	N = 30
	pmap = [[[combined(opensimplex3D, x/N, y/N, z/N) for x in range(N)] for y in range(N)] for z in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 2.5

def opensimplex4D_performance():
	print("Testing time to fill a 10x10x10x10 array with default parameters")
	base = time()
	N = 10
	pmap = [[[[combined(opensimplex4D, x/N, y/N, z/N, w/N) for x in range(N)] for y in range(N)] for z in range(N)] for w in range(N)]
	elapsed = time() - base
	print("\tElapsed %s seconds" % elapsed)
	assert elapsed < 1.8

def opensimplex2D_subjective():
	print("Displaying 2D opensimplex output")
	N = 100
	pmap = [[combined(opensimplex2D, x/N, y/N) for x in range(N)] for y in range(N)]
	
	plt.subplot(221)
	plt.title("6 octaves")
	plt.imshow(pmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(222)
	plt.title("1 octave")
	pmap = [[combined(opensimplex2D, 6*x/N, 6*y/N, octaves = 1) for x in range(N)] for y in range(N)]
	plt.imshow(pmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(223)
	plt.title("4 octaves, marbled")
	mpmap = [[sin(1.6 * 2 * pi * combined(opensimplex2D, 6*x/N, 6*y/N, octaves = 4)) for x in range(N)] for y in range(N)]
	plt.imshow(mpmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.subplot(224)
	plt.title("15 octaves, crinkled")
	cpmap = [[combined(opensimplex2D, 10*x/N, 10*y/N, octaves = 15) for x in range(N)] for y in range(N)]
	plt.imshow(cpmap, cmap = 'plasma', interpolation = 'nearest')
	
	plt.show()

opensimplex2D_functional()
opensimplex3D_functional()
opensimplex4D_functional()
opensimplex2D_performance()
opensimplex2D_performance2()
opensimplex3D_performance()
opensimplex4D_performance()
opensimplex2D_subjective()