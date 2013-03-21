from setuptools import setup, find_packages

import strawberry


setup(
    name='strawberry',
    version='0.1',
    description="An introspective interface for Django and MongoDB",
    long_description='None',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Self",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
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