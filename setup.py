from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in automail/__init__.py
from automail import __version__ as version

setup(
	name="automail",
	version=version,
	description="Auto Mail for specific time peroid for auto mail report DocType",
	author="Prashant Kamble",
	author_email="kambleprashant@outlook.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
