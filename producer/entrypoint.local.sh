#!/bin/bash

# if any of the commands fails for any reason, the entire script fails
set -o errexit

# fail exit if one of pipe command fails
set -o pipefail

# exits if any of variables is not set
set -o nounset

echo "[RUN SERVER]"
watchmedo auto-restart --recursive --pattern="*.py" --directory="/apps/" python -- -m main
