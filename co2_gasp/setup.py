import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="co2_gasp",
    version="1",
    author="Hamish Robertson",
    author_email="h(dot)alastair(dot)r@gmail.com",
    description="CO2 GASP PACKAGING",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hammytheham//CO2_GASP_PROGRAM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
