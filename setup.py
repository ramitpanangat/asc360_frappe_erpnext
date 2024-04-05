from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in a3_adventure_sports_cover/__init__.py
from a3_adventure_sports_cover import __version__ as version

setup(
	name="a3_adventure_sports_cover",
	version=version,
	description="Insurance for adventure sports.",
	author="Ramit Panangat",
	author_email="ramit.panangat@acube.co",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
