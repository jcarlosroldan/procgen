Procgen style guide
===================

If you wish to contribute in this project, please follow these style guidelines:

1. Our base style guide is [PEP-8](https://www.python.org/dev/peps/pep-0008/)
2. Tabs are the preferred indentation method
3. Each module is a script with a set of functions: `noise.py`
4. Each *public* function is wrapped with line separators with the name of the function: `# PERLIN -------`
5. After a line separator, we can find (in the same order):
	1. Imports used: only built-in and numpy resources are allowed
	1. Public global variables, prefixed with the main function name: `PERLIN_PERSISTENCE = 0.5`
	2. The main function. This is the only non-optional field: `perlin(x, y, z)`
	3. Every other façade: `perlin2D(x,y)`, `perlin1D(x)`
	4. The auxiliar functions and variables, with a leading underscore, the name of the main function, and another underscore: `_perlin_lerp(t, a, b)`, `_perlin_p = [1, 2, 3]`
6. Every function must be shortly documented (even auxiliar ones): `""" Linear interpolation """`, public functions will be properly documented at docs generation stage of the project
7. Add default values to every possible parameter

The easier way to learn this style is [checking an example](./procgen/noise.py).

## Testing

We will delve into the details of unit testing at other stage of the project. However, there you have some guidelines:

1. We are not using any testing library yet, just `assert`s and visualizations using `matplotlib`
2. Tests are located at tests/`<module_name>`/`<function_name>`
3. Three types of tests should be done:
	1. Functional test: checks that the funcion works as expected. It is usual to check known values here, or to average a set of outputs that should approach to some value
	2. Performance test: checks that the time required to perform a task is smaller than a fixed value
	3. Subjective test (optional): many of these procedural generation techniques are very subjective, and human judgement might be required in some cases, such as checking that default parameters are properly tuned
4. If a visualization is required, use matplotlib `plasma` color map (`cmap` parameter) or another perceptually uniform colormap (`viridis`, `inferno` or `magma`)