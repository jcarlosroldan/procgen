# PERLIN ----------------------------------------------------------------------

def perlin(x, y, z, octaves = 6, persistence = .5, lacunarity = 2):
	""" Generate 3-D perlin noise. """
	total = 0
	freq = 1
	amplitude = 1
	max_val = 0
	for i in range(octaves):
		total += _perlin_octave_noise(x * freq, y * freq, z * freq) * amplitude
		max_val += amplitude
		amplitude *= persistence
		freq *= lacunarity
	return total / max_val

_perlin_p = 2 * [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

def _perlin_fade(t):
	""" Optimised fade function: 6*t**5 - 15*t**4 + 10*t**3 """
	return t * t * t * (t * (t * 6 - 15) + 10)

def _perlin_lerp(t, a, b):
	""" Linear interpolation """
	return a + t * (b - a)

def _perlin_grad(hash, x, y, z):
	""" Convert lo 4 bits of hash code into 12 gradient directions. """
	h = hash & 0xF
	u = x if h < 8 else y
	v = y if h < 4 else (x if h == 12 or h == 14 else z)
	return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v)

def _perlin_octave_noise(x, y, z):
	""" Taken from Improving Noise by Ken Perlin, SIGGRAPH 2002 """
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
	A = _perlin_p[X] + Y
	AA = _perlin_p[A] + Z
	AB = _perlin_p[A + 1] + Z
	B = _perlin_p[X + 1] + Y
	BA = _perlin_p[B] + Z
	BB = _perlin_p[B + 1] +Z
	# add blended results from 8 corners of cube
	return _perlin_lerp(
		w,
		_perlin_lerp(
			v,
			_perlin_lerp(
				u,
				_perlin_grad(_perlin_p[AA], x, y, z),
				_perlin_grad(_perlin_p[BA], x - 1, y, z)
			),
			_perlin_lerp(
				u,
				_perlin_grad(_perlin_p[AB], x, y - 1, z),
				_perlin_grad(_perlin_p[BB], x - 1, y - 1, z)
			)
		),
		_perlin_lerp(
			v,
			_perlin_lerp(
				u,
				_perlin_grad(_perlin_p[AA + 1], x, y, z - 1),
				_perlin_grad(_perlin_p[BA + 1], x - 1, y, z - 1)
			),
			_perlin_lerp(
				u,
				_perlin_grad(_perlin_p[AB + 1], x, y - 1, z - 1),
				_perlin_grad(_perlin_p[BB + 1], x - 1, y - 1, z - 1)
			)
		)
	)

# SIMPLEX ---------------------------------------------------------------------

