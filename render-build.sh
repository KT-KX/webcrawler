#!/usr/bin/env bash
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium --with-deps
