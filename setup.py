import os

from setuptools import setup
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))
__version__ = None

with open(os.path.join(here, 'README.md')) as f:
    README = f.read().rstrip('\n')
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read().rstrip('\n')
with open(os.path.join(here, 'requirements', 'core.txt')) as _file:
    REQUIREMENTS = [line.rstrip('\n') for line in _file.readlines()]
with open(os.path.join(here, 'requirements', 'test.txt')) as _file:
    TEST_REQUIREMENTS = REQUIREMENTS
    TEST_REQUIREMENTS += [line.rstrip('\n') for line in _file.readlines()]
with open(os.path.join(here, 'flask_avro', 'version.py')) as _file:
    exec(_file.read())


setup(
    name='flask-avro',
    version=__version__,
    description='Simple AVRO IPC endpoint registration for Flask',
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/packagelib/flask-avro',
    author='Jeffrey Starker',
    author_email='jstarker@gmail.com',
    license='Apache License (2.0)',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Framework :: Flask',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='flask avro',
    packages=find_packages(exclude=['tests']),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite='tests'
)
