#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- بدء تنفيذ سكربت البناء (build.sh) ---"

echo "1. تثبيت اعتماديات Python من requirements.txt..."
pip install -r requirements.txt

echo "2. بدء عملية تثبيت Google Chrome..."
apt-get update
apt-get install -y wget gnupg

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
apt-get -y update
apt-get install -y google-chrome-stable

echo "--- اكتمل تثبيت Google Chrome بنجاح ---"
