"""
We will use requests and scrapy as a reference for our structure and workflow:

https://github.com/requests/requests/blob/master/tests/test_requests.py
https://github.com/scrapy/scrapy/blob/master/tests/test_crawl.py
"""
_perlin_p = 2 * [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

_perlin_fade = lambda t: t * t * t * (t * (t * 6 - 15) + 10) # 6*t**5 - 15*t**4 + 10*t**3

_perlin_lerp = lambda t, a, b: a + t * (b - a)

def _perlin_grad(hash, x, y, z):
	# convert lo 4 bits of hash code into 12 gradient directions.
	h = hash & 0xF
	u = x if h<8 else y
	v = y if h<4 else (x if h==12 or h==14 else z)
	return (u if h&1 == 0 else -u) + (v if h&2 == 0 else -v)

def _perlin_octave_noise(x, y, z):
	# Taken from Improving Noise by Ken Perlin, SIGGRAPH 2002
	# find unit cube that contains point
	X = int(x) & 255
	Y = int(y) & 255
	Z = int(z) & 255
	# find relative x, y, z of each point in cube
	x = x % 1
	y = y % 1
	z = z % 1
	# compute fade curves for each of x, y, z
	u = _perlin_fade(x)
	v = _perlin_fade(y)
	w = _perlin_fade(z)
	# hash coordinates of the 8 cube corners
	A = _perlin_p[X  ]+Y
	AA = _perlin_p[A]+Z
	AB = _perlin_p[A+1]+Z
	B = _perlin_p[X+1]+Y
	BA = _perlin_p[B]+Z
	BB = _perlin_p[B+1]+Z
	# add blended results from 8 corners of cube
	return _perlin_lerp(w, _perlin_lerp(v, _perlin_lerp(u, _perlin_grad(_perlin_p[AA  ], x  , y  , z   ),
								 _perlin_grad(_perlin_p[BA  ], x-1, y  , z   )),
						 _perlin_lerp(u, _perlin_grad(_perlin_p[AB  ], x  , y-1, z   ),
								 _perlin_grad(_perlin_p[BB  ], x-1, y-1, z   ))),
				 _perlin_lerp(v, _perlin_lerp(u, _perlin_grad(_perlin_p[AA+1], x  , y  , z-1 ),
								 _perlin_grad(_perlin_p[BA+1], x-1, y  , z-1 )),
						 _perlin_lerp(u, _perlin_grad(_perlin_p[AB+1], x  , y-1, z-1 ),
								 _perlin_grad(_perlin_p[BB+1], x-1, y-1, z-1 ))))

def perlin(x, y, z, octaves = 6, persistence = 0.5, lacunarity = 2):
	total = 0
	freq = 1
	amplitude = 1
	max_val = 0
	for i in range(octaves):
		total += _perlin_octave_noise(x*freq, y*freq, z*freq) * amplitude
		max_val += amplitude
		amplitude *= persistence
		freq *= lacunarity
	return total / max_val

print(_perlin_octave_noise(0.23, 0.12, 0.16))
print(_perlin_octave_noise(0.23, 1000.13, 0.16))