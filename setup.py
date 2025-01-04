from setuptools import setup, find_packages

setup(
    name="sudoku_lib",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "PySide6>=6.0.0"
    ],
    author="Idriss Boukmouche",
    author_email="boukemoucheidriss@gmail.com",
    description="A comprehensive Sudoku solver and game library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/terminaldz/sudoku_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
