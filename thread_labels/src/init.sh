#! /bin/bash

cd /src
npm i 
npx puppeteer browsers install chrome
node script.js $1 $2 $3
