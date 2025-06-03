# Check if the virtual environment directory exists
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    # Create the virtual environment using python3
    python3 -m venv "env"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please ensure python3 and venv are installed."
        exit 1
    fi
else
    echo "Virtual environment 'env' already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "env/bin/activate"
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

# Start Docker Compose for Elasticsearch in pyelastic
echo "Starting Elasticsearch with Docker Compose..."
(cd pyelastic && docker-compose up -d)
if [ $? -ne 0 ]; then
    echo "Failed to start Docker Compose in pyelastic."
    exit 1
fi

# Run main.py in pyelastic in the background
(cd pyelastic && source ../env/bin/activate && python main.py) &
MAIN_PID=$!

# Install npm dependencies for Frontend
cd Frontend
npm install --legacy-peer-deps
if [ $? -ne 0 ]; then
    echo "Failed to install npm dependencies in Frontend."
    exit 1
fi

# Start Frontend using npx nx serve in the background
npx nx serve Frontend &
FRONTEND_PID=$!
cd ..

# Wait a few seconds for the server to start, then open the app in the browser
sleep 5
open http://localhost:4200

