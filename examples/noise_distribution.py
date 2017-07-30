from os import chdir
chdir("..")

from random import random

REPETITIONS = 10**6
RANGE = 10**8

from procgen.noise import perlin1D, perlin2D, perlin3D, perlin4D, simplex2D, simplex3D, opensimplex2D, opensimplex3D, opensimplex4D

to_test = [
	[perlin1D],
	[perlin2D, simplex2D, opensimplex2D],
	[perlin3D, simplex3D, opensimplex3D],
	[perlin4D, opensimplex4D]
]

print("   NAME         MIN        MAX         AVG")
print("_expected_     -1          1           0")
for n, methods in enumerate(to_test):
	for method in methods:
		res = [method(*[random()*RANGE - RANGE/2 for _ in range(n + 1)]) for _ in range(REPETITIONS)]
		avg = sum(res)/REPETITIONS
		print("%-14s %.8f %.8f %s%.8f" % (method.__name__, min(res), max(res), " " if not avg < 0 else "", avg))