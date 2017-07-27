# GLOBAL ----------------------------------------------------------------------

def combined(noise_function, x, y, z = None, w = None, octaves = 6, persistence = .5, lacunarity = 2):
	""" Generate noise by combining multiple frequencies of the same noise
	DISCLAIMER: This is a temporary solution, octaves, persistence and lacunarity will be noise function parameters in the future. """
	total = 0
	freq = 1
	amplitude = 1
	max_val = 0
	for i in range(octaves):
		if w == None:
			if z == None:
				total += noise_function(x * freq, y * freq) * amplitude
			else:
				total += noise_function(x * freq, y * freq, z * freq) * amplitude
		else:
			total += noise_function(x * freq, y * freq, z * freq, w * freq) * amplitude
		max_val += amplitude
		amplitude *= persistence
		freq *= lacunarity
	return total / max_val

# PERLIN ----------------------------------------------------------------------

from math import floor

def perlin2D(x, y):
	""" Generate 2D perlin noise.
	Taken from Improving Noise by Ken Perlin, SIGGRAPH 2002. """
	X = floor(x) & 0xFF
	Y = floor(y) & 0xFF
	
	x = x % 1
	y = y % 1
	
	u = _perlin_fade(x)
	v = _perlin_fade(y)
	
	A = _perlin_p[X] + Y
	B = _perlin_p[X + 1] + Y
	
	return _perlin_lerp(
			v,
			_perlin_lerp(
				u,
				_perlin_grad2D(_perlin_p[_perlin_p[A]], x, y),
				_perlin_grad2D(_perlin_p[_perlin_p[B]], x - 1, y)
			),
			_perlin_lerp(
				u,
				_perlin_grad2D(_perlin_p[_perlin_p[A + 1]], x, y - 1),
				_perlin_grad2D(_perlin_p[_perlin_p[B + 1]], x - 1, y - 1)
			)
		)

def perlin3D(x, y, z):
	""" Generate 3D perlin noise.
	Taken from Improving Noise by Ken Perlin, SIGGRAPH 2002. """
	X = floor(x) & 0xFF
	Y = floor(y) & 0xFF
	Z = floor(z) & 0xFF
	
	x = x % 1
	y = y % 1
	z = z % 1
	
	u = _perlin_fade(x)
	v = _perlin_fade(y)
	w = _perlin_fade(z)
	
	A = _perlin_p[X] + Y
	AA = _perlin_p[A] + Z
	AB = _perlin_p[A + 1] + Z
	B = _perlin_p[X + 1] + Y
	BA = _perlin_p[B] + Z
	BB = _perlin_p[B + 1] +Z
	
	return _perlin_lerp(
		w,
		_perlin_lerp(
			v,
			_perlin_lerp(
				u,
				_perlin_grad3D(_perlin_p[AA], x, y, z),
				_perlin_grad3D(_perlin_p[BA], x - 1, y, z)
			),
			_perlin_lerp(
				u,
				_perlin_grad3D(_perlin_p[AB], x, y - 1, z),
				_perlin_grad3D(_perlin_p[BB], x - 1, y - 1, z)
			)
		),
		_perlin_lerp(
			v,
			_perlin_lerp(
				u,
				_perlin_grad3D(_perlin_p[AA + 1], x, y, z - 1),
				_perlin_grad3D(_perlin_p[BA + 1], x - 1, y, z - 1)
			),
			_perlin_lerp(
				u,
				_perlin_grad3D(_perlin_p[AB + 1], x, y - 1, z - 1),
				_perlin_grad3D(_perlin_p[BB + 1], x - 1, y - 1, z - 1)
			)
		)
	)