def simplex(xin,yin,zin):
	""" Generate 3-D simplex noise. A Python version of the Stefan Gustavson 2012 JAVA implementation."""
	grad3 = [[1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0],
			[1,0,1],[-1,0,1],[1,0,-1],[-1,0,-1],
			[0,1,1],[0,-1,1],[0,1,-1],[0,-1,-1]]
	p = [151,160,137,91,90,15,
		131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
		190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
		88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
		77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
		102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
		135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
		5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
		223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
		129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
		251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
		49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
		138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]
	perm = []
	permMod12 = []
	for i in range(512):
		perm.append(p[i & 255])
		permMod12.append(int((perm[i] % 12)))
	F3 = 1.0/3.0
	G3 = 1.0/6.0
	s = (xin+yin+zin)*F3
	i = _fast_floor(xin+s)
	j = _fast_floor(yin+s)
	k = _fast_floor(zin+s)
	t = (i+j+k)*G3
	#Unskew the cell origin back to (x,y,z) space
	X0 = i-t 
	Y0 = j-t
	Z0 = k-t
	#The x,y,z distances from the cell origin
	x0 = xin-X0 
	y0 = yin-Y0
	z0 = zin-Z0
	#For the 3D case, the simplex shape is a slightly irregular tetrahedron.
    #Determine which simplex we are in.
	if x0>=y0:
		if y0>=z0:
			# X Y Z order
			i1,j1,k1,i2,j2,k2 = 1,0,0,1,1,0
		elif x0>=z0:
			# X Z Y order
			i1,j1,k1,i2,j2,k2 = 1,0,0,1,0,1
		else:
			#Z X Y order
			i1,j1,k1,i2,j2,k2 = 0,0,1,1,0,1
	else:
		#x0<y0
		if y0<z0:
			# X Y Z order
			i1,j1,k1,i2,j2,k2 = 0,0,1,0,1,1
		elif x0<z0:
			# X Y Z order
			i1,j1,k1,i2,j2,k2 = 0,1,0,0,1,1
		else:
			# X Y Z order
			i1,j1,k1,i2,j2,k2 = 0,1,0,1,1,0
	"""A step of (1,0,0) in (i,j,k) means a step of (1-c,-c,-c) in (x,y,z),
	a step of (0,1,0) in (i,j,k) means a step of (-c,1-c,-c) in (x,y,z), and
	a step of (0,0,1) in (i,j,k) means a step of (-c,-c,1-c) in (x,y,z), where
	c = 1/6."""
	#Offsets for second corner in (x,y,z) coords
	x1 = x0 - i1 + G3
	y1 = y0 - j1 + G3
	z1 = z0 - k1 + G3
	#Offsets for third corner in (x,y,z) coords
	x2 = x0 - i2 + 2.0*G3
	y2 = y0 - j2 + 2.0*G3
	z2 = z0 - k2 + 2.0*G3
	#Offsets for last corner in (x,y,z) coords
	x3 = x0 - 1.0 + 3.0*G3
	y3 = y0 - 1.0 + 3.0*G3
	z3 = z0 - 1.0 + 3.0*G3
	#Work out the hashed gradient indices of the four simplex corners
	ii = i & 255
	jj = j & 255
	kk = k & 255
	gi0 = permMod12[ii+perm[jj+perm[kk]]]
	gi1 = permMod12[ii+i1+perm[jj+j1+perm[kk+k1]]]
	gi2 = permMod12[ii+i2+perm[jj+j2+perm[kk+k2]]]
	gi3 = permMod12[ii+1+perm[jj+1+perm[kk+1]]]
	#Calculate the contribution from the four corners

	t0 = 0.6 - x0*x0 - y0*y0 - z0*z0
	if t0<0:
		n0 = 0.0
	else:
		t0 *= t0
		n0 = t0 * t0 * _dot(grad3[gi0], x0, y0, z0)
	t1 = 0.6 - x1*x1 - y1*y1 - z1*z1
	if t1<0: 
		n1 = 0.0
	else:
		t1 *= t1
		n1 = t1 * t1 * _dot(grad3[gi1], x1, y1, z1)
	t2 = 0.6 - x2*x2 - y2*y2 - z2*z2
	if t2<0:
		n2 = 0.0
	else:
		t2 *= t2
		n2 = t2 * t2 * _dot(grad3[gi2], x2, y2, z2)
	t3 = 0.6 - x3*x3 - y3*y3 - z3*z3
	if t3<0:
		n3 = 0.0
	else:
		t3 *= t3
		n3 = t3 * t3 * _dot(grad3[gi3], x3, y3, z3)
	"""Add contributions from each corner to get the final noise value.
	The result is scaled to stay just inside [-1,1]"""
	return 32.0*(n0 + n1 + n2 + n3)

def _fast_floor(x):
	xi = int(x)
	if(x<xi):
		return xi-1
	else:
		return xi

def _dot(g,x,y,z):
	return g[0]*x + g[1]*y + g[2]*z

# OPENSIMPLEX -----------------------------------------------------------------

# WAVELET ---------------------------------------------------------------------

# VORONOI ---------------------------------------------------------------------

# WORLEY ----------------------------------------------------------------------

# BILLOW ----------------------------------------------------------------------

# RIDGED ----------------------------------------------------------------------
