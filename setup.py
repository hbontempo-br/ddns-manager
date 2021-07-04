"""Setup script for ddns-manager"""

import os.path
from os import environ

from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as f:
    README = f.read()

# Parsing requirements files
with open(os.path.join(HERE, "requirements.txt")) as f:
    REQUIREMENTS = f.read().splitlines()

# Extracting version from environment variable
VERSION = environ.get("VERSION")
if VERSION == "":
    raise EnvironmentError("Invalid VERSION")

setup(
    name="ddns-manager",
    version=VERSION,
    description="Keep your ddns up to date",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hbontempo-br/ddns-manager",
    author="hbontempo-br",
    author_email="me@hbontempo.dev",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "ddns_manager=ddns_manager.__main__:cli",
        ]
    },
    python_requires=">=3.6",
)
