#!/bin/sh

cd ../shuup-packages/ || exit
for d in */ ; do
    echo "Starting to build_resources on $d"
    cd "$d"
    python setup.py build_resources
    echo "Finished to build_resources on $d"
    cd ..
done
echo "Done"
