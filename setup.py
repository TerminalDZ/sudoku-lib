from setuptools import setup, find_packages

setup(
    name="sudoku_lib",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "PySide6>=6.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "pydantic>=2.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "black>=23.0.0",
            "requests>=2.31.0",
            "httpx>=0.24.0",
            "pytest-asyncio>=0.21.0"
        ]
    },
    author="Idriss Boukmouche",
    author_email="boukemoucheidriss@gmail.com",
    description="A comprehensive Sudoku solver and game library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/terminaldz/sudoku_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
