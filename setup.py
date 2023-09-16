from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="zaptools",
    version="0.1.1",
    url="https://github.com/NathanDraco22/zap-adapter-python",
    license='MIT',

    author="Nathan Mejia",
    author_email="nathandraco22@gmail.com",

    description="A toolkit for Event-Driven websocket management",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        "zaptools"
    ],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
    ],
)
