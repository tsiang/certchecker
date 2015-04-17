from setuptools import setup, find_packages

import os

requirements = [
    'boto>=2.37.0',
    'click>=4.0'
]

setup(
    name='certchecker',
    description="A tool to check SSL Certificates in AWS",
    version='0.2.2',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    author='Steven Tsiang',
    author_email='steven@scopely.com',
    url='https://github.com/tsiang/certchecker',
    license=open("LICENSE").read(),
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        certchecker=certchecker.__main__:main
    """
)
