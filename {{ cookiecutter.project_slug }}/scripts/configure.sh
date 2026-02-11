#!/usr/bin/env bash

# This script prepares the development environment.
# It installs all relevant packages and creates a template .env file.

uv sync

uv run pre-commit install

cat > .env <<EOL

EOL
