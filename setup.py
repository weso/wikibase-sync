from setuptools import setup
from os import path

curr_dir = path.abspath(path.dirname(__file__))
with open(path.join(curr_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wbsync',
    version='0.1.4',
    packages=['wbsync', 'wbsync.external', 'wbsync.synchronization',
              'wbsync.triplestore', 'wbsync.util',
              'rdfsync', 'rdfsync.util', 'rdfsync.githubcon', 'rdfsync.wb2rdf'],
    url='https://github.com/weso/rdf-wb-sync',
    license='MIT',
    author='Alejandro González Hevia, Othmane Bakhtaoui, Enrique J Rodriguez, Angel García-Menéndez',
    author_email='alejandrgh11@gmail.com, b.othmane98@live.fr, rodriguezmenrique@uniovi.es, garciamenangel@uniovi.es',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests==2.32.3', 'rdflib==7.1.3', 'ontospy==2.1.1',
        'PyGithub==2.5.0', 'pytest~=8.3.4', 'python-dateutil~=2.9.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ]
)
