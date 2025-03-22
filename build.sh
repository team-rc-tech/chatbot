#!/bin/bash
# Extract the .zip file
unzip rasa-chatbot.zip -d .
# Navigate into the rasa-deploy folder
cd rasa-deploy/
# Install dependencies
pip install -r requirements.txt
