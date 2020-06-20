from setuptools import setup, find_packages

setup(
    name='YNAB Dash ETL',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['ynab-sdk-python<1'],
    python_requires='>=3'
)
