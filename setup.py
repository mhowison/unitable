import os
from setuptools import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="unitable",
    version="0.0.1",
    author="Mark Howison",
    author_email="mark@howison.org",
    url="https://github.com/mhowison/unitable",
    keywords=["data", "data analysis", "data frame", "data science"],
    description="A data analysis environment that unites the best features of pandas, R, Stata, and others.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
    ],
    provides=["unitable"],
    packages=["unitable"],
    install_requires=["pandas"]
)
