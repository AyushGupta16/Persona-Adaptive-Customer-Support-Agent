#!/bin/bash

echo "Downloading LLaMA 2 7B Q2_K GGUF model..."
FILE_ID="1QBJiKSdJ-_UpYCWCpX3YlGV5oi6gEPlR"
FILE_NAME="llama-2-7b.Q2_K.gguf"

curl -L -o "$FILE_NAME" "https://drive.google.com/uc?export=download&id=${FILE_ID}"

echo "Download complete. Saved as $FILE_NAME"