#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.
set -euo pipefail
echo conda activate
conda activate myenv
echo run python
exec python server.py