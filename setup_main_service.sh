#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to prompt for input with a default value
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    read -p "$prompt [$default]: " input
    echo "${input:-$default}"
}

# Get current directory
CURRENT_DIR=$(pwd)

# Prompt for configuration
APP_NAME=$(prompt_with_default "Enter the name for your service" "fastapi-app")
APP_PATH=$(prompt_with_default "Enter the path to your app/main.py file" "$CURRENT_DIR/app/main.py")
HOST=$(prompt_with_default "Enter the host to bind to" "0.0.0.0")
PORT=$(prompt_with_default "Enter the port to bind to" "8000")
WORKERS=$(prompt_with_default "Enter the number of worker processes" "4")

# Create the systemd service file
cat << EOF | sudo tee /etc/systemd/system/"$APP_NAME".service
[Unit]
Description=FastAPI application running with Uvicorn
After=network.target

[Service]
User=$USER
Group=$(id -gn)
WorkingDirectory=$(dirname $APP_PATH)
Environment="PATH=$PATH"
ExecStart=$(which uvicorn) main:app --host $HOST --port $PORT --workers $WORKERS
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd manager configuration
sudo systemctl daemon-reload

# Start the service
sudo systemctl start $APP_NAME

# Enable the service to start on boot
sudo systemctl enable $APP_NAME

echo "$APP_NAME service has been set up and started successfully!"
echo "You can check its status with: sudo systemctl status $APP_NAME"
