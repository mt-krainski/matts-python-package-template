#!/usr/bin/env bash

# This script prepares the development envrionment.
# It installs all relevant plugins, additional packages
# and creates a template .env file.

poetry install

poetry -q self add poetry-plugin-dotenv
poetry run pre-commit install

cat > .env <<EOL

EOL