_perlin_p = 2 * [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

def _perlin_fade(t):
	""" Optimised fade function: 6*t**5 - 15*t**4 + 10*t**3 """
	return t * t * t * (t * (t * 6 - 15) + 10)

def _perlin_lerp(t, a, b):
	""" Linear interpolation """
	return a + t * (b - a)

def _perlin_grad2D(hash, x, y):
	""" Convert lo 4 bits of hash code into 12 gradient directions """
	h = hash & 0xF
	u = x if h < 0b1000 else y
	v = y if h < 0b100 else (x if h == 0b1100 or h == 0b1110 else 0)
	return (u if h & 0b1 == 0 else -u) + (v if h & 0b10 == 0 else -v)

def _perlin_grad3D(hash, x, y, z):
	""" Convert lo 4 bits of hash code into 12 gradient directions """
	h = hash & 0xF
	u = x if h < 0b1000 else y
	v = y if h < 0b100 else (x if h == 0b1100 or h == 0b1110 else z)
	return (u if h & 0b1 == 0 else -u) + (v if h & 0b10 == 0 else -v)

# SIMPLEX ---------------------------------------------------------------------

from math import floor

def simplex2D(x, y):
	""" Generate 2D simplex noise
	Taken from Stefan Gustavson 2012 Java implementation. """
	s = (x + y) * _simplex_F2
	i = floor(x + s)
	j = floor(y + s)
	t = (i + j) * _simplex_G2
	# unskew the cell origin back to (x,y) space
	X0 = i - t
	Y0 = j - t
	# the x,y distances from the cell origin
	x0 = x - X0
	y0 = y - Y0
	# for the 2D case, the simplex shape is an equilateral triangle.
	# determine which simplex we are in.
	if x0 > y0:
		# lower triangle, XY order: (0,0)->(1,0)->(1,1)
		i1, j1 = 1, 0
	else:
		# upper triangle, YX order: (0,0)->(0,1)->(1,1)
		i1, j1 = 0, 1

	# offsets for middle corner in (x,y) unskewed coords
	x1 = x0 - i1 + _simplex_G2
	y1 = y0 - j1 + _simplex_G2
	# offsets for last corner in (x,y) unskewed coords
	x2 = x0 - 1.0 + 2 * _simplex_G2
	y2 = y0 - 1.0 + 2 * _simplex_G2
	# work out the hashed gradient indices of the three simplex corners
	ii = i & 255
	jj = j & 255
	gi0 = _simplex_perm_mod12[ii + _simplex_perm[jj]]
	gi1 = _simplex_perm_mod12[ii + i1 + _simplex_perm[jj + j1]]
	gi2 = _simplex_perm_mod12[ii + 1 + _simplex_perm[jj + 1]]
	# calculate the contribution from the three corners
	t0 = 0.5 - x0**2 - y0**2
	if t0 < 0:
		n0 = 0
	else:
		t0 *= t0
		n0 = t0 * t0 * _simplex_dot2D(_simplex_grad3[gi0], x0, y0)
	t1 = 0.5 - x1**2 - y1**2
	if t1 < 0:
		n1 = 0
	else:
		t1 *= t1
		n1 = t1**2 * _simplex_dot2D(_simplex_grad3[gi1], x1, y1)
	t2 = 0.5 - x2**2 - y2**2
	if t2 < 0:
		n2 = 0
	else:
		t2 *= t2
		n2 = t2 * t2 * _simplex_dot2D(_simplex_grad3[gi2], x2, y2)
	return 70 * (n0 + n1 + n2)

def simplex3D(x, y, z):
	""" Generate 3D simplex noise
	Taken from Stefan Gustavson 2012 Java implementation. """	
	s = (x + y + z) / 3
	i = floor(x + s)
	j = floor(y + s)
	k = floor(z + s)
	t = (i + j + k) * _simplex_G3
	# unskew the cell origin back to (x,y,z) space
	X0 = i - t
	Y0 = j - t
	Z0 = k - t
	# the x,y,z distances from the cell origin
	x0 = x - X0
	y0 = y - Y0
	z0 = z - Z0
	# for the 3D case, the simplex shape is a slightly irregular tetrahedron.
    # determine which simplex we are in.
	if x0 >= y0:
		if y0 >= z0:
			# X Y Z order
			i1, j1, k1, i2, j2, k2 = 1, 0, 0, 1, 1, 0
		elif x0 >= z0:
			# X Z Y order
			i1, j1, k1, i2, j2, k2 = 1, 0, 0, 1, 0, 1
		else:
			#Z X Y order
			i1, j1, k1, i2, j2, k2 = 0, 0, 1, 1, 0, 1
	else:
		if y0 < z0:
			# X Y Z order
			i1, j1, k1, i2, j2, k2 = 0, 0, 1, 0, 1, 1
		elif x0 < z0:
			# X Y Z order
			i1, j1, k1, i2, j2, k2 = 0, 1, 0, 0, 1, 1
		else:
			# X Y Z order
			i1, j1, k1, i2, j2, k2 = 0, 1, 0, 1, 1, 0
	# offsets for second corner in (x,y,z) coords
	x1 = x0 - i1 + _simplex_G3
	y1 = y0 - j1 + _simplex_G3
	z1 = z0 - k1 + _simplex_G3
	# offsets for third corner in (x,y,z) coords
	x2 = x0 - i2 + 2 * _simplex_G3
	y2 = y0 - j2 + 2 * _simplex_G3
	z2 = z0 - k2 + 2 * _simplex_G3
	# offsets for last corner in (x,y,z) coords
	x3 = x0 - 1 + 3 * _simplex_G3
	y3 = y0 - 1 + 3 * _simplex_G3
	z3 = z0 - 1 + 3 * _simplex_G3
	# work out the hashed gradient indices of the four simplex corners
	ii = i & 255
	jj = j & 255
	kk = k & 255
	gi0 = _simplex_perm_mod12[ii + _simplex_perm[jj + _simplex_perm[kk]]]
	gi1 = _simplex_perm_mod12[ii + i1 + _simplex_perm[jj + j1 + _simplex_perm[kk + k1]]]
	gi2 = _simplex_perm_mod12[ii + i2 + _simplex_perm[jj + j2 + _simplex_perm[kk + k2]]]
	gi3 = _simplex_perm_mod12[ii + 1 + _simplex_perm[jj + 1 + _simplex_perm[kk + 1]]]
	# calculate the contribution from the four corners
	t0 = 0.6 - x0**2 - y0**2 - z0**2
	if t0 < 0:
		n0 = 0
	else:
		t0 *= t0
		n0 = t0 * t0 * _simplex_dot3D(_simplex_grad3[gi0], x0, y0, z0)
	t1 = 0.6 - x1**2 - y1**2 - z1**2
	if t1 < 0:
		n1 = 0
	else:
		t1 *= t1
		n1 = t1 * t1 * _simplex_dot3D(_simplex_grad3[gi1], x1, y1, z1)
	t2 = 0.6 - x2**2 - y2**2 - z2**2
	if t2 < 0:
		n2 = 0
	else:
		t2 *= t2
		n2 = t2 * t2 * _simplex_dot3D(_simplex_grad3[gi2], x2, y2, z2)
	t3 = 0.6 - x3**2 - y3**2 - z3**2
	if t3 < 0:
		n3 = 0
	else:
		t3 *= t3
		n3 = t3 * t3 * _simplex_dot3D(_simplex_grad3[gi3], x3, y3, z3)
	return 32 * (n0 + n1 + n2 + n3)

_simplex_grad3 = [[1,1,0], [-1,1,0], [1,-1,0], [-1,-1,0], [1,0,1], [-1,0,1], [1,0,-1], [-1,0,-1], [0,1,1], [0,-1,1], [0,1,-1], [0,-1,-1]]
_simplex_grad4 = [[0,1,1,1], [0,1,1,-1], [0,1,-1,1], [0,1,-1,-1], [0,-1,1,1], [0,-1,1,-1], [0,-1,-1,1], [0,-1,-1,-1], [1,0,1,1], [1,0,1,-1], [1,0,-1,1], [1,0,-1,-1], [-1,0,1,1], [-1,0,1,-1], [-1,0,-1,1], [-1,0,-1,-1], [1,1,0,1], [1,1,0,-1], [1,-1,0,1], [1,-1,0,-1], [-1,1,0,1], [-1,1,0,-1], [-1,-1,0,1], [-1,-1,0,-1], [1,1,1,0], [1,1,-1,0], [1,-1,1,0], [1,-1,-1,0], [-1,1,1,0], [-1,1,-1,0], [-1,-1,1,0], [-1,-1,-1,0]]
_simplex_perm = 2 * [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]
_simplex_perm_mod12 = 2 * [7,4,5,7,6,3,11,1,9,11,0,5,2,5,7,9,8,0,7,6,9,10,8,3,1,0,9,10,11,10,6,4,7,0,6,3,0,2,5,2,10,0,3,11,9,11,11,8,9,9,9,4,9,5,8,3,6,8,5,4,3,0,8,7,2,9,11,2,7,0,3,10,5,2,2,3,11,3,1,2,0,7,1,2,4,9,8,5,7,10,5,4,4,6,11,6,5,1,3,5,1,0,8,1,5,4,0,7,4,5,6,1,8,4,3,10,8,8,3,2,8,4,1,6,5,6,3,4,4,1,10,10,4,3,5,10,2,3,10,6,3,10,1,8,3,2,11,11,11,4,10,5,2,9,4,6,7,3,2,9,11,8,8,2,8,10,7,10,5,9,5,11,11,7,4,9,9,10,3,1,7,2,0,2,7,5,8,4,10,5,4,8,2,6,1,0,11,10,2,1,10,6,0,0,11,11,6,1,9,3,1,7,9,2,11,11,1,0,10,7,1,7,10,1,4,0,0,8,7,1,2,9,7,4,6,2,6,8,1,9,6,6,7,5,0,0,3,9,8,3,6,6,11,1,0,0]
_simplex_F2 = 0.3660254037844386
_simplex_G2 = 0.21132486540518713
_simplex_G3 = 0.16666666666666666
_simplex_F4 = 0.30901699437494745
_simplex_G4 = 0.1381966011250105

def _simplex_dot2D(g, x, y):
	""" 2D dot product """
	return g[0] * x + g[1] * y

def _simplex_dot3D(g, x, y, z):
	""" 3D dot product """
	return g[0] * x + g[1] * y + g[2] * z

# OPENSIMPLEX -----------------------------------------------------------------

def opensimplex2D(x, y):
	""" Generate 2D OpenSimplex noise
	Taken from Kurt Spencer Java implementation. """
	stretchOffset = (x + y) * -0.211324865405187
	xs = x + stretchOffset
	ys = y + stretchOffset
	
	xsb = floor(xs)
	ysb = floor(ys)
	
	squishOffset = (xsb + ysb) * _opensimplex_squish2D
	xb = xsb + squishOffset
	yb = ysb + squishOffset
	
	xins = xs - xsb
	yins = ys - ysb
	
	inSum = xins + yins

	dx0 = x - xb
	dy0 = y - yb
	
	value = 0

	dx1 = dx0 - 1 - _opensimplex_squish2D
	dy1 = dy0 - 0 - _opensimplex_squish2D
	attn1 = 2 - dx1 * dx1 - dy1 * dy1
	if attn1 > 0:
		attn1 *= attn1
		value += attn1 * attn1 * _opensimplex_extrapolate2D(xsb + 1, ysb + 0, dx1, dy1)

	dx2 = dx0 - 0 - _opensimplex_squish2D
	dy2 = dy0 - 1 - _opensimplex_squish2D
	attn2 = 2 - dx2 * dx2 - dy2 * dy2
	if attn2 > 0:
		attn2 *= attn2
		value += attn2 * attn2 * _opensimplex_extrapolate2D(xsb + 0, ysb + 1, dx2, dy2)
	
	if inSum <= 1:
		zins = 1 - inSum
		if zins > xins or zins > yins:
			if xins > yins:
				xsv_ext = xsb + 1
				ysv_ext = ysb - 1
				dx_ext = dx0 - 1
				dy_ext = dy0 + 1
			else:
				xsv_ext = xsb - 1
				ysv_ext = ysb + 1
				dx_ext = dx0 + 1
				dy_ext = dy0 - 1
		else:
			xsv_ext = xsb + 1
			ysv_ext = ysb + 1
			dx_ext = dx0 - 1 - 2 * _opensimplex_squish2D
			dy_ext = dy0 - 1 - 2 * _opensimplex_squish2D
	else:
		zins = 2 - inSum
		if zins < xins or zins < yins:
			if xins > yins:
				xsv_ext = xsb + 2
				ysv_ext = ysb + 0
				dx_ext = dx0 - 2 - 2 * _opensimplex_squish2D
				dy_ext = dy0 + 0 - 2 * _opensimplex_squish2D
			else:
				xsv_ext = xsb + 0
				ysv_ext = ysb + 2
				dx_ext = dx0 + 0 - 2 * _opensimplex_squish2D
				dy_ext = dy0 - 2 - 2 * _opensimplex_squish2D
		else:
			dx_ext = dx0
			dy_ext = dy0
			xsv_ext = xsb
			ysv_ext = ysb
		xsb += 1
		ysb += 1
		dx0 = dx0 - 1 - 2 * _opensimplex_squish2D
		dy0 = dy0 - 1 - 2 * _opensimplex_squish2D
	
	attn0 = 2 - dx0 * dx0 - dy0 * dy0
	if (attn0 > 0):
		attn0 *= attn0
		value += attn0 * attn0 * _opensimplex_extrapolate2D(xsb, ysb, dx0, dy0)

	attn_ext = 2 - dx_ext * dx_ext - dy_ext * dy_ext
	if (attn_ext > 0):
		attn_ext *= attn_ext
		value += attn_ext * attn_ext * _opensimplex_extrapolate2D(xsv_ext, ysv_ext, dx_ext, dy_ext)
	
	return value / 47

def opensimplex3D(x, y, z):
	""" Generate 3D OpenSimplex noise
	Taken from Kurt Spencer Java implementation. """
	stretchOffset = (x + y + z) * -1.0 / 6
	xs = x + stretchOffset
	ys = y + stretchOffset
	zs = z + stretchOffset
	
	xsb = floor(xs)
	ysb = floor(ys)
	zsb = floor(zs)
	
	squishOffset = (xsb + ysb + zsb) * _opensimplex_squish3D
	xb = xsb + squishOffset
	yb = ysb + squishOffset
	zb = zsb + squishOffset
	
	xins = xs - xsb
	yins = ys - ysb
	zins = zs - zsb
	
	inSum = xins + yins + zins

	dx0 = x - xb
	dy0 = y - yb
	dz0 = z - zb
	
	value = 0

	if (inSum <= 1):
		aPoint = 0x01
		aScore = xins
		bPoint = 0x02
		bScore = yins
		if aScore >= bScore and zins > bScore:
			bScore = zins
			bPoint = 0x04
		elif aScore < bScore and zins > aScore:
			aScore = zins
			aPoint = 0x04
		
		wins = 1 - inSum
		if wins > aScore or wins > bScore:
			c = bPoint if bScore > aScore else aPoint
			
			if (c & 0x01) == 0:
				xsv_ext0 = xsb - 1
				xsv_ext1 = xsb
				dx_ext0 = dx0 + 1
				dx_ext1 = dx0
			else:
				xsv_ext0 = xsv_ext1 = xsb + 1
				dx_ext0 = dx_ext1 = dx0 - 1

			if (c & 0x02) == 0:
				ysv_ext0 = ysv_ext1 = ysb
				dy_ext0 = dy_ext1 = dy0
				if (c & 0x01) == 0:
					ysv_ext1 -= 1
					dy_ext1 += 1
				else:
					ysv_ext0 -= 1
					dy_ext0 += 1
			else:
				ysv_ext0 = ysv_ext1 = ysb + 1
				dy_ext0 = dy_ext1 = dy0 - 1

			if (c & 0x04) == 0:
				zsv_ext0 = zsb
				zsv_ext1 = zsb - 1
				dz_ext0 = dz0
				dz_ext1 = dz0 + 1
			else:
				zsv_ext0 = zsv_ext1 = zsb + 1
				dz_ext0 = dz_ext1 = dz0 - 1
		else:
			c = (aPoint | bPoint) & 0xFF
			
			if (c & 0x01) == 0:
				xsv_ext0 = xsb
				xsv_ext1 = xsb - 1
				dx_ext0 = dx0 - 2 * _opensimplex_squish3D
				dx_ext1 = dx0 + 1 - _opensimplex_squish3D
			else:
				xsv_ext0 = xsv_ext1 = xsb + 1
				dx_ext0 = dx0 - 1 - 2 * _opensimplex_squish3D
				dx_ext1 = dx0 - 1 - _opensimplex_squish3D

			if (c & 0x02) == 0:
				ysv_ext0 = ysb
				ysv_ext1 = ysb - 1
				dy_ext0 = dy0 - 2 * _opensimplex_squish3D
				dy_ext1 = dy0 + 1 - _opensimplex_squish3D
			else:
				ysv_ext0 = ysv_ext1 = ysb + 1
				dy_ext0 = dy0 - 1 - 2 * _opensimplex_squish3D
				dy_ext1 = dy0 - 1 - _opensimplex_squish3D

			if (c & 0x04) == 0:
				zsv_ext0 = zsb
				zsv_ext1 = zsb - 1
				dz_ext0 = dz0 - 2 * _opensimplex_squish3D
				dz_ext1 = dz0 + 1 - _opensimplex_squish3D
			else:
				zsv_ext0 = zsv_ext1 = zsb + 1
				dz_ext0 = dz0 - 1 - 2 * _opensimplex_squish3D
				dz_ext1 = dz0 - 1 - _opensimplex_squish3D

		attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0
		if attn0 > 0:
			attn0 *= attn0
			value += attn0 * attn0 * _opensimplex_extrapolate3D(xsb + 0, ysb + 0, zsb + 0, dx0, dy0, dz0)

		dx1 = dx0 - 1 - _opensimplex_squish3D
		dy1 = dy0 - 0 - _opensimplex_squish3D
		dz1 = dz0 - 0 - _opensimplex_squish3D
		attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1
		if attn1 > 0:
			attn1 *= attn1
			value += attn1 * attn1 * _opensimplex_extrapolate3D(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1)

		
		dx2 = dx0 - 0 - _opensimplex_squish3D
		dy2 = dy0 - 1 - _opensimplex_squish3D
		dz2 = dz1
		attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2
		if attn2 > 0:
			attn2 *= attn2
			value += attn2 * attn2 * _opensimplex_extrapolate3D(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2)

		dx3 = dx2
		dy3 = dy1
		dz3 = dz0 - 1 - _opensimplex_squish3D
		attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3
		if attn3 > 0:
			attn3 *= attn3
			value += attn3 * attn3 * _opensimplex_extrapolate3D(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3)
	elif inSum >= 2:
	
		aPoint = 0x06
		aScore = xins
		bPoint = 0x05
		bScore = yins
		if aScore <= bScore and zins < bScore:
			bScore = zins
			bPoint = 0x03
		elif aScore > bScore and zins < aScore:
			aScore = zins
			aPoint = 0x03

		wins = 3 - inSum
		if wins < aScore or wins < bScore:
			c = bPoint if bScore < aScore else aPoint
			
			if (c & 0x01) != 0:
				xsv_ext0 = xsb + 2
				xsv_ext1 = xsb + 1
				dx_ext0 = dx0 - 2 - 3 * _opensimplex_squish3D
				dx_ext1 = dx0 - 1 - 3 * _opensimplex_squish3D
			else:
				xsv_ext0 = xsv_ext1 = xsb
				dx_ext0 = dx_ext1 = dx0 - 3 * _opensimplex_squish3D

			if (c & 0x02) != 0:
				ysv_ext0 = ysv_ext1 = ysb + 1
				dy_ext0 = dy_ext1 = dy0 - 1 - 3 * _opensimplex_squish3D
				if (c & 0x01) != 0:
					ysv_ext1 += 1
					dy_ext1 -= 1
				else:
					ysv_ext0 += 1
					dy_ext0 -= 1
			else:
				ysv_ext0 = ysv_ext1 = ysb
				dy_ext0 = dy_ext1 = dy0 - 3 * _opensimplex_squish3D

			if (c & 0x04) != 0:
				zsv_ext0 = zsb + 1
				zsv_ext1 = zsb + 2
				dz_ext0 = dz0 - 1 - 3 * _opensimplex_squish3D
				dz_ext1 = dz0 - 2 - 3 * _opensimplex_squish3D
			else:
				zsv_ext0 = zsv_ext1 = zsb
				dz_ext0 = dz_ext1 = dz0 - 3 * _opensimplex_squish3D
		else:
			c = (aPoint & bPoint) & 0xFF
			
			if (c & 0x01) != 0:
				xsv_ext0 = xsb + 1
				xsv_ext1 = xsb + 2
				dx_ext0 = dx0 - 1 - _opensimplex_squish3D
				dx_ext1 = dx0 - 2 - 2 * _opensimplex_squish3D
			else:
				xsv_ext0 = xsv_ext1 = xsb
				dx_ext0 = dx0 - _opensimplex_squish3D
				dx_ext1 = dx0 - 2 * _opensimplex_squish3D

			if (c & 0x02) != 0:
				ysv_ext0 = ysb + 1
				ysv_ext1 = ysb + 2
				dy_ext0 = dy0 - 1 - _opensimplex_squish3D
				dy_ext1 = dy0 - 2 - 2 * _opensimplex_squish3D
			else:
				ysv_ext0 = ysv_ext1 = ysb
				dy_ext0 = dy0 - _opensimplex_squish3D
				dy_ext1 = dy0 - 2 * _opensimplex_squish3D

			if (c & 0x04) != 0:
				zsv_ext0 = zsb + 1
				zsv_ext1 = zsb + 2
				dz_ext0 = dz0 - 1 - _opensimplex_squish3D
				dz_ext1 = dz0 - 2 - 2 * _opensimplex_squish3D
			else:
				zsv_ext0 = zsv_ext1 = zsb
				dz_ext0 = dz0 - _opensimplex_squish3D
				dz_ext1 = dz0 - 2 * _opensimplex_squish3D

		dx3 = dx0 - 1 - 2 * _opensimplex_squish3D
		dy3 = dy0 - 1 - 2 * _opensimplex_squish3D
		dz3 = dz0 - 0 - 2 * _opensimplex_squish3D
		attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3
		if attn3 > 0:
			attn3 *= attn3
			value += attn3 * attn3 * _opensimplex_extrapolate3D(xsb + 1, ysb + 1, zsb + 0, dx3, dy3, dz3)

		dx2 = dx3
		dy2 = dy0 - 0 - 2 * _opensimplex_squish3D
		dz2 = dz0 - 1 - 2 * _opensimplex_squish3D
		attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2
		if attn2 > 0:
			attn2 *= attn2
			value += attn2 * attn2 * _opensimplex_extrapolate3D(xsb + 1, ysb + 0, zsb + 1, dx2, dy2, dz2)

		dx1 = dx0 - 0 - 2 * _opensimplex_squish3D
		dy1 = dy3
		dz1 = dz2
		attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1
		if attn1 > 0:
			attn1 *= attn1
			value += attn1 * attn1 * _opensimplex_extrapolate3D(xsb + 0, ysb + 1, zsb + 1, dx1, dy1, dz1)

		dx0 = dx0 - 1 - 3 * _opensimplex_squish3D
		dy0 = dy0 - 1 - 3 * _opensimplex_squish3D
		dz0 = dz0 - 1 - 3 * _opensimplex_squish3D
		attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0
		if attn0 > 0:
			attn0 *= attn0
			value += attn0 * attn0 * _opensimplex_extrapolate3D(xsb + 1, ysb + 1, zsb + 1, dx0, dy0, dz0)
	else:
		p1 = xins + yins
		if p1 > 1:
			aScore = p1 - 1
			aPoint = 0x03
			aIsFurtherSide = True
		else:
			aScore = 1 - p1
			aPoint = 0x04
			aIsFurtherSide = False

		p2 = xins + zins
		if p2 > 1:
			bScore = p2 - 1
			bPoint = 0x05
			bIsFurtherSide = True
		else:
			bScore = 1 - p2
			bPoint = 0x02
			bIsFurtherSide = False

		p3 = yins + zins
		if p3 > 1:
			score = p3 - 1
			if aScore <= bScore and aScore < score:
				aScore = score
				aPoint = 0x06
				aIsFurtherSide = True
			elif aScore > bScore and bScore < score:
				bScore = score
				bPoint = 0x06
				bIsFurtherSide = True
		else:
			score = 1 - p3
			if aScore <= bScore and aScore < score:
				aScore = score
				aPoint = 0x01
				aIsFurtherSide = False
			elif aScore > bScore and bScore < score:
				bScore = score
				bPoint = 0x01
				bIsFurtherSide = False

		if aIsFurtherSide == bIsFurtherSide:
			if aIsFurtherSide:

				dx_ext0 = dx0 - 1 - 3 * _opensimplex_squish3D
				dy_ext0 = dy0 - 1 - 3 * _opensimplex_squish3D
				dz_ext0 = dz0 - 1 - 3 * _opensimplex_squish3D
				xsv_ext0 = xsb + 1
				ysv_ext0 = ysb + 1
				zsv_ext0 = zsb + 1

				c = (aPoint & bPoint) & 0xFF
				if (c & 0x01) != 0:
					dx_ext1 = dx0 - 2 - 2 * _opensimplex_squish3D
					dy_ext1 = dy0 - 2 * _opensimplex_squish3D
					dz_ext1 = dz0 - 2 * _opensimplex_squish3D
					xsv_ext1 = xsb + 2
					ysv_ext1 = ysb
					zsv_ext1 = zsb
				elif (c & 0x02) != 0:
					dx_ext1 = dx0 - 2 * _opensimplex_squish3D
					dy_ext1 = dy0 - 2 - 2 * _opensimplex_squish3D
					dz_ext1 = dz0 - 2 * _opensimplex_squish3D
					xsv_ext1 = xsb
					ysv_ext1 = ysb + 2
					zsv_ext1 = zsb
				else:
					dx_ext1 = dx0 - 2 * _opensimplex_squish3D
					dy_ext1 = dy0 - 2 * _opensimplex_squish3D
					dz_ext1 = dz0 - 2 - 2 * _opensimplex_squish3D
					xsv_ext1 = xsb
					ysv_ext1 = ysb
					zsv_ext1 = zsb + 2
			else:
				dx_ext0 = dx0
				dy_ext0 = dy0
				dz_ext0 = dz0
				xsv_ext0 = xsb
				ysv_ext0 = ysb
				zsv_ext0 = zsb

				c = (aPoint | bPoint) & 0xFF
				if (c & 0x01) == 0:
					dx_ext1 = dx0 + 1 - _opensimplex_squish3D
					dy_ext1 = dy0 - 1 - _opensimplex_squish3D
					dz_ext1 = dz0 - 1 - _opensimplex_squish3D
					xsv_ext1 = xsb - 1
					ysv_ext1 = ysb + 1
					zsv_ext1 = zsb + 1
				elif (c & 0x02) == 0:
					dx_ext1 = dx0 - 1 - _opensimplex_squish3D
					dy_ext1 = dy0 + 1 - _opensimplex_squish3D
					dz_ext1 = dz0 - 1 - _opensimplex_squish3D
					xsv_ext1 = xsb + 1
					ysv_ext1 = ysb - 1
					zsv_ext1 = zsb + 1
				else:
					dx_ext1 = dx0 - 1 - _opensimplex_squish3D
					dy_ext1 = dy0 - 1 - _opensimplex_squish3D
					dz_ext1 = dz0 + 1 - _opensimplex_squish3D
					xsv_ext1 = xsb + 1
					ysv_ext1 = ysb + 1
					zsv_ext1 = zsb - 1
		else:
			if aIsFurtherSide:
				c1 = aPoint
				c2 = bPoint
			else:
				c1 = bPoint
				c2 = aPoint

			if (c1 & 0x01) == 0:
				dx_ext0 = dx0 + 1 - _opensimplex_squish3D
				dy_ext0 = dy0 - 1 - _opensimplex_squish3D
				dz_ext0 = dz0 - 1 - _opensimplex_squish3D
				xsv_ext0 = xsb - 1
				ysv_ext0 = ysb + 1
				zsv_ext0 = zsb + 1
			elif (c1 & 0x02) == 0:
				dx_ext0 = dx0 - 1 - _opensimplex_squish3D
				dy_ext0 = dy0 + 1 - _opensimplex_squish3D
				dz_ext0 = dz0 - 1 - _opensimplex_squish3D
				xsv_ext0 = xsb + 1
				ysv_ext0 = ysb - 1
				zsv_ext0 = zsb + 1
			else:
				dx_ext0 = dx0 - 1 - _opensimplex_squish3D
				dy_ext0 = dy0 - 1 - _opensimplex_squish3D
				dz_ext0 = dz0 + 1 - _opensimplex_squish3D
				xsv_ext0 = xsb + 1
				ysv_ext0 = ysb + 1
				zsv_ext0 = zsb - 1

			dx_ext1 = dx0 - 2 * _opensimplex_squish3D
			dy_ext1 = dy0 - 2 * _opensimplex_squish3D
			dz_ext1 = dz0 - 2 * _opensimplex_squish3D
			xsv_ext1 = xsb
			ysv_ext1 = ysb
			zsv_ext1 = zsb
			if (c2 & 0x01) != 0:
				dx_ext1 -= 2
				xsv_ext1 += 2
			elif (c2 & 0x02) != 0:
				dy_ext1 -= 2
				ysv_ext1 += 2
			else:
				dz_ext1 -= 2
				zsv_ext1 += 2

		dx1 = dx0 - 1 - _opensimplex_squish3D
		dy1 = dy0 - 0 - _opensimplex_squish3D
		dz1 = dz0 - 0 - _opensimplex_squish3D
		attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1
		if attn1 > 0:
			attn1 *= attn1
			value += attn1 * attn1 * _opensimplex_extrapolate3D(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1)

		dx2 = dx0 - 0 - _opensimplex_squish3D
		dy2 = dy0 - 1 - _opensimplex_squish3D
		dz2 = dz1
		attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2
		if attn2 > 0:
			attn2 *= attn2
			value += attn2 * attn2 * _opensimplex_extrapolate3D(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2)

		dx3 = dx2
		dy3 = dy1
		dz3 = dz0 - 1 - _opensimplex_squish3D
		attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3
		if attn3 > 0:
			attn3 *= attn3
			value += attn3 * attn3 * _opensimplex_extrapolate3D(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3)

		dx4 = dx0 - 1 - 2 * _opensimplex_squish3D
		dy4 = dy0 - 1 - 2 * _opensimplex_squish3D
		dz4 = dz0 - 0 - 2 * _opensimplex_squish3D
		attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4
		if attn4 > 0:
			attn4 *= attn4
			value += attn4 * attn4 * _opensimplex_extrapolate3D(xsb + 1, ysb + 1, zsb + 0, dx4, dy4, dz4)

		dx5 = dx4
		dy5 = dy0 - 0 - 2 * _opensimplex_squish3D
		dz5 = dz0 - 1 - 2 * _opensimplex_squish3D
		attn5 = 2 - dx5 * dx5 - dy5 * dy5 - dz5 * dz5
		if attn5 > 0:
			attn5 *= attn5
			value += attn5 * attn5 * _opensimplex_extrapolate3D(xsb + 1, ysb + 0, zsb + 1, dx5, dy5, dz5)

		dx6 = dx0 - 0 - 2 * _opensimplex_squish3D
		dy6 = dy4
		dz6 = dz5
		attn6 = 2 - dx6 * dx6 - dy6 * dy6 - dz6 * dz6
		if attn6 > 0:
			attn6 *= attn6
			value += attn6 * attn6 * _opensimplex_extrapolate3D(xsb + 0, ysb + 1, zsb + 1, dx6, dy6, dz6)

	attn_ext0 = 2 - dx_ext0 * dx_ext0 - dy_ext0 * dy_ext0 - dz_ext0 * dz_ext0
	if attn_ext0 > 0:
		attn_ext0 *= attn_ext0
		value += attn_ext0 * attn_ext0 * _opensimplex_extrapolate3D(xsv_ext0, ysv_ext0, zsv_ext0, dx_ext0, dy_ext0, dz_ext0)

	attn_ext1 = 2 - dx_ext1 * dx_ext1 - dy_ext1 * dy_ext1 - dz_ext1 * dz_ext1
	if attn_ext1 > 0:
		attn_ext1 *= attn_ext1
		value += attn_ext1 * attn_ext1 * _opensimplex_extrapolate3D(xsv_ext1, ysv_ext1, zsv_ext1, dx_ext1, dy_ext1, dz_ext1)

	return value / 103

def opensimplex4D(x, y, z, w):
	""" Generate 4D OpenSimplex noise
	Taken from Kurt Spencer Java implementation. """
	stretchOffset = (x + y + z + w) * -0.138196601125011
	xs = x + stretchOffset
	ys = y + stretchOffset
	zs = z + stretchOffset
	ws = w + stretchOffset

	xsb = floor(xs)
	ysb = floor(ys)
	zsb = floor(zs)
	wsb = floor(ws)

	squishOffset = (xsb + ysb + zsb + wsb) * _opensimplex_squish4D
	xb = xsb + squishOffset
	yb = ysb + squishOffset
	zb = zsb + squishOffset
	wb = wsb + squishOffset

	xins = xs - xsb
	yins = ys - ysb
	zins = zs - zsb
	wins = ws - wsb

	inSum = xins + yins + zins + wins

	dx0 = x - xb
	dy0 = y - yb
	dz0 = z - zb
	dw0 = w - wb

	value = 0
	if inSum <= 1:
		aPoint = 0x01
		aScore = xins
		bPoint = 0x02
		bScore = yins
		if aScore >= bScore and zins > bScore:
			bScore = zins
			bPoint = 0x04
		elif aScore < bScore and zins > aScore:
			aScore = zins
			aPoint = 0x04
		if aScore >= bScore and wins > bScore:
			bScore = wins
			bPoint = 0x08
		elif aScore < bScore and wins > aScore:
			aScore = wins
			aPoint = 0x08


		uins = 1 - inSum
		if uins > aScore or uins > bScore:
			c = bPoint if bScore > aScore else aPoint
			if (c & 0x01) == 0:
				xsv_ext0 = xsb - 1
				xsv_ext1 = xsv_ext2 = xsb
				dx_ext0 = dx0 + 1
				dx_ext1 = dx_ext2 = dx0
			else:
				xsv_ext0 = xsv_ext1 = xsv_ext2 = xsb + 1
				dx_ext0 = dx_ext1 = dx_ext2 = dx0 - 1

			if (c & 0x02) == 0:
				ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb
				dy_ext0 = dy_ext1 = dy_ext2 = dy0
				if (c & 0x01) == 0x01:
					ysv_ext0 -= 1
					dy_ext0 += 1
				else:
					ysv_ext1 -= 1
					dy_ext1 += 1
			else:
				ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb + 1
				dy_ext0 = dy_ext1 = dy_ext2 = dy0 - 1

			if (c & 0x04) == 0:
				zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb
				dz_ext0 = dz_ext1 = dz_ext2 = dz0
				if (c & 0x03) != 0:
					if (c & 0x03) == 0x03:
						zsv_ext0 -= 1
						dz_ext0 += 1
					else:
						zsv_ext1 -= 1
						dz_ext1 += 1
				else:
					zsv_ext2 -= 1
					dz_ext2 += 1
			else:
				zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb + 1
				dz_ext0 = dz_ext1 = dz_ext2 = dz0 - 1

			if (c & 0x08) == 0:
				wsv_ext0 = wsv_ext1 = wsb
				wsv_ext2 = wsb - 1
				dw_ext0 = dw_ext1 = dw0
				dw_ext2 = dw0 + 1
			else:
				wsv_ext0 = wsv_ext1 = wsv_ext2 = wsb + 1
				dw_ext0 = dw_ext1 = dw_ext2 = dw0 - 1
		else:
			c = (aPoint | bPoint) & 0xFF
			
			if (c & 0x01) == 0:
				xsv_ext0 = xsv_ext2 = xsb
				xsv_ext1 = xsb - 1
				dx_ext0 = dx0 - 2 * _opensimplex_squish4D
				dx_ext1 = dx0 + 1 - _opensimplex_squish4D
				dx_ext2 = dx0 - _opensimplex_squish4D
			else:
				xsv_ext0 = xsv_ext1 = xsv_ext2 = xsb + 1
				dx_ext0 = dx0 - 1 - 2 * _opensimplex_squish4D
				dx_ext1 = dx_ext2 = dx0 - 1 - _opensimplex_squish4D

			if (c & 0x02) == 0:
				ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb
				dy_ext0 = dy0 - 2 * _opensimplex_squish4D
				dy_ext1 = dy_ext2 = dy0 - _opensimplex_squish4D
				if (c & 0x01) == 0x01:
					ysv_ext1 -= 1
					dy_ext1 += 1
				else:
					ysv_ext2 -= 1
					dy_ext2 += 1
			else:
				ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb + 1
				dy_ext0 = dy0 - 1 - 2 * _opensimplex_squish4D
				dy_ext1 = dy_ext2 = dy0 - 1 - _opensimplex_squish4D

			if (c & 0x04) == 0:
				zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb
				dz_ext0 = dz0 - 2 * _opensimplex_squish4D
				dz_ext1 = dz_ext2 = dz0 - _opensimplex_squish4D
				if (c & 0x03) == 0x03:
					zsv_ext1 -= 1
					dz_ext1 += 1
				else:
					zsv_ext2 -= 1
					dz_ext2 += 1
			else:
				zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb + 1
				dz_ext0 = dz0 - 1 - 2 * _opensimplex_squish4D
				dz_ext1 = dz_ext2 = dz0 - 1 - _opensimplex_squish4D

			if (c & 0x08) == 0:
				wsv_ext0 = wsv_ext1 = wsb
				wsv_ext2 = wsb - 1
				dw_ext0 = dw0 - 2 * _opensimplex_squish4D
				dw_ext1 = dw0 - _opensimplex_squish4D
				dw_ext2 = dw0 + 1 - _opensimplex_squish4D
			else:
				wsv_ext0 = wsv_ext1 = wsv_ext2 = wsb + 1
				dw_ext0 = dw0 - 1 - 2 * _opensimplex_squish4D
				dw_ext1 = dw_ext2 = dw0 - 1 - _opensimplex_squish4D

		attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0 - dw0 * dw0
		if attn0 > 0:
			attn0 *= attn0
			value += attn0 * attn0 * _opensimplex_extrapolate4D(xsb + 0, ysb + 0, zsb + 0, wsb + 0, dx0, dy0, dz0, dw0)

		dx1 = dx0 - 1 - _opensimplex_squish4D
		dy1 = dy0 - 0 - _opensimplex_squish4D
		dz1 = dz0 - 0 - _opensimplex_squish4D
		dw1 = dw0 - 0 - _opensimplex_squish4D
		attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1 - dw1 * dw1
		if attn1 > 0:
			attn1 *= attn1
			value += attn1 * attn1 * _opensimplex_extrapolate4D(xsb + 1, ysb + 0, zsb + 0, wsb + 0, dx1, dy1, dz1, dw1)

		dx2 = dx0 - 0 - _opensimplex_squish4D
		dy2 = dy0 - 1 - _opensimplex_squish4D
		dz2 = dz1
		dw2 = dw1
		attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2 - dw2 * dw2
		if attn2 > 0:
			attn2 *= attn2
			value += attn2 * attn2 * _opensimplex_extrapolate4D(xsb + 0, ysb + 1, zsb + 0, wsb + 0, dx2, dy2, dz2, dw2)

		dx3 = dx2
		dy3 = dy1
		dz3 = dz0 - 1 - _opensimplex_squish4D
		dw3 = dw1
		attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3 - dw3 * dw3
		if attn3 > 0:
			attn3 *= attn3
			value += attn3 * attn3 * _opensimplex_extrapolate4D(xsb + 0, ysb + 0, zsb + 1, wsb + 0, dx3, dy3, dz3, dw3)

		dx4 = dx2
		dy4 = dy1
		dz4 = dz1
		dw4 = dw0 - 1 - _opensimplex_squish4D
		attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4 - dw4 * dw4
		if attn4 > 0:
			attn4 *= attn4
			value += attn4 * attn4 * _opensimplex_extrapolate4D(xsb + 0, ysb + 0, zsb + 0, wsb + 1, dx4, dy4, dz4, dw4)
	elif inSum >= 3:
		aPoint = 0x0E
		aScore = xins
		bPoint = 0x0D
		bScore = yins
		if aScore <= bScore and zins < bScore:
			bScore = zins
			bPoint = 0x0B
		elif aScore > bScore and zins < aScore:
			aScore = zins
			aPoint = 0x0B
		if aScore <= bScore and wins < bScore:
			bScore = wins
			bPoint = 0x07
		elif aScore > bScore and wins < aScore:
			aScore = wins
			aPoint = 0x07


		uins = 4 - inSum
		if uins < aScore or uins < bScore:
			c = bPoint if bScore < aScore else aPoint
			
			if (c & 0x01) != 0:
				xsv_ext0 = xsb + 2
				xsv_ext1 = xsv_ext2 = xsb + 1
				dx_ext0 = dx0 - 2 - 4 * _opensimplex_squish4D
				dx_ext1 = dx_ext2 = dx0 - 1 - 4 * _opensimplex_squish4D
			else:
				xsv_ext0 = xsv_ext1 = xsv_ext2 = xsb
				dx_ext0 = dx_ext1 = dx_ext2 = dx0 - 4 * _opensimplex_squish4D

			if (c & 0x02) != 0:
				ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb + 1
				dy_ext0 = dy_ext1 = dy_ext2 = dy0 - 1 - 4 * _opensimplex_squish4D
				if (c & 0x01) != 0:
					ysv_ext1 += 1
					dy_ext1 -= 1
				else:
					ysv_ext0 += 1
					dy_ext0 -= 1
			else:
				ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb
				dy_ext0 = dy_ext1 = dy_ext2 = dy0 - 4 * _opensimplex_squish4D

			if (c & 0x04) != 0:
				zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb + 1
				dz_ext0 = dz_ext1 = dz_ext2 = dz0 - 1 - 4 * _opensimplex_squish4D
				if (c & 0x03) != 0x03:
					if (c & 0x03) == 0:
						zsv_ext0 += 1
						dz_ext0 -= 1
					else:
						zsv_ext1 += 1
						dz_ext1 -= 1
				else:
					zsv_ext2 += 1
					dz_ext2 -= 1
			else:
				zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb
				dz_ext0 = dz_ext1 = dz_ext2 = dz0 - 4 * _opensimplex_squish4D

			if (c & 0x08) != 0:
				wsv_ext0 = wsv_ext1 = wsb + 1
				wsv_ext2 = wsb + 2
				dw_ext0 = dw_ext1 = dw0 - 1 - 4 * _opensimplex_squish4D
				dw_ext2 = dw0 - 2 - 4 * _opensimplex_squish4D
			else:
				wsv_ext0 = wsv_ext1 = wsv_ext2 = wsb
				dw_ext0 = dw_ext1 = dw_ext2 = dw0 - 4 * _opensimplex_squish4D
		else:
			c = (aPoint & bPoint) & 0xFF
			
			if (c & 0x01) != 0:
				xsv_ext0 = xsv_ext2 = xsb + 1
				xsv_ext1 = xsb + 2
				dx_ext0 = dx0 - 1 - 2 * _opensimplex_squish4D
				dx_ext1 = dx0 - 2 - 3 * _opensimplex_squish4D
				dx_ext2 = dx0 - 1 - 3 * _opensimplex_squish4D
			else:
				xsv_ext0 = xsv_ext1 = xsv_ext2 = xsb
				dx_ext0 = dx0 - 2 * _opensimplex_squish4D
				dx_ext1 = dx_ext2 = dx0 - 3 * _opensimplex_squish4D

			if (c & 0x02) != 0:
				ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb + 1
				dy_ext0 = dy0 - 1 - 2 * _opensimplex_squish4D
				dy_ext1 = dy_ext2 = dy0 - 1 - 3 * _opensimplex_squish4D
				if (c & 0x01) != 0:
					ysv_ext2 += 1
					dy_ext2 -= 1
				else:
					ysv_ext1 += 1
					dy_ext1 -= 1
			else:
				ysv_ext0 = ysv_ext1 = ysv_ext2 = ysb
				dy_ext0 = dy0 - 2 * _opensimplex_squish4D
				dy_ext1 = dy_ext2 = dy0 - 3 * _opensimplex_squish4D

			if (c & 0x04) != 0:
				zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb + 1
				dz_ext0 = dz0 - 1 - 2 * _opensimplex_squish4D
				dz_ext1 = dz_ext2 = dz0 - 1 - 3 * _opensimplex_squish4D
				if (c & 0x03) != 0:
					zsv_ext2 += 1
					dz_ext2 -= 1
				else:
					zsv_ext1 += 1
					dz_ext1 -= 1
			else:
				zsv_ext0 = zsv_ext1 = zsv_ext2 = zsb
				dz_ext0 = dz0 - 2 * _opensimplex_squish4D
				dz_ext1 = dz_ext2 = dz0 - 3 * _opensimplex_squish4D

			if (c & 0x08) != 0:
				wsv_ext0 = wsv_ext1 = wsb + 1
				wsv_ext2 = wsb + 2
				dw_ext0 = dw0 - 1 - 2 * _opensimplex_squish4D
				dw_ext1 = dw0 - 1 - 3 * _opensimplex_squish4D
				dw_ext2 = dw0 - 2 - 3 * _opensimplex_squish4D
			else:
				wsv_ext0 = wsv_ext1 = wsv_ext2 = wsb
				dw_ext0 = dw0 - 2 * _opensimplex_squish4D
				dw_ext1 = dw_ext2 = dw0 - 3 * _opensimplex_squish4D

		dx4 = dx0 - 1 - 3 * _opensimplex_squish4D
		dy4 = dy0 - 1 - 3 * _opensimplex_squish4D
		dz4 = dz0 - 1 - 3 * _opensimplex_squish4D
		dw4 = dw0 - 3 * _opensimplex_squish4D
		attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4 - dw4 * dw4
		if attn4 > 0:
			attn4 *= attn4
			value += attn4 * attn4 * _opensimplex_extrapolate4D(xsb + 1, ysb + 1, zsb + 1, wsb + 0, dx4, dy4, dz4, dw4)

		dx3 = dx4
		dy3 = dy4
		dz3 = dz0 - 3 * _opensimplex_squish4D
		dw3 = dw0 - 1 - 3 * _opensimplex_squish4D
		attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3 - dw3 * dw3
		if attn3 > 0:
			attn3 *= attn3
			value += attn3 * attn3 * _opensimplex_extrapolate4D(xsb + 1, ysb + 1, zsb + 0, wsb + 1, dx3, dy3, dz3, dw3)

		dx2 = dx4
		dy2 = dy0 - 3 * _opensimplex_squish4D
		dz2 = dz4
		dw2 = dw3
		attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2 - dw2 * dw2
		if attn2 > 0:
			attn2 *= attn2
			value += attn2 * attn2 * _opensimplex_extrapolate4D(xsb + 1, ysb + 0, zsb + 1, wsb + 1, dx2, dy2, dz2, dw2)

		dx1 = dx0 - 3 * _opensimplex_squish4D
		dz1 = dz4
		dy1 = dy4
		dw1 = dw3
		attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1 - dw1 * dw1
		if attn1 > 0:
			attn1 *= attn1
			value += attn1 * attn1 * _opensimplex_extrapolate4D(xsb + 0, ysb + 1, zsb + 1, wsb + 1, dx1, dy1, dz1, dw1)

		dx0 = dx0 - 1 - 4 * _opensimplex_squish4D
		dy0 = dy0 - 1 - 4 * _opensimplex_squish4D
		dz0 = dz0 - 1 - 4 * _opensimplex_squish4D
		dw0 = dw0 - 1 - 4 * _opensimplex_squish4D
		attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0 - dw0 * dw0
		if attn0 > 0:
			attn0 *= attn0
			value += attn0 * attn0 * _opensimplex_extrapolate4D(xsb + 1, ysb + 1, zsb + 1, wsb + 1, dx0, dy0, dz0, dw0)
	elif inSum <= 2:
		aIsBiggerSide = True
		bIsBiggerSide = True

		if xins + yins > zins + wins:
			aScore = xins + yins
			aPoint = 0x03
		else:
			aScore = zins + wins
			aPoint = 0x0C

		if xins + zins > yins + wins:
			bScore = xins + zins
			bPoint = 0x05
		else:
			bScore = yins + wins
			bPoint = 0x0A

		if xins + wins > yins + zins:
			score = xins + wins
			if aScore >= bScore and score > bScore:
				bScore = score
				bPoint = 0x09
			elif aScore < bScore and score > aScore:
				aScore = score
				aPoint = 0x09
		else:
			score = yins + zins
			if aScore >= bScore and score > bScore:
				bScore = score
				bPoint = 0x06
			elif aScore < bScore and score > aScore:
				aScore = score
				aPoint = 0x06

		p1 = 2 - inSum + xins
		if aScore >= bScore and p1 > bScore:
			bScore = p1
			bPoint = 0x01
			bIsBiggerSide = False
		elif aScore < bScore and p1 > aScore:
			aScore = p1
			aPoint = 0x01
			aIsBiggerSide = False

		p2 = 2 - inSum + yins
		if aScore >= bScore and p2 > bScore:
			bScore = p2
			bPoint = 0x02
			bIsBiggerSide = False
		elif aScore < bScore and p2 > aScore:
			aScore = p2
			aPoint = 0x02
			aIsBiggerSide = False

		p3 = 2 - inSum + zins
		if aScore >= bScore and p3 > bScore:
			bScore = p3
			bPoint = 0x04
			bIsBiggerSide = False
		elif aScore < bScore and p3 > aScore:
			aScore = p3
			aPoint = 0x04
			aIsBiggerSide = False

		p4 = 2 - inSum + wins
		if aScore >= bScore and p4 > bScore:
			bScore = p4
			bPoint = 0x08
			bIsBiggerSide = False
		elif aScore < bScore and p4 > aScore:
			aScore = p4
			aPoint = 0x08
			aIsBiggerSide = False

		if aIsBiggerSide == bIsBiggerSide:
			if aIsBiggerSide:
				c1 = (aPoint | bPoint) & 0xFF
				c2 = (aPoint & bPoint) & 0xFF
				if (c1 & 0x01) == 0:
					xsv_ext0 = xsb
					xsv_ext1 = xsb - 1
					dx_ext0 = dx0 - 3 * _opensimplex_squish4D
					dx_ext1 = dx0 + 1 - 2 * _opensimplex_squish4D
				else:
					xsv_ext0 = xsv_ext1 = xsb + 1
					dx_ext0 = dx0 - 1 - 3 * _opensimplex_squish4D
					dx_ext1 = dx0 - 1 - 2 * _opensimplex_squish4D

				if (c1 & 0x02) == 0:
					ysv_ext0 = ysb
					ysv_ext1 = ysb - 1
					dy_ext0 = dy0 - 3 * _opensimplex_squish4D
					dy_ext1 = dy0 + 1 - 2 * _opensimplex_squish4D
				else:
					ysv_ext0 = ysv_ext1 = ysb + 1
					dy_ext0 = dy0 - 1 - 3 * _opensimplex_squish4D
					dy_ext1 = dy0 - 1 - 2 * _opensimplex_squish4D

				if (c1 & 0x04) == 0:
					zsv_ext0 = zsb
					zsv_ext1 = zsb - 1
					dz_ext0 = dz0 - 3 * _opensimplex_squish4D
					dz_ext1 = dz0 + 1 - 2 * _opensimplex_squish4D
				else:
					zsv_ext0 = zsv_ext1 = zsb + 1
					dz_ext0 = dz0 - 1 - 3 * _opensimplex_squish4D
					dz_ext1 = dz0 - 1 - 2 * _opensimplex_squish4D

				if (c1 & 0x08) == 0:
					wsv_ext0 = wsb
					wsv_ext1 = wsb - 1
					dw_ext0 = dw0 - 3 * _opensimplex_squish4D
					dw_ext1 = dw0 + 1 - 2 * _opensimplex_squish4D
				else:
					wsv_ext0 = wsv_ext1 = wsb + 1
					dw_ext0 = dw0 - 1 - 3 * _opensimplex_squish4D
					dw_ext1 = dw0 - 1 - 2 * _opensimplex_squish4D

				xsv_ext2 = xsb
				ysv_ext2 = ysb
				zsv_ext2 = zsb
				wsv_ext2 = wsb
				dx_ext2 = dx0 - 2 * _opensimplex_squish4D
				dy_ext2 = dy0 - 2 * _opensimplex_squish4D
				dz_ext2 = dz0 - 2 * _opensimplex_squish4D
				dw_ext2 = dw0 - 2 * _opensimplex_squish4D
				if (c2 & 0x01) != 0:
					xsv_ext2 += 2
					dx_ext2 -= 2
				elif (c2 & 0x02) != 0:
					ysv_ext2 += 2
					dy_ext2 -= 2
				elif (c2 & 0x04) != 0:
					zsv_ext2 += 2
					dz_ext2 -= 2
				else:
					wsv_ext2 += 2
					dw_ext2 -= 2
			else:
				xsv_ext2 = xsb
				ysv_ext2 = ysb
				zsv_ext2 = zsb
				wsv_ext2 = wsb
				dx_ext2 = dx0
				dy_ext2 = dy0
				dz_ext2 = dz0
				dw_ext2 = dw0

				c = (aPoint | bPoint) & 0xFF
				
				if (c & 0x01) == 0:
					xsv_ext0 = xsb - 1
					xsv_ext1 = xsb
					dx_ext0 = dx0 + 1 - _opensimplex_squish4D
					dx_ext1 = dx0 - _opensimplex_squish4D
				else:
					xsv_ext0 = xsv_ext1 = xsb + 1
					dx_ext0 = dx_ext1 = dx0 - 1 - _opensimplex_squish4D

				if (c & 0x02) == 0:
					ysv_ext0 = ysv_ext1 = ysb
					dy_ext0 = dy_ext1 = dy0 - _opensimplex_squish4D
					if (c & 0x01) == 0x01:
						ysv_ext0 -= 1
						dy_ext0 += 1
					else:
						ysv_ext1 -= 1
						dy_ext1 += 1
				else:
					ysv_ext0 = ysv_ext1 = ysb + 1
					dy_ext0 = dy_ext1 = dy0 - 1 - _opensimplex_squish4D

				if (c & 0x04) == 0:
					zsv_ext0 = zsv_ext1 = zsb
					dz_ext0 = dz_ext1 = dz0 - _opensimplex_squish4D
					if (c & 0x03) == 0x03:
						zsv_ext0 -= 1
						dz_ext0 += 1
					else:
						zsv_ext1 -= 1
						dz_ext1 += 1
				else:
					zsv_ext0 = zsv_ext1 = zsb + 1
					dz_ext0 = dz_ext1 = dz0 - 1 - _opensimplex_squish4D

				if (c & 0x08) == 0:
					wsv_ext0 = wsb
					wsv_ext1 = wsb - 1
					dw_ext0 = dw0 - _opensimplex_squish4D
					dw_ext1 = dw0 + 1 - _opensimplex_squish4D
				else:
					wsv_ext0 = wsv_ext1 = wsb + 1
					dw_ext0 = dw_ext1 = dw0 - 1 - _opensimplex_squish4D
		else:
			if aIsBiggerSide:
				c1 = aPoint
				c2 = bPoint
			else:
				c1 = bPoint
				c2 = aPoint

			if (c1 & 0x01) == 0:
				xsv_ext0 = xsb - 1
				xsv_ext1 = xsb
				dx_ext0 = dx0 + 1 - _opensimplex_squish4D
				dx_ext1 = dx0 - _opensimplex_squish4D
			else:
				xsv_ext0 = xsv_ext1 = xsb + 1
				dx_ext0 = dx_ext1 = dx0 - 1 - _opensimplex_squish4D

			if (c1 & 0x02) == 0:
				ysv_ext0 = ysv_ext1 = ysb
				dy_ext0 = dy_ext1 = dy0 - _opensimplex_squish4D
				if (c1 & 0x01) == 0x01:
					ysv_ext0 -= 1
					dy_ext0 += 1
				else:
					ysv_ext1 -= 1
					dy_ext1 += 1
			else:
				ysv_ext0 = ysv_ext1 = ysb + 1
				dy_ext0 = dy_ext1 = dy0 - 1 - _opensimplex_squish4D

			if (c1 & 0x04) == 0:
				zsv_ext0 = zsv_ext1 = zsb
				dz_ext0 = dz_ext1 = dz0 - _opensimplex_squish4D
				if (c1 & 0x03) == 0x03:
					zsv_ext0 -= 1
					dz_ext0 += 1
				else:
					zsv_ext1 -= 1
					dz_ext1 += 1
			else:
				zsv_ext0 = zsv_ext1 = zsb + 1
				dz_ext0 = dz_ext1 = dz0 - 1 - _opensimplex_squish4D

			if (c1 & 0x08) == 0:
				wsv_ext0 = wsb
				wsv_ext1 = wsb - 1
				dw_ext0 = dw0 - _opensimplex_squish4D
				dw_ext1 = dw0 + 1 - _opensimplex_squish4D
			else:
				wsv_ext0 = wsv_ext1 = wsb + 1
				dw_ext0 = dw_ext1 = dw0 - 1 - _opensimplex_squish4D

			xsv_ext2 = xsb
			ysv_ext2 = ysb
			zsv_ext2 = zsb
			wsv_ext2 = wsb
			dx_ext2 = dx0 - 2 * _opensimplex_squish4D
			dy_ext2 = dy0 - 2 * _opensimplex_squish4D
			dz_ext2 = dz0 - 2 * _opensimplex_squish4D
			dw_ext2 = dw0 - 2 * _opensimplex_squish4D
			if (c2 & 0x01) != 0:
				xsv_ext2 += 2
				dx_ext2 -= 2
			elif (c2 & 0x02) != 0:
				ysv_ext2 += 2
				dy_ext2 -= 2
			elif (c2 & 0x04) != 0:
				zsv_ext2 += 2
				dz_ext2 -= 2
			else:
				wsv_ext2 += 2
				dw_ext2 -= 2

		dx1 = dx0 - 1 - _opensimplex_squish4D
		dy1 = dy0 - 0 - _opensimplex_squish4D
		dz1 = dz0 - 0 - _opensimplex_squish4D
		dw1 = dw0 - 0 - _opensimplex_squish4D
		attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1 - dw1 * dw1
		if attn1 > 0:
			attn1 *= attn1
			value += attn1 * attn1 * _opensimplex_extrapolate4D(xsb + 1, ysb + 0, zsb + 0, wsb + 0, dx1, dy1, dz1, dw1)

		dx2 = dx0 - 0 - _opensimplex_squish4D
		dy2 = dy0 - 1 - _opensimplex_squish4D
		dz2 = dz1
		dw2 = dw1
		attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2 - dw2 * dw2
		if attn2 > 0:
			attn2 *= attn2
			value += attn2 * attn2 * _opensimplex_extrapolate4D(xsb + 0, ysb + 1, zsb + 0, wsb + 0, dx2, dy2, dz2, dw2)

		dx3 = dx2
		dy3 = dy1
		dz3 = dz0 - 1 - _opensimplex_squish4D
		dw3 = dw1
		attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3 - dw3 * dw3
		if attn3 > 0:
			attn3 *= attn3
			value += attn3 * attn3 * _opensimplex_extrapolate4D(xsb + 0, ysb + 0, zsb + 1, wsb + 0, dx3, dy3, dz3, dw3)

		dx4 = dx2
		dy4 = dy1
		dz4 = dz1
		dw4 = dw0 - 1 - _opensimplex_squish4D
		attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4 - dw4 * dw4
		if attn4 > 0:
			attn4 *= attn4
			value += attn4 * attn4 * _opensimplex_extrapolate4D(xsb + 0, ysb + 0, zsb + 0, wsb + 1, dx4, dy4, dz4, dw4)

		dx5 = dx0 - 1 - 2 * _opensimplex_squish4D
		dy5 = dy0 - 1 - 2 * _opensimplex_squish4D
		dz5 = dz0 - 0 - 2 * _opensimplex_squish4D
		dw5 = dw0 - 0 - 2 * _opensimplex_squish4D
		attn5 = 2 - dx5 * dx5 - dy5 * dy5 - dz5 * dz5 - dw5 * dw5
		if attn5 > 0:
			attn5 *= attn5
			value += attn5 * attn5 * _opensimplex_extrapolate4D(xsb + 1, ysb + 1, zsb + 0, wsb + 0, dx5, dy5, dz5, dw5)

		dx6 = dx0 - 1 - 2 * _opensimplex_squish4D
		dy6 = dy0 - 0 - 2 * _opensimplex_squish4D
		dz6 = dz0 - 1 - 2 * _opensimplex_squish4D
		dw6 = dw0 - 0 - 2 * _opensimplex_squish4D
		attn6 = 2 - dx6 * dx6 - dy6 * dy6 - dz6 * dz6 - dw6 * dw6
		if attn6 > 0:
			attn6 *= attn6
			value += attn6 * attn6 * _opensimplex_extrapolate4D(xsb + 1, ysb + 0, zsb + 1, wsb + 0, dx6, dy6, dz6, dw6)

		dx7 = dx0 - 1 - 2 * _opensimplex_squish4D
		dy7 = dy0 - 0 - 2 * _opensimplex_squish4D
		dz7 = dz0 - 0 - 2 * _opensimplex_squish4D
		dw7 = dw0 - 1 - 2 * _opensimplex_squish4D
		attn7 = 2 - dx7 * dx7 - dy7 * dy7 - dz7 * dz7 - dw7 * dw7
		if attn7 > 0:
			attn7 *= attn7
			value += attn7 * attn7 * _opensimplex_extrapolate4D(xsb + 1, ysb + 0, zsb + 0, wsb + 1, dx7, dy7, dz7, dw7)

		dx8 = dx0 - 0 - 2 * _opensimplex_squish4D
		dy8 = dy0 - 1 - 2 * _opensimplex_squish4D
		dz8 = dz0 - 1 - 2 * _opensimplex_squish4D
		dw8 = dw0 - 0 - 2 * _opensimplex_squish4D
		attn8 = 2 - dx8 * dx8 - dy8 * dy8 - dz8 * dz8 - dw8 * dw8
		if attn8 > 0:
			attn8 *= attn8
			value += attn8 * attn8 * _opensimplex_extrapolate4D(xsb + 0, ysb + 1, zsb + 1, wsb + 0, dx8, dy8, dz8, dw8)

		dx9 = dx0 - 0 - 2 * _opensimplex_squish4D
		dy9 = dy0 - 1 - 2 * _opensimplex_squish4D
		dz9 = dz0 - 0 - 2 * _opensimplex_squish4D
		dw9 = dw0 - 1 - 2 * _opensimplex_squish4D
		attn9 = 2 - dx9 * dx9 - dy9 * dy9 - dz9 * dz9 - dw9 * dw9
		if attn9 > 0:
			attn9 *= attn9
			value += attn9 * attn9 * _opensimplex_extrapolate4D(xsb + 0, ysb + 1, zsb + 0, wsb + 1, dx9, dy9, dz9, dw9)

		dx10 = dx0 - 0 - 2 * _opensimplex_squish4D
		dy10 = dy0 - 0 - 2 * _opensimplex_squish4D
		dz10 = dz0 - 1 - 2 * _opensimplex_squish4D
		dw10 = dw0 - 1 - 2 * _opensimplex_squish4D
		attn10 = 2 - dx10 * dx10 - dy10 * dy10 - dz10 * dz10 - dw10 * dw10
		if attn10 > 0:
			attn10 *= attn10
			value += attn10 * attn10 * _opensimplex_extrapolate4D(xsb + 0, ysb + 0, zsb + 1, wsb + 1, dx10, dy10, dz10, dw10)
	else:
		aIsBiggerSide = True
		bIsBiggerSide = True

		if xins + yins < zins + wins:
			aScore = xins + yins
			aPoint = 0x0C
		else:
			aScore = zins + wins
			aPoint = 0x03

		if xins + zins < yins + wins:
			bScore = xins + zins
			bPoint = 0x0A
		else:
			bScore = yins + wins
			bPoint = 0x05

		if xins + wins < yins + zins:
			score = xins + wins
			if aScore <= bScore and score < bScore:
				bScore = score
				bPoint = 0x06
			elif aScore > bScore and score < aScore:
				aScore = score
				aPoint = 0x06
		else:
			score = yins + zins
			if aScore <= bScore and score < bScore:
				bScore = score
				bPoint = 0x09
			elif aScore > bScore and score < aScore:
				aScore = score
				aPoint = 0x09

		p1 = 3 - inSum + xins
		if aScore <= bScore and p1 < bScore:
			bScore = p1
			bPoint = 0x0E
			bIsBiggerSide = False
		elif aScore > bScore and p1 < aScore:
			aScore = p1
			aPoint = 0x0E
			aIsBiggerSide = False

		p2 = 3 - inSum + yins
		if aScore <= bScore and p2 < bScore:
			bScore = p2
			bPoint = 0x0D
			bIsBiggerSide = False
		elif aScore > bScore and p2 < aScore:
			aScore = p2
			aPoint = 0x0D
			aIsBiggerSide = False

		p3 = 3 - inSum + zins
		if aScore <= bScore and p3 < bScore:
			bScore = p3
			bPoint = 0x0B
			bIsBiggerSide = False
		elif aScore > bScore and p3 < aScore:
			aScore = p3
			aPoint = 0x0B
			aIsBiggerSide = False

		p4 = 3 - inSum + wins
		if aScore <= bScore and p4 < bScore:
			bScore = p4
			bPoint = 0x07
			bIsBiggerSide = False
		elif aScore > bScore and p4 < aScore:
			aScore = p4
			aPoint = 0x07
			aIsBiggerSide = False

		if aIsBiggerSide == bIsBiggerSide:
			if aIsBiggerSide:
				c1 = (aPoint & bPoint) & 0xFF
				c2 = (aPoint | bPoint) & 0xFF

				xsv_ext0 = xsv_ext1 = xsb
				ysv_ext0 = ysv_ext1 = ysb
				zsv_ext0 = zsv_ext1 = zsb
				wsv_ext0 = wsv_ext1 = wsb
				dx_ext0 = dx0 - _opensimplex_squish4D
				dy_ext0 = dy0 - _opensimplex_squish4D
				dz_ext0 = dz0 - _opensimplex_squish4D
				dw_ext0 = dw0 - _opensimplex_squish4D
				dx_ext1 = dx0 - 2 * _opensimplex_squish4D
				dy_ext1 = dy0 - 2 * _opensimplex_squish4D
				dz_ext1 = dz0 - 2 * _opensimplex_squish4D
				dw_ext1 = dw0 - 2 * _opensimplex_squish4D
				if (c1 & 0x01) != 0:
					xsv_ext0 += 1
					dx_ext0 -= 1
					xsv_ext1 += 2
					dx_ext1 -= 2
				elif (c1 & 0x02) != 0:
					ysv_ext0 += 1
					dy_ext0 -= 1
					ysv_ext1 += 2
					dy_ext1 -= 2
				elif (c1 & 0x04) != 0:
					zsv_ext0 += 1
					dz_ext0 -= 1
					zsv_ext1 += 2
					dz_ext1 -= 2
				else:
					wsv_ext0 += 1
					dw_ext0 -= 1
					wsv_ext1 += 2
					dw_ext1 -= 2

				xsv_ext2 = xsb + 1
				ysv_ext2 = ysb + 1
				zsv_ext2 = zsb + 1
				wsv_ext2 = wsb + 1
				dx_ext2 = dx0 - 1 - 2 * _opensimplex_squish4D
				dy_ext2 = dy0 - 1 - 2 * _opensimplex_squish4D
				dz_ext2 = dz0 - 1 - 2 * _opensimplex_squish4D
				dw_ext2 = dw0 - 1 - 2 * _opensimplex_squish4D
				if (c2 & 0x01) == 0:
					xsv_ext2 -= 2
					dx_ext2 += 2
				elif (c2 & 0x02) == 0:
					ysv_ext2 -= 2
					dy_ext2 += 2
				elif (c2 & 0x04) == 0:
					zsv_ext2 -= 2
					dz_ext2 += 2
				else:
					wsv_ext2 -= 2
					dw_ext2 += 2
			else:

				xsv_ext2 = xsb + 1
				ysv_ext2 = ysb + 1
				zsv_ext2 = zsb + 1
				wsv_ext2 = wsb + 1
				dx_ext2 = dx0 - 1 - 4 * _opensimplex_squish4D
				dy_ext2 = dy0 - 1 - 4 * _opensimplex_squish4D
				dz_ext2 = dz0 - 1 - 4 * _opensimplex_squish4D
				dw_ext2 = dw0 - 1 - 4 * _opensimplex_squish4D

				c = (aPoint & bPoint) & 0xFF
				
				if (c & 0x01) != 0:
					xsv_ext0 = xsb + 2
					xsv_ext1 = xsb + 1
					dx_ext0 = dx0 - 2 - 3 * _opensimplex_squish4D
					dx_ext1 = dx0 - 1 - 3 * _opensimplex_squish4D
				else:
					xsv_ext0 = xsv_ext1 = xsb
					dx_ext0 = dx_ext1 = dx0 - 3 * _opensimplex_squish4D

				if (c & 0x02) != 0:
					ysv_ext0 = ysv_ext1 = ysb + 1
					dy_ext0 = dy_ext1 = dy0 - 1 - 3 * _opensimplex_squish4D
					if (c & 0x01) == 0:
						ysv_ext0 += 1
						dy_ext0 -= 1
					else:
						ysv_ext1 += 1
						dy_ext1 -= 1
				else:
					ysv_ext0 = ysv_ext1 = ysb
					dy_ext0 = dy_ext1 = dy0 - 3 * _opensimplex_squish4D

				if (c & 0x04) != 0:
					zsv_ext0 = zsv_ext1 = zsb + 1
					dz_ext0 = dz_ext1 = dz0 - 1 - 3 * _opensimplex_squish4D
					if (c & 0x03) == 0:
						zsv_ext0 += 1
						dz_ext0 -= 1
					else:
						zsv_ext1 += 1
						dz_ext1 -= 1
				else:
					zsv_ext0 = zsv_ext1 = zsb
					dz_ext0 = dz_ext1 = dz0 - 3 * _opensimplex_squish4D

				if (c & 0x08) != 0:
					wsv_ext0 = wsb + 1
					wsv_ext1 = wsb + 2
					dw_ext0 = dw0 - 1 - 3 * _opensimplex_squish4D
					dw_ext1 = dw0 - 2 - 3 * _opensimplex_squish4D
				else:
					wsv_ext0 = wsv_ext1 = wsb
					dw_ext0 = dw_ext1 = dw0 - 3 * _opensimplex_squish4D
		else:
			if aIsBiggerSide:
				c1 = aPoint
				c2 = bPoint
			else:
				c1 = bPoint
				c2 = aPoint

			if (c1 & 0x01) != 0:
				xsv_ext0 = xsb + 2
				xsv_ext1 = xsb + 1
				dx_ext0 = dx0 - 2 - 3 * _opensimplex_squish4D
				dx_ext1 = dx0 - 1 - 3 * _opensimplex_squish4D
			else:
				xsv_ext0 = xsv_ext1 = xsb
				dx_ext0 = dx_ext1 = dx0 - 3 * _opensimplex_squish4D

			if (c1 & 0x02) != 0:
				ysv_ext0 = ysv_ext1 = ysb + 1
				dy_ext0 = dy_ext1 = dy0 - 1 - 3 * _opensimplex_squish4D
				if (c1 & 0x01) == 0:
					ysv_ext0 += 1
					dy_ext0 -= 1
				else:
					ysv_ext1 += 1
					dy_ext1 -= 1
			else:
				ysv_ext0 = ysv_ext1 = ysb
				dy_ext0 = dy_ext1 = dy0 - 3 * _opensimplex_squish4D

			if (c1 & 0x04) != 0:
				zsv_ext0 = zsv_ext1 = zsb + 1
				dz_ext0 = dz_ext1 = dz0 - 1 - 3 * _opensimplex_squish4D
				if (c1 & 0x03) == 0:
					zsv_ext0 += 1
					dz_ext0 -= 1
				else:
					zsv_ext1 += 1
					dz_ext1 -= 1
			else:
				zsv_ext0 = zsv_ext1 = zsb
				dz_ext0 = dz_ext1 = dz0 - 3 * _opensimplex_squish4D

			if (c1 & 0x08) != 0:
				wsv_ext0 = wsb + 1
				wsv_ext1 = wsb + 2
				dw_ext0 = dw0 - 1 - 3 * _opensimplex_squish4D
				dw_ext1 = dw0 - 2 - 3 * _opensimplex_squish4D
			else:
				wsv_ext0 = wsv_ext1 = wsb
				dw_ext0 = dw_ext1 = dw0 - 3 * _opensimplex_squish4D

			xsv_ext2 = xsb + 1
			ysv_ext2 = ysb + 1
			zsv_ext2 = zsb + 1
			wsv_ext2 = wsb + 1
			dx_ext2 = dx0 - 1 - 2 * _opensimplex_squish4D
			dy_ext2 = dy0 - 1 - 2 * _opensimplex_squish4D
			dz_ext2 = dz0 - 1 - 2 * _opensimplex_squish4D
			dw_ext2 = dw0 - 1 - 2 * _opensimplex_squish4D
			if (c2 & 0x01) == 0:
				xsv_ext2 -= 2
				dx_ext2 += 2
			elif (c2 & 0x02) == 0:
				ysv_ext2 -= 2
				dy_ext2 += 2
			elif (c2 & 0x04) == 0:
				zsv_ext2 -= 2
				dz_ext2 += 2
			else:
				wsv_ext2 -= 2
				dw_ext2 += 2

		dx4 = dx0 - 1 - 3 * _opensimplex_squish4D
		dy4 = dy0 - 1 - 3 * _opensimplex_squish4D
		dz4 = dz0 - 1 - 3 * _opensimplex_squish4D
		dw4 = dw0 - 3 * _opensimplex_squish4D
		attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4 - dw4 * dw4
		if attn4 > 0:
			attn4 *= attn4
			value += attn4 * attn4 * _opensimplex_extrapolate4D(xsb + 1, ysb + 1, zsb + 1, wsb + 0, dx4, dy4, dz4, dw4)

		dx3 = dx4
		dy3 = dy4
		dz3 = dz0 - 3 * _opensimplex_squish4D
		dw3 = dw0 - 1 - 3 * _opensimplex_squish4D
		attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3 - dw3 * dw3
		if attn3 > 0:
			attn3 *= attn3
			value += attn3 * attn3 * _opensimplex_extrapolate4D(xsb + 1, ysb + 1, zsb + 0, wsb + 1, dx3, dy3, dz3, dw3)

		dx2 = dx4
		dy2 = dy0 - 3 * _opensimplex_squish4D
		dz2 = dz4
		dw2 = dw3
		attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2 - dw2 * dw2
		if attn2 > 0:
			attn2 *= attn2
			value += attn2 * attn2 * _opensimplex_extrapolate4D(xsb + 1, ysb + 0, zsb + 1, wsb + 1, dx2, dy2, dz2, dw2)

		dx1 = dx0 - 3 * _opensimplex_squish4D
		dz1 = dz4
		dy1 = dy4
		dw1 = dw3
		attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1 - dw1 * dw1
		if attn1 > 0:
			attn1 *= attn1
			value += attn1 * attn1 * _opensimplex_extrapolate4D(xsb + 0, ysb + 1, zsb + 1, wsb + 1, dx1, dy1, dz1, dw1)

		dx5 = dx0 - 1 - 2 * _opensimplex_squish4D
		dy5 = dy0 - 1 - 2 * _opensimplex_squish4D
		dz5 = dz0 - 0 - 2 * _opensimplex_squish4D
		dw5 = dw0 - 0 - 2 * _opensimplex_squish4D
		attn5 = 2 - dx5 * dx5 - dy5 * dy5 - dz5 * dz5 - dw5 * dw5
		if attn5 > 0:
			attn5 *= attn5
			value += attn5 * attn5 * _opensimplex_extrapolate4D(xsb + 1, ysb + 1, zsb + 0, wsb + 0, dx5, dy5, dz5, dw5)

		dx6 = dx0 - 1 - 2 * _opensimplex_squish4D
		dy6 = dy0 - 0 - 2 * _opensimplex_squish4D
		dz6 = dz0 - 1 - 2 * _opensimplex_squish4D
		dw6 = dw0 - 0 - 2 * _opensimplex_squish4D
		attn6 = 2 - dx6 * dx6 - dy6 * dy6 - dz6 * dz6 - dw6 * dw6
		if attn6 > 0:
			attn6 *= attn6
			value += attn6 * attn6 * _opensimplex_extrapolate4D(xsb + 1, ysb + 0, zsb + 1, wsb + 0, dx6, dy6, dz6, dw6)

		dx7 = dx0 - 1 - 2 * _opensimplex_squish4D
		dy7 = dy0 - 0 - 2 * _opensimplex_squish4D
		dz7 = dz0 - 0 - 2 * _opensimplex_squish4D
		dw7 = dw0 - 1 - 2 * _opensimplex_squish4D
		attn7 = 2 - dx7 * dx7 - dy7 * dy7 - dz7 * dz7 - dw7 * dw7
		if attn7 > 0:
			attn7 *= attn7
			value += attn7 * attn7 * _opensimplex_extrapolate4D(xsb + 1, ysb + 0, zsb + 0, wsb + 1, dx7, dy7, dz7, dw7)

		dx8 = dx0 - 0 - 2 * _opensimplex_squish4D
		dy8 = dy0 - 1 - 2 * _opensimplex_squish4D
		dz8 = dz0 - 1 - 2 * _opensimplex_squish4D
		dw8 = dw0 - 0 - 2 * _opensimplex_squish4D
		attn8 = 2 - dx8 * dx8 - dy8 * dy8 - dz8 * dz8 - dw8 * dw8
		if attn8 > 0:
			attn8 *= attn8
			value += attn8 * attn8 * _opensimplex_extrapolate4D(xsb + 0, ysb + 1, zsb + 1, wsb + 0, dx8, dy8, dz8, dw8)

		dx9 = dx0 - 0 - 2 * _opensimplex_squish4D
		dy9 = dy0 - 1 - 2 * _opensimplex_squish4D
		dz9 = dz0 - 0 - 2 * _opensimplex_squish4D
		dw9 = dw0 - 1 - 2 * _opensimplex_squish4D
		attn9 = 2 - dx9 * dx9 - dy9 * dy9 - dz9 * dz9 - dw9 * dw9
		if attn9 > 0:
			attn9 *= attn9
			value += attn9 * attn9 * _opensimplex_extrapolate4D(xsb + 0, ysb + 1, zsb + 0, wsb + 1, dx9, dy9, dz9, dw9)

		dx10 = dx0 - 0 - 2 * _opensimplex_squish4D
		dy10 = dy0 - 0 - 2 * _opensimplex_squish4D
		dz10 = dz0 - 1 - 2 * _opensimplex_squish4D
		dw10 = dw0 - 1 - 2 * _opensimplex_squish4D
		attn10 = 2 - dx10 * dx10 - dy10 * dy10 - dz10 * dz10 - dw10 * dw10
		if attn10 > 0:
			attn10 *= attn10
			value += attn10 * attn10 * _opensimplex_extrapolate4D(xsb + 0, ysb + 0, zsb + 1, wsb + 1, dx10, dy10, dz10, dw10)

	attn_ext0 = 2 - dx_ext0 * dx_ext0 - dy_ext0 * dy_ext0 - dz_ext0 * dz_ext0 - dw_ext0 * dw_ext0
	if attn_ext0 > 0:
		attn_ext0 *= attn_ext0
		value += attn_ext0 * attn_ext0 * _opensimplex_extrapolate4D(xsv_ext0, ysv_ext0, zsv_ext0, wsv_ext0, dx_ext0, dy_ext0, dz_ext0, dw_ext0)

	attn_ext1 = 2 - dx_ext1 * dx_ext1 - dy_ext1 * dy_ext1 - dz_ext1 * dz_ext1 - dw_ext1 * dw_ext1
	if attn_ext1 > 0:
		attn_ext1 *= attn_ext1
		value += attn_ext1 * attn_ext1 * _opensimplex_extrapolate4D(xsv_ext1, ysv_ext1, zsv_ext1, wsv_ext1, dx_ext1, dy_ext1, dz_ext1, dw_ext1)

	attn_ext2 = 2 - dx_ext2 * dx_ext2 - dy_ext2 * dy_ext2 - dz_ext2 * dz_ext2 - dw_ext2 * dw_ext2
	if attn_ext2 > 0:
		attn_ext2 *= attn_ext2
		value += attn_ext2 * attn_ext2 * _opensimplex_extrapolate4D(xsv_ext2, ysv_ext2, zsv_ext2, wsv_ext2, dx_ext2, dy_ext2, dz_ext2, dw_ext2)

	return value / 30

_opensimplex_squish2D = 0.366025403784439
_opensimplex_squish3D = 1.0 / 3
_opensimplex_squish4D = 0.309016994374947
_opensimplex_perm = [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]
_opensimplex_perm3D = [21,48,51,57,54,45,33,39,27,69,0,15,6,51,21,27,60,36,21,18,63,66,24,9,39,0,63,30,69,66,18,12,21,0,54,9,0,6,15,42,66,36,9,33,63,33,33,24,27,27,27,48,63,15,24,45,18,60,15,48,9,0,60,21,6,63,69,42,57,0,9,66,15,6,42,45,33,45,39,6,36,57,39,42,12,27,60,51,21,66,15,48,12,18,69,18,51,3,45,51,3,0,24,3,51,12,36,57,48,51,54,3,24,12,45,30,60,60,45,42,60,12,39,18,15,54,9,48,12,3,30,30,12,9,15,30,42,9,66,18,45,30,39,60,45,42,33,33,69,48,30,51,42,63,12,54,21,45,6,63,69,24,24,6,60,30,57,66,15,27,15,33,69,57,12,27,27,66,45,39,57,6,36,42,21,51,24,48,30,51,48,24,6,18,3,36,33,30,6,3,66,54,0,36,69,33,54,3,27,9,3,57,27,42,69,33,3,0,66,21,39,21,30,39,48,36,36,24,57,3,6,63,21,12,18,42,54,60,39,63,18,54,57,15,0,0,9,63,24,9,18,54,69,39,36,36]
_opensimplex_gradients2D = [5,2,2,5,-5,2,-2,5,5,-2,2,-5,-5,-2,-2,-5]
_opensimplex_gradients3D = [-11,4,4,-4,11,4,-4,4,11,11,4,4,4,11,4,4,4,11,-11,-4,4,-4,-11,4,-4,-4,11,11,-4,4,4,-11,4,4,-4,11,-11,4,-4,-4,11,-4,-4,4,-11,11,4,-4,4,11,-4,4,4,-11,-11,-4,-4,-4,-11,-4,-4,-4,-11,11,-4,-4,4,-11,-4,4,-4,-11]
_opensimplex_gradients4D = [3,1,1,1,1,3,1,1,1,1,3,1,1,1,1,3,-3,1,1,1,-1,3,1,1,-1,1,3,1,-1,1,1,3,3,-1,1,1,1,-3,1,1,1,-1,3,1,1,-1,1,3,-3,-1,1,1,-1,-3,1,1,-1,-1,3,1,-1,-1,1,3,3,1,-1,1,1,3,-1,1,1,1,-3,1,1,1,-1,3,-3,1,-1,1,-1,3,-1,1,-1,1,-3,1,-1,1,-1,3,3,-1,-1,1,1,-3,-1,1,1,-1,-3,1,1,-1,-1,3,-3,-1,-1,1,-1,-3,-1,1,-1,-1,-3,1,-1,-1,-1,3,3,1,1,-1,1,3,1,-1,1,1,3,-1,1,1,1,-3,-3,1,1,-1,-1,3,1,-1,-1,1,3,-1,-1,1,1,-3,3,-1,1,-1,1,-3,1,-1,1,-1,3,-1,1,-1,1,-3,-3,-1,1,-1,-1,-3,1,-1,-1,-1,3,-1,-1,-1,1,-3,3,1,-1,-1,1,3,-1,-1,1,1,-3,-1,1,1,-1,-3,-3,1,-1,-1,-1,3,-1,-1,-1,1,-3,-1,-1,1,-1,-3,3,-1,-1,-1,1,-3,-1,-1,1,-1,-3,-1,1,-1,-1,-3,-3,-1,-1,-1,-1,-3,-1,-1,-1,-1,-3,-1,-1,-1,-1,-3]

def _opensimplex_extrapolate2D(xsb, ysb, dx, dy):
	""" 2D extrapolation """
	index = _opensimplex_perm[(_opensimplex_perm[xsb & 0xFF] + ysb) & 0xFF] & 0x0E
	return _opensimplex_gradients2D[index] * dx + _opensimplex_gradients2D[index + 1] * dy

def _opensimplex_extrapolate3D(xsb, ysb, zsb, dx, dy, dz):
	""" 3D extrapolation """
	index = _opensimplex_perm3D[(_opensimplex_perm[(_opensimplex_perm[xsb & 0xFF] + ysb) & 0xFF] + zsb) & 0xFF]
	return _opensimplex_gradients3D[index] * dx + _opensimplex_gradients3D[index + 1] * dy + _opensimplex_gradients3D[index + 2] * dz

def _opensimplex_extrapolate4D(xsb, ysb, zsb, wsb, dx, dy, dz, dw):
	""" 4D extrapolation """
	index = _opensimplex_perm[(_opensimplex_perm[(_opensimplex_perm[(_opensimplex_perm[xsb & 0xFF] + ysb) & 0xFF] + zsb) & 0xFF] + wsb) & 0xFF] & 0xFC
	return _opensimplex_gradients4D[index] * dx + _opensimplex_gradients4D[index + 1] * dy + _opensimplex_gradients4D[index + 2] * dz + _opensimplex_gradients4D[index + 3] * dw

# WAVELET ---------------------------------------------------------------------

# VORONOI ---------------------------------------------------------------------

# WORLEY ----------------------------------------------------------------------

# BILLOW ----------------------------------------------------------------------

# RIDGED ----------------------------------------------------------------------
