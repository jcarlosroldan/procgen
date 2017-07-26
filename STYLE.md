Procgen style guide
===================

If you wish to contribute in this project, please follow these style guidelines:

1. Our base style guide is [PEP-8](https://www.python.org/dev/peps/pep-0008/)
2. Tabs are the preferred indentation method
3. Each module package is a script with a set of functions: `noise.py`
4. Each *public* function is wrapped with line separators with the name of the function: `# PERLIN -------`
5. After a line separator, we can find (in the same order):
	1. Public global variables, prefixed with the main function name: `PERLIN_PERSISTENCE = 0.5`
	2. The main function. This is the only non-optional field: `perlin(x, y, z)`
	3. Every other façade: `perlin2D(x,y)`, `perlin1D(x)`
	4. The auxiliar functions and variables, with a leading underscore, the name of the main function, and another underscore: `_perlin_lerp(t, a, b)`, `_perlin_p = [1, 2, 3]`
6. Every function must be shortly documented (even auxiliar ones): `""" Linear interpolation """`, public functions will be properly documented at docs generation stage of the project

The easier way to learn this style is [checking an example](./procgen/noise.py).