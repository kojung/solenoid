#!/bin/bash

set -e

./lint.sh
./typecheck.sh
./unit_tests.sh
