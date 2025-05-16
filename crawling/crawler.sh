#!/bin/bash

# Define the virtual environment directory name
VENV_DIR="env"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    # Create the virtual environment using python3
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please ensure python3 and venv are installed."
        exit 1
    fi
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install requirements."
        # Optionally deactivate and exit if install fails
        # deactivate
        # exit 1
    fi
else
    echo "requirements.txt not found. Skipping installation."
fi

# Run the main Python script if it exists
if [ -f "main.py" ]; then
    echo "Running main.py..."
    MAX_WORKERS=8 python main.py
else
    echo "main.py not found."
fi

# Deactivate the virtual environment (optional, script execution ends anyway)
# echo "Deactivating virtual environment..."
# deactivate

echo "Script finished."
exit 0