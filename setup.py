from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="bencode-python",
    version="0.0.1",
    description="Bencode encoder and decoder written in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zrekryu",
    author_email="zrekryu@gmail.com",
    url="https://github.com/zrekryu/py-bencode",
    keywords=["bencode", "beecode", "torrent", "bittorrent"],
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
        ]
    )