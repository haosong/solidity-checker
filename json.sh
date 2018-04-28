#!/bin/bash

rm -rf ./tmp
mkdir ./tmp
solidity-parser $1 > ./tmp/result.json

