#!/usr/bin/env bash

src="$1"
des="$2"

# Check if both arguments are present
if [[ -z "$src" || -z "$des" ]]; then
    echo "Usage: ./cp.sh <src> <des>"
    exit 1
fi

# # Check if src-style.css is a file
# if [[ ! -f "$src-styles.css" ]]; then
#     echo "Error: $src-styles.css is not a file"
#     exit 1
# fi

# # Check if src-index.html is a file
# if [[ ! -f "$src-index.html" ]]; then
#     echo "Error: $src-index.html is not a file"
#     exit 1
# fi

# Check if des-style.css already exists
if [[ -f "$des-styles.css" ]]; then
    read -p "$des-styles.css already exists, are you sure? (y/n): " response
    if [[ "$response" != "y" ]]; then
        exit 1
    fi
fi

# Check if des-index.html already exists
if [[ -f "$des-index.html" ]]; then
    read -p "$des-index.html already exists, are you sure? (y/n): " response
    if [[ "$response" != "y" ]]; then
        exit 1
    fi
fi

# Copy src-style.css to des-style.css
cp "$src-styles.css" "$des-styles.css"
# cp "$src-index.html" "$des-index.html"

# Replace line 11 of index.html
sed -i "10s/${src}/${des}/" $des-article.html
