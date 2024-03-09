import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='automython',
    version='1.0.2',
    description='A simplistic programming language interpreter to Python to help students grasp finite automata theory programmatically and with a computed graph through visualization libraries.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/mkantrr/automython',
    author='Matthew Kanter',
    author_email='matt@matutu.dev',
    license='MIT',
    keywords=['automata', "finite", 'compiler', 'interpreter', 'theory', 'computational theory', "non-deterministic", "turing", "machine", "state"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    package_dir={'':'src'},
    packages=find_packages('src'),
    install_requires=[
        "automata-lib[visual]",
        "pandas",
        "ipython"
    ],
    entry_points={
        'console_scripts': [
            'automython=interpreter:interpret'
        ]
    }
)