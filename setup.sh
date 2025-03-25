#!/bin/bash

set -e
echo "scrapper-app-surtidos setup"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "venv created."
else
    echo "venv alredy exists."
fi

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup completed successfully!"
