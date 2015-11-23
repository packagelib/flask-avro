from setuptools import setup, find_packages

setup(
    name='flask-avro',
    version='0.0.1',

    description='Simple AVRO IPC endpoint registration for Flask',
    # long_description=long_description,  TODO generate long description.

    url='https://github.com/packagelib/flask-avro',

    author='Jeffrey Starker',
    author_email='jstarker@gmail.com',

    license='MIT',

    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Framework :: Flask',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='flask avro',

    packages=find_packages(exclude=['tests']),
    install_requires=['flask', 'avro'],
    test_suite="tests"
)
