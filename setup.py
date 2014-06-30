from distutils.core import setup

setup(
    name='Party',
    version='1.5.0',
    author='Ted Sheibar',
    author_email='tsheibar@gmail.com',
    packages=['party'],
    url='http://pypi.python.org/pypi/Party/',
    license='LICENSE.txt',
    description='Lightweight Python client to the Artifactory API.',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests>=2.3.0",
        "wsgiref>=0.1.2",
    ],
)
