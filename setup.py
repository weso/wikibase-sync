from setuptools import setup
from os import path

curr_dir = path.abspath(path.dirname(__file__))
with open(path.join(curr_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wbsync',
    version='0.1.3',
    packages=['wbsync', 'wbsync.external', 'wbsync.synchronization',
              'wbsync.triplestore', 'wbsync.util',
              'rdfsync', 'rdfsync.util', 'rdfsync.githubcon', 'rdfsync.wb2rdf'],
    url='https://github.com/weso/rdf-wb-sync',
    license='MIT',
    author='Alejandro González Hevia, Othmane Bakhtaoui',
    author_email='alejandrgh11@gmail.com, b.othmane98@live.fr',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests==2.23.0', 'rdflib==5.0.0', 'ontospy==1.9.8.3',
        'PyGithub==1.53', 'pytest~=6.1.0', 'python-dateutil~=2.8.1'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ]
)
