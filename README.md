## Status

| Bintray | Linux/macOS |
|:--------:|:-----------------:|
|[![Download](https://api.bintray.com/packages/morheit/conan/fizz%3Amorheit/images/download.svg)](https://bintray.com/morheit/conan/fizz%3Amorheit/2019.11.11.00%3Astable)|[![Build Status](https://travis-ci.org/Morheit/conan-fizz.svg?branch=stable%2F2019.11.11.00)](https://travis-ci.org/Morheit/conan-fizz)|

## Conan Recipe for [*Fizz*](https://github.com/facebookincubator/fizz)

Fizz is a TLS 1.3 implementation

The packages generated with conanfile from this repository can be found on [Bintray](https://bintray.com/morheit/conan/fizz%3Amorheit/).

## Setup

### Basic Setup

    $ conan remote add conan-morheit https://api.bintray.com/conan/morheit/conan
    $ conan install fizz/2019.11.11.00@morheit/stable

### Project Setup

For project setup specify the package in your *conanfile.txt*
```
[requires]
fizz/2019.11.11.00@morheit/stable

[generators]
cmake
```
