#!/usr/bin/env bash

poetry install
poetry run pre-commit autoupdate
