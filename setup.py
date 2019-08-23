import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ktis-parser",
    version="0.3.0",
    author="zaeval",
    author_email="zaeval@kookmin.ac.kr",
    description="ktis_parser default information parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zaeval/ktis_parser",
    packages=setuptools.find_packages(),
    license="GPL",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)