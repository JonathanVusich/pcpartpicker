import os
from setuptools import setup, find_packages


def read(file_name: str):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="pcpartpicker",
    version="2.2.0",
    author="Jonathan Vusich",
    author_email="jonathanvusich@gmail.com",
    description="A fast, simple API for PCPartPicker.com.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="GPL",
    keywords="pcpartpicker api webscraper python3",
    url="https://github.com/JonathanVusich/pcpartpicker",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "utils"]),
    install_requires=read("requirements.txt"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
