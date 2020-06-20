from ynabdashetl import __version__
from setuptools import setup, find_packages

setup(
    name='ynab-dash-etl',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ynab-sdk-python@git+https://github.com/bljustice/ynab-sdk-python.git@master'
    ],
    python_requires='>=3'
)
