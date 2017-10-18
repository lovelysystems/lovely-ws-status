import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.rst')).read()
changes = open(os.path.join(here, 'CHANGES.rst')).read()

requires = ['pyramid']


setup(
    name='lovely-ws-status',
    version='0.1.0',
    description='Service Status Utilities for Pyramid Apps',
    long_description=readme + '\n\n' + changes,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Pyramid",
    ],
    author='Lovely Systems',
    author_email='office@lovelysystems.com',
    url='https://github.com/lovelysystems/lovely-ws-status',
    keywords='pyramid svc status monitoring',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=requires
)
