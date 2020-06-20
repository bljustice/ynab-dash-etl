from ynabdashetl import __version__
from setuptools import setup, find_packages

setup(
    name='YNAB Dash ETL',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['ynab-sdk-python<1'],
    python_requires='>=3'
)
