#!/bin/bash

echo "FastApi Service Prompt:"

# Path to the virtual environment
VENV_PATH="/opt/homebrew/bin/fastapilib/bin"
ACTIVATE_SCRIPT="$VENV_PATH/activate"
DEACTIVATE_SCRIPT="$VENV_PATH/deactivate"
PYTHON_EXECUTABLE="$VENV_PATH/python"

while true; do
    read -p "> " userInput
    
    if [ "$userInput" == "activate" ]; then
        source "$ACTIVATE_SCRIPT"
        if [ $? -eq 0 ]; then
            echo "Environment activated successfully! Start Vayo"
        else
            echo "Command failed"
        fi
    elif [ "$userInput" == "deactivate" ]; then
        source "$DEACTIVATE_SCRIPT"
        if [ $? -eq 0 ]; then
            echo "Environment deactivated successfully! Stop Vayo"
            break
        else
            echo "Command failed"
        fi
    elif [ "$userInput" == "installPkg" ]; then
        echo "Installing packages"
        "$PYTHON_EXECUTABLE" -m pip install -r /Users/sagarpoudel/Downloads/transfer/streamlit/requirements.txt
        if [ $? -eq 0 ]; then
            echo "Packages installed."
        else
            echo "Command failed"
        fi
    elif [ "$userInput" == "exit" ]; then
        source "$DEACTIVATE_SCRIPT"
        echo "Exiting the prompt."
        break
    elif [ "$userInput" == "runserver" ]; then
        echo "Starting Server!!!"
        "$PYTHON_EXECUTABLE" streamlit run /Users/sagarpoudel/Downloads/transfer/streamlit/streamlitapp.py
    else
        eval "$userInput"
    fi
done
