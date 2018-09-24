from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='scroodle',
    version='1.0',
    license="MIT",
    description='IDC Moodle scrapper',
    long_description=long_description,
    author='Tsehori',
    author_email='g.tsehori@gmail.com',
    packages=['scroodle'],
    install_requires=['tabulate', 'robobrowser', 'pandas']
)

