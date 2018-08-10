import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.rst')).read()


def get_version():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION.txt")
    with open(p) as f:
        return f.read().strip()


setup(
    name='lovely-ws-status',
    version=get_version(),
    description='Service Status Utilities for Pyramid Apps',
    long_description=readme,
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Framework :: Pyramid"
    ],
    author='Lovely Systems',
    author_email='office@lovelysystems.com',
    url='https://github.com/lovelysystems/lovely-ws-status',
    keywords='pyramid service status monitoring prometheus',
    namespace_packages=['lovely', 'lovely.ws'],
    packages=['lovely.ws.status'],
    package_dir={'': 'src'},
    zip_safe=True,
    install_requires=['pyramid>=1.9.1'],
    license='Apache License 2.0',
    data_files=('LICENSE', 'VERSION.txt', 'README.rst')
)
