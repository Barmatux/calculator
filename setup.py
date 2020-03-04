from setuptools import setup, find_packages
setup(
    name='pycalc',
    version='0.3',
    author='Anton Tsyhankou',
    description='Simple calculator',
    packages= find_packages(),
    entry_points = {'console_scripts':
                    'pycalc = calculator.pycalc:main'},
    install_requires=['setuptools'],
    python_requires='>=3.6'
)