"""Setup script for ddns-manager"""

import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="ddns-manager",
    version="0.1.1",
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
    install_requires=["click", "PyYAML", "requests", "retry"],
    entry_points={
        "console_scripts": [
            "ddns_manager=ddns_manager.__main__:cli",
        ]
    },
    python_requires=3.6,
)
