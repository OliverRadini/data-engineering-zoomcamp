from prefect.infrastructure.docker import DockerContainer

docker_block = DockerContainer(
    image="donutttt/prefect:v0001",
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save("zoom", overwrite=True)