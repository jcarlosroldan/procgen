from setuptools import find_packages, setup

with open('requirements.txt', 'r', encoding='utf-8') as fp:
    requirements = [r for r in fp.read().split('\n') if len(r)]

setup(
    name="procgen",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3',
    url="https://github.com/juancroldan/procgen",
    author="juancroldan",
    license="MIT",
    install_requires=requirements,
    zip_safe=False
)