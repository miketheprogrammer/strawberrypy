from setuptools import setup, find_packages

import strawberry


setup(
    name='strawberry',
    version='0.1a',
    description="Strawberry Py is a lightweight RESTFull (No Auth Yet) API Server. It is fast, efficient, and simple. Thats all. This version of Strawberry Py also includes my MongoDB Relational Mapper and schema versioner called Mongitude While both StrawberryPy and Mongitude are far from finished they sport some interesting functionality.",
    long_description='None',
    classifiers=[
        "Development Status :: 1 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Self",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: RESTfull Server",
        "Topic :: Internet :: WWW/HTTP :: MongoDB Relational Versioner",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='mongodb',
    author='Michael Hernandez',
    author_email='michael.hernandez1988@gmail.com',
    url='http://github.com/',
    license='MIT',
    packages=find_packages(exclude=['examples', 'lib']),
    include_package_data=True,
    install_requires=['cherrypy', 'pymongo'],
    zip_safe=False,
)