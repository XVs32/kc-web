#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

script/.venv/bin/python script/fetch-master.py "${1:-public/master_bk}" 
