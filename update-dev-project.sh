#!/bin/sh

while read -r line; do
    package=$(echo "$line" | cut -f 1 -d ' ')
    if [[ "$package" == *"=="* ]]; then
    if [[ "$package" == *"shuup"* ]]; then
        lepackage=$(echo "$package" | cut -f 1 -d "=")
        if [ -d "/$1/$lepackage/" ]; then
            pip install -e "/$1/$lepackage" || exit
        else
            pip install --find-links=/app/wheels $package || exit
        fi
    else
        pip install $package || exit
    fi
    fi
done < requirements.txt
