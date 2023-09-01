from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in hrms_custom/__init__.py
from hrms_custom import __version__ as version

setup(
	name="hrms_custom",
	version=version,
	description="Hrms customisation",
	author="8848",
	author_email="jay@8848digital.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
