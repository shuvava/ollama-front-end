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
REPO_PATH=$(prompt_with_default "Enter the path to your Git repository" "$CURRENT_DIR")
CHECK_INTERVAL=$(prompt_with_default "Enter the check interval in seconds" "300")
SERVICE_TO_RESTART=$(prompt_with_default "Enter the name of the service to restart" "your_service_name")

# Update the Python script with the provided configuration
sed -i "s|REPO_PATH = \"/path/to/your/repo\"|REPO_PATH = \"$REPO_PATH\"|" git_update_service.py
sed -i "s|CHECK_INTERVAL = 300|CHECK_INTERVAL = $CHECK_INTERVAL|" git_update_service.py
sed -i "s|SERVICE_TO_RESTART = \"your_service_name\"|SERVICE_TO_RESTART = \"$SERVICE_TO_RESTART\"|" git_update_service.py

# Make the script executable
chmod +x git_update_service.py

# Create the systemd service file
cat << EOF | sudo tee /etc/systemd/system/git-update.service
[Unit]
Description=Git Update Service
After=network.target

[Service]
ExecStart=$CURRENT_DIR/git_update_service.py
Restart=always
User=$USER
Group=$(id -gn)

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd manager configuration
sudo systemctl daemon-reload

# Start the service
sudo systemctl start git-update

# Enable the service to start on boot
sudo systemctl enable git-update

echo "Git Update Service has been set up and started successfully!"
