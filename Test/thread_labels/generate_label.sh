#! /bin/sh
datamatrix=$1
serial=$2
template=$3

docker run -i -v ./src:/src --init --cap-add=SYS_ADMIN --rm ghcr.io/puppeteer/puppeteer:latest bash /src/init.sh $1 $2 $3
