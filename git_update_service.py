#!/usr/bin/env python3

import os
import subprocess
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
REPO_PATH = "/path/to/your/repo"  # Update this to your repository path
CHECK_INTERVAL = 300  # Check every 5 minutes (300 seconds)
SERVICE_TO_RESTART = "your_service_name"  # Update this to the name of the service you want to restart

def run_command(command):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e}")
        return None

def check_for_updates():
    """Check if there are any new commits in the remote repository."""
    os.chdir(REPO_PATH)
    run_command("git fetch")
    local_commit = run_command("git rev-parse HEAD")
    remote_commit = run_command("git rev-parse @{u}")
    return local_commit != remote_commit

def pull_updates():
    """Pull the latest changes from the remote repository."""
    os.chdir(REPO_PATH)
    return run_command("git pull")

def restart_service():
    """Restart the specified service."""
    return run_command(f"sudo systemctl restart {SERVICE_TO_RESTART}")

def main():
    while True:
        logging.info("Checking for updates...")
        if check_for_updates():
            logging.info("Updates found. Pulling changes...")
            pull_result = pull_updates()
            if pull_result:
                logging.info("Changes pulled successfully. Restarting service...")
                restart_result = restart_service()
                if restart_result is not None:
                    logging.info("Service restarted successfully.")
                else:
                    logging.error("Failed to restart service.")
            else:
                logging.error("Failed to pull changes.")
        else:
            logging.info("No updates found.")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
