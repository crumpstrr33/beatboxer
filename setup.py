from setuptools import setup, find_packages
from os import path
import re

with open('README.md', 'r') as f:
    long_description = f.read()

with open(path.join('beatboxer', '__init__.py'), 'r') as f:
    setup_file = f.read()
version = re.findall(r'__version__ = \'(.*)\'', setup_file)[0]
name = re.findall(r'__name__ = \'(.*)\'', setup_file)[0]

with open('requirements.txt', 'r') as f:
    requirements = f.read().split('\n')

setup(
    name=name,
    version=version,
    author='Jacob Scott',
    author_email='jscott12009@gmail.com',
    description='A beatboxer to create custom beats.',
    license='MIT',
    url='https://github.com/crumpstrr33/beatboxer',
    packages=find_packages(),
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    package_data={'beatboxer': [
        'samples/bass.wav',
        'samples/clap.wav',
        'samples/crash.wav',
        'samples/hihat.wav',
        'samples/kick.wav',
        'samples/snare.wav']
    },
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
