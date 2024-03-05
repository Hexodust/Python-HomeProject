
from typing import List

import docker
from docker import DockerClient
from docker.models.containers import Container


def cleanup(client: DockerClient, containers: List[Container], network_name: str):
    """Removes the given network and the docker containers

    Parameters
    ----------
    client : DockerClient
        Client for accessing docker components
    containers : List[Container]
        List of containers to be removed
    network_name : str
        Name of the network to be removed
    """

    for container in containers:
        print(f"Removing container: {container.name}")
        container.remove(force=True)

    print(f"Removing network {network_name}.")
    client.networks.get(network_name).remove()


def create_docker_container(client: DockerClient, image: str, name: str) -> Container | None:
    """Creates a docker container with specified image and name

    Parameters
    ----------
    client : DockerClient
        Client for accessing docker components
    image : str
        Name of the image used to create docker containers
    name : str
        Name of the container and also the hostname

    Returns
    -------
    Container or None
        Docker container or None
    """

    try:
        container = client.containers.run(
            image,
            detach=True,
            name=name,
            hostname=name,
            tty=True
        )
        if container and container.status == 'running' or container.status == 'created':
            print(f"Container {name} was created and runs successfully")
        else:
            print(f"There was an error creating the container {name} or the container is not running.")
        return container
    except docker.errors.APIError as e:
        print(f"Error creating container {name}: {e}")
        return None


def create_docker_containers(client: DockerClient, num_targets: int) -> tuple[Container, List[Container]]:
    """Creates specified number of docker containers

    Parameters
    ----------
    client : DockerClient
        Client for accessing docker components
    num_targets : int
        Number of target containers to create

    Returns
    -------
    Container
        Container attacker
    List[Container]
        List of target containers
    """

    target_list = []
    attacker = create_docker_container(client, 'alpine', 'attacker')
    for i in range(num_targets):
        target_list.append(create_docker_container(client, 'alpine', f'target-{i}'))

    return attacker, target_list


def create_network(client: DockerClient, containers: List[Container], network_name: str):
    """Creates a network with given name and connects all created containers to it

    Parameters
    ----------
    client : DockerClient
        Client for accessing docker components
    containers : List[Container]
        List of containers to connect to the network
    network_name : str
        Name of the network to create
    """

    network = client.networks.create(network_name)
    for container in containers:
        network.connect(container)


def extract_packet_loss(ping_output: str) -> str:
    """Parsing the ping request output to extract the summary

    Parameters
    ----------
    ping_output : str
        Output of a ping command (bash style)

    Returns
    -------
    str
        Summary of numer of packets were transmitted, received and packet loss
    """

    result = ping_output.split("\n")

    return result[-3]


def ping_containers(no_of_pings, attacker, target_list):
    """Send a ping from the attacker to each container in the list

    Parameters
    ----------
    no_of_pings : int
        How many times should attacker container ping each target container
    attacker : Container
        Ping sender
    target_list : List[Container]
        List of ping receivers
    """

    for target in target_list:
        exit_code, ping_output = attacker.exec_run(f"ping -c {no_of_pings} {target.name}")
        ping_output_str = str(ping_output, encoding="utf-8")
        packet_loss_output = extract_packet_loss(ping_output_str)
        print(f"Ping from attacker to {target.name} returned exit code {exit_code} with {packet_loss_output}")
