#!/bin/bash

# A simple script to add, commit, and push changes to GitHub

# Check if a commit message was provided as an argument
if [ -z "$1" ]; then
  echo "Usage: ./push.sh \"Your commit message here\""
  exit 1
fi

COMMIT_MESSAGE="$1"
BRANCH_NAME="main" # Or "master", depending on your default branch

echo "Staging all changes..."
git add .

echo "Committing changes with message: \"$COMMIT_MESSAGE\""
git commit -m "$COMMIT_MESSAGE"

# Check if the commit was successful (e.g., if there were actual changes to commit)
if [ $? -ne 0 ]; then
  echo "No changes to commit or commit failed. Exiting."
  exit 0
fi

echo "Pushing to $BRANCH_NAME branch..."
git remote add origin https://github.com/nicholasjameshall/srs_api.git
git push origin "$BRANCH_NAME"

# Check if the push was successful
if [ $? -eq 0 ]; then
  echo "Successfully pushed to GitHub!"
else
  echo "Error: Failed to push changes."
fi
