#!/bin/sh

# These are disabled until the resource building in the container is improved
# echo "Running update-dev-project.sh"
# bash update-dev-project.sh shuup-packages

echo "Running bash -c 'tail -f /dev/null' so that the container won't stop"
bash -c 'tail -f /dev/null'

echo "Done"
