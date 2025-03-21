#! /usr/bin/env bash

VERSION=2.0.6

if [ ! -d "libRadtran-${VERSION}" ]
then
    wget https://www.libradtran.org/download/libRadtran-${VERSION}.tar.gz
    tar -xzf libRadtran-${VERSION}.tar.gz
    rm libRadtran-${VERSION}.tar.gz
    cd libRadtran-${VERSION}
    ./configure
    make
    make
    make
    make check
    cd ..
fi