"""
This module defines a CLI interface for managing Docker containers and networks.
"""

from typing import List

import docker
import click

from container_manager import create_network, ping_containers, create_docker_containers, cleanup


@click.group()
def cli() -> None:
    """
    Dummy method for grouping sub-commands.
    """
    pass


@cli.command()
@click.option("--count", default=1, help="Number of targets.")
def cli_create_docker_containers(count: int) -> None:
    """
    Creates Docker containers.

    Parameters
    ----------
    count : int
        Number of containers to create.
    """
    client = docker.from_env()
    create_docker_containers(client, count)


@cli.command()
@click.option("--network_name", default="hack-net", help="Network name")
@click.option("--container",
              "-c",
              "containers",
              default=["attacker", "target-0"],
              help="Name of container",
              multiple=True)
def cli_network_setup(network_name: str, containers: List[str]) -> None:
    """
    Sets up a Docker network and connects containers to it.

    Parameters
    ----------
    network_name : str
        Name of the network.
    containers : List[str]
        Names of containers to connect to the network.
    """
    list_of_containers: List[docker.models.containers.Container] = []
    client = docker.from_env()
    for container in containers:
        list_of_containers.append(client.containers.get(container))
    create_network(client, list_of_containers, network_name)


@cli.command()
@click.option("--no_of_pings", default=4, help="How many pings are sent to each container")
@click.option("--destinations", "-d", default=["target-0"], multiple=True, help="Ping destination")
@click.option("--source", default="attacker", help="Ping source")
def cli_network_testing(no_of_pings: int, source: str, destinations: List[str]) -> None:
    """
    Tests network connectivity by sending pings between containers.

    Parameters
    ----------
    no_of_pings : int
        Number of pings to send.
    source : str
        Name of the container from which pings originate.
    destinations : List[str]
        Names of containers to ping.
    """
    list_of_destinations: List[docker.models.containers.Container] = []
    client = docker.from_env()
    ping_source = client.containers.get(source)
    for destination in destinations:
        list_of_destinations.append(client.containers.get(destination))
    ping_containers(no_of_pings, ping_source, list_of_destinations)


@cli.command()
@click.option("--containers", "-c", default=["attacker","target-0"], multiple=True, help="Containers to remove")
@click.option("--network_name", "-n", default="hack-net", help="Name of the network to remove")
def cli_cleanup(containers: List[str], network_name: str) -> None:
    """
    Removes Docker containers and optionally the associated network.

    Parameters
    ----------
    containers : List[str]
        Names of containers to remove.
    network_name : str
        Name of the network to remove (if no containers left).
    """
    list_of_containers: List[docker.models.containers.Container] = []
    client = docker.from_env()
    for container in containers:
        list_of_containers.append(client.containers.get(container))
    cleanup(client, list_of_containers, network_name)


@cli.command()
def cli_run_all() -> None:
    """
    Runs predefined command set-up
    """
    client = docker.from_env()
    network_name = "hack-net"
    num_targets = 4
    no_of_pings = 4
    attacker, target_list = create_docker_containers(client, num_targets)

    create_network(client, [attacker, *target_list], network_name)
    ping_containers(no_of_pings, attacker, target_list)

    cleanup(client, [attacker, *target_list], network_name)


if __name__ == "__main__":
    cli()
