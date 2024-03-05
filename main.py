import docker
from time import sleep

client = docker.from_env()

def remove_containers():
    containers = client.containers.list(all=True)
    for container in containers:
        print(f"Removing container: {container.name}")
        container.remove(force=True)

def create_docker_container(image, name):
    try:
        container = client.containers.run(
            image,
            detach=True,
            name=name,
            hostname=name,
            remove=True,
            tty=True
        )
        wait_for_container(container.id)
        container = client.containers.get(container.id)
        if container and container.status == 'running':
            print(f"Container {name} was created successfully")
        else:
            print(f"There was an error creating container {name}")
        return container
    except docker.errors.APIError as e:
        print(f"Error creating container {name}: {e}")
        return None

def wait_for_container(container_id):
    timeout = 10
    stop_time= 1
    elapsed_time = 0
    while client.containers.get(container_id).status != "running" and elapsed_time < timeout:
        sleep(stop_time)
        elapsed_time += stop_time
        continue



def create_docker_containers(num_targets):
    create_docker_container('alpine', 'attacker')
    for i in range(num_targets):
        create_docker_container('alpine', f'target-{i}')


if __name__ == "__main__":
    remove_containers()
    num_targets = int(input("Input the number of target containers to be created: "))
    create_docker_containers(num_targets)
    print(client.containers.list())
