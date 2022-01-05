import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
# install_requires
setup(
    name="super8",
    version="0.1.0",
    description="open-source toolset for video analysis",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/blancai/super8",
    author="Rich Pavlovskiy",
    author_email="rich.pavlovskiy@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
		packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "super8=super8.__main__:main",
        ]
    },
)

