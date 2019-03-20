while read -r line; do
    package=$(echo "$line" | cut -f 1 -d ' ')
    if [[ "$package" == *"=="* ]]; then
    if [[ "$package" == *"shuup"* ]]; then
        lepackage=$(echo "$package" | cut -f 1 -d "=")
        pip install -e "$1/$lepackage"
    else
        pip install $package
    fi
    fi
done < requirements.txt
