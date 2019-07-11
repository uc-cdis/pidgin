#!/bin/bash

MYVAR="deploy"
zip from_travis_$MYVAR.zip lambda_function.py

# zip from_travis_$TRAVIS_BRANCH.zip lambda_function.py
# aws lambda publish-version --function-name from_travis_$TRAVIS_BRANCH
