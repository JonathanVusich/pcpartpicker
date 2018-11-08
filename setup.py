from setuptools import setup, find_packages

install_requires = [
                    "aiohttp",
                    "aiodns",
                    "lxml",
                    ]
setup(name="pcpartpicker", packages = find_packages())
