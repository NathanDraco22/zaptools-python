from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="zaptools",
    version="0.0.6b1",
    url="https://github.com/NathanDraco22/zap-adapter-python",
    license='MIT',

    author="Nathan Mejia",
    author_email="nathandraco22@gmail.com",

    description="Python Implementation to ZapTools WebSockets",
    long_description=long_description,

    packages=[
        "zaptools"
    ],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
    ],
)
