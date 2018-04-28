#!/bin/bash

rm -rf ./tmp
mkdir ./tmp
./node_modules/solidity-parser/cli.js $1 > ./tmp/result.json
