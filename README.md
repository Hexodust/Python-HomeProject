# Docker Container Provisioning Tool

This Python tool allows for the programmatic provisioning of Docker containers on virtual networks. It is designed to facilitate the setup, testing, and cleanup of Docker containers for various use cases, such as network testing, development environments, or security research.

## Features

- **Create Docker Containers**: Automatically create multiple Docker containers based on Alpine Linux, with customizable names and hostnames.

- **Network Setup**: Create a Docker network and connect the containers to it for seamless communication.

- **Network Testing**: Test the network connectivity by pinging each target container from the attacker container, ensuring 0% packet loss.

- **Cleanup**: Safely remove the Docker containers and network after completing the tasks, ensuring proper resource management.

## Requirements

- Python 3.x
- Docker
- Click

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/docker-container-provisioning.git
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure Docker is installed and running on your system.

## Usage

Run the provided command-line Python script to perform Docker container provisioning:

```bash
python cli.py <command> [options]
```

Available commands:

- create-containers: Create Docker containers.
- setup-network: Set up a Docker network and connect containers to it.
- test-network: Test network connectivity between containers.
- cleanup: Remove Docker containers and optionally the associated network.
- Use --help option with any command to see available options and usage details.

## Documentation
Detailed documentation for each command and its options is available in the docstrings of the cli.py file. Run python cli.py --help to see the list of available commands and python cli.py <command> --help for usage details of a specific command.


# Project made by Paul-Gabriel Tanase
