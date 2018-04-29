#!/bin/bash

rm -rf ../data
mkdir ../data
../node_modules/solidity-parser/cli.js $1 > ../data/ast.json
