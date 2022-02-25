import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(

    name="zaptools",
    version="0.0.1",
    url="https://github.com/kragniz/cookiecutter-pypackage-minimal",
    license='MIT',

    author="Nathan Mejia",
    author_email="nathandraco22@gmail.com",

    description="Python Implementation to ZapTools WebSockets",
    long_description=read("README.rst"),

    packages=[
        "zaptools",
        "zaptools.FastApi",
        "zaptools.customtypes",
        "zaptools.EventRegister",
        "zaptools.models"
    ],

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
