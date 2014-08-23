from setuptools import setup

setup(
    name='party',
    version='1.5.3',
    author='Ted Sheibar',
    author_email='tsheibar@gmail.com',
    packages=['party'],
    package_dir={'party': 'party'},
    package_data={'':['README.md']},
    include_package_data=True,
    url='http://pypi.python.org/pypi/Party/',
    license='LICENSE.txt',
    description='Lightweight Python client to the Artifactory API.',
    long_description=open('README.md').read(),
    install_requires=[
        "requests>=2.3.0",
        "wsgiref>=0.1.2",
    ],
)
