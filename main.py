import docker


def cleanup(client, containers, network_name):
    for container in containers:
        print(f"Removing container: {container.name}")
        container.remove(force=True)

    print(f"Removing network {network_name}.")
    client.networks.get(network_name).remove()


def create_docker_container(client, image, name):
    try:
        container = client.containers.run(
            image,
            detach=True,
            name=name,
            hostname=name,
            tty=True
        )
        if container and container.status == 'running':
            print(f"Container {name} was created and runs successfully")
        else:
            print(f"There was an error creating the container {name} or the container is not running.")
        return container
    except docker.errors.APIError as e:
        print(f"Error creating container {name}: {e}")
        return None


def create_docker_containers(client, num_targets):
    target_list = []
    attacker = create_docker_container(client, 'alpine', 'attacker')
    for i in range(num_targets):
        target_list.append(create_docker_container(client, 'alpine', f'target-{i}'))

    return attacker, target_list


def create_network(client, network_name):
    network = client.networks.create(network_name)
    for container in client.containers.list():
        network.connect(container)


def extract_packet_loss(command_output):
    result = command_output.split("\n")
    return result[-3]

def ping_containers(attacker, target_list):
    for target in target_list:
        exit_code, command_output = attacker.exec_run(f"ping -c 4 {target.name}")
        command_output_str = str(command_output, encoding="utf-8")
        packet_loss_output = extract_packet_loss(command_output_str)
        print(f"Ping from attacker to {target.name} returned exit code {exit_code} with {packet_loss_output}")



def main():

    client = docker.from_env()
    network_name = "hack-net"
    num_targets = int(input("Input the number of target containers to be created: "))
    attacker, target_list = create_docker_containers(client, num_targets)

    create_network(client, network_name)
    ping_containers(attacker, target_list)

    cleanup(client, [attacker, *target_list], network_name)


if __name__ == "__main__":
    main()