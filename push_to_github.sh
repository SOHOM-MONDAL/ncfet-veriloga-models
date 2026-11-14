#!/usr/bin/env bash
# Usage: ./push_to_github.sh https://github.com/<your-username>/nc-tfet-verilog-a.git
set -e
if [ -z "$1" ]; then echo "Usage: $0 <github-repo-url>"; exit 1; fi
git init
git add .
git commit -m "Initial commit: NC-TFET Verilog-A models, Spectre testbenches, results"
git branch -M main
git remote add origin "$1"
git push -u origin main
