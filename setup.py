from setuptools import setup, find_namespace_packages


name = "filament"


def long_description():
    with open("README.md") as fp:
        return fp.read()


def parse_requirements_file(path):
    with open(path) as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


setup(
    name="filament",
    description="Various add-ons, extensions and utilities for hikari-lightbulb",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="tandemdude",
    author_email="tandemdude1@gmail.com",
    url="https://github.com/tandemdude/filament",
    packages=find_namespace_packages(include=[name + "*"]),
    install_requires=parse_requirements_file("requirements.txt"),
    python_requires=">=3.8.0,<3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: Stackless",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
