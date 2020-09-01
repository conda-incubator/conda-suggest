import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="conda-suggest",
    version="0.1.0",
    author="Anthony Scopatz",
    description="Conda Suggest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/conda-incubator/conda-suggest",
    packages=['conda_suggest'],
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "conda-suggest = conda_suggest.main:main",
        ],
    },
)
