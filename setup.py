from setuptools import setup

setup(
    author='Jeffrey Finkelstein',
    author_email='jeffrey.finkelstein@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    description='A game of collapsing tiles.',
    download_url='http://pypi.python.org/pypi/numbertiles',
    # install_requires=[],
    include_package_data=True,
    # keywords=[],
    license='GNU GPLv3+',
    long_description=__doc__,
    name='Number Tiles',
    platforms='any',
    packages=['numbertiles'],
    test_suite='nose.collector',
    tests_require=['nose'],
    url='http://github.com/jfinkels/numbertiles',
    version='0.0.1-dev',
    # zip_safe=False
)
