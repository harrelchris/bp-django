#!/usr/bin/env bash

VENV=".venv"

# Activate virtual environment
source $VENV/bin/activate

python3 -m black app

python3 -m flake8 app
