import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-genia",
    version = "0.1dev",
    author = "Taylor Mitchell",
    author_email = "taylor.mitchell@gmail.com",
    description = ("A pluggable Django app for managing generations of data"),
    license = "BSD",
    keywords = "django data generations",
    url = "https://github.com/tmitchell/django-genia",
    packages=['genia',],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)