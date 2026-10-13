#!/usr/bin/env bash

uv run collect.py

jq -s '[.[].data.list[] ]' jobs/*.json >jobs.json

uv run insert.py
