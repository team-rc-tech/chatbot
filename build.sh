#!/bin/bash
# Upgrade pip
pip install --upgrade pip
# Extract the .zip file
unzip rasa-chatbot.zip -d .
# Install dependencies
pip install -r requirements.txt
