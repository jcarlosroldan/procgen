Procgen: Procedural generation library
======================================

Procgen is a fast general purpose procedural generation library for Python. It can be used for a widde range of purposes, from terrain generation to generative art, both in 2D and 3D worlds.

**Warning:** This library is currently under development. Several API changes are expected until an stable version is reached.

## Requirements

* Python 3.2+
* Numpy 1.10+
* Works on Linux, Windows, Mac OSX, BSD

## Install

To install Procgen, simply:

```
pip install numpy -U
git clone https://github.com/juancroldan/procgen.git
```

Soon, you will be able to use pip to install this library.

## Documentation

Since big API changes are expected, documentation is not available yet. We will upload it to readthedocs.org soon.

## Contribute

By January 2018, a 1.0 stable version will be released, a proper branch workflow will be used, and contributions will be open. Adventurous coders can contact with [juancarlos@sevilla.es](mailto:juancarlos@sevilla.es) to contribute in this wild, unstable stage.

## Current work

Currenty, we are working to provide a basic set of algorithms for procedural generation.

We are implementing algorithms from the following sources:

* [Procedural generation gamasutra example](http://www.gamasutra.com/blogs/JonGallant/20160211/264591/Procedurally_Generating_Wrapping_World_Maps_in_Unity_C__Part_4.php)
* [Procedural generation wiki](http://pcg.wikidot.com/)
* [Procedural Content Generation in Games book](http://pcgbook.com/)
* [Procedural generation subreddit](https://www.reddit.com/r/proceduralgeneration/)
* [Procgen Github projects](https://github.com/search?l=Python&q=procedural+generation&type=Repositories&utf8=%E2%9C%93)

Our backlog is:

1. Noise initialisation: `seed`
2. Lattice-based noise functions: `perlin`, `simplex`, `opensimplex`, `wavelet`
3. Point-based noise functions: `voronoi`, `worley`
4. Perlin-based noise functions: `billow`, `ridged`
5. Test coverage for noise functions
6. Biome generation: [`whittaker`](http://www.jgallant.com/procedurally-generating-wrapping-world-maps-in-unity-csharp-part-4/)
7. Tree-placement algorithms
8. Water-placement algorithms: rivers, lakes, wind-aware filling
9. Test coverage for terrain functions
10. Backlog update: [Cellullar automata](https://www.hermetic.ch/pca/tg.htm), L-systems, [boolean evaluation heightmap](https://sites.google.com/site/mddn442/research-topics/procedural-terrains-cities-and-worlds)...
11. Version 1.0 is reached: issue-driven development, pull requests opened, dev branch, examples in wiki, automatic tests, setup.py to use pip install git+git://
