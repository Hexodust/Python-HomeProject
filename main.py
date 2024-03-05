import docker
client = docker.from_env()
def create_docker_attacker():
    attacker_container = client.containers.run(
        'alpine',
        detach=True,
        name='attacker',
        hostname='attacker',
    )
    if attacker_container.status == 'running':
        print("Attacker container has been created successfully.")
    else:
        print("There was an error with Attacker Container")
        print(attacker_container.status)


def create_docker_containers(num_targets):
    create_docker_attacker()
    target_containers_list = []
    # Creating the target containers
    for i in range(num_targets):
        target_container = client.containers.run(
            'alpine',
            detach=True,
            name=f'target-{i}',
            hostname=f'target-{i}'
        )
        target_containers_list.append(target_container)

    for i, container in enumerate(target_containers_list):
        if container.status == 'running':
            print(f"Container target-{i} was created successfully")
        else:
            print(f"There was an error creating container target-{i}")



if __name__ == "__main__":
    num_targets = int(input("Input the number of target containers to be created: "))
    create_docker_containers(num_targets)
