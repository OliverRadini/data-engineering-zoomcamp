create pod:
podman pod create --name postgre-sql -p 9876:80 -p 5432:5432

create volume:
podman volume create pg-data

pgadmin:
podman run --pod postgre-sql -e 'PGADMIN_DEFAULT_EMAIL=admin@admin.com' -e 'PGADMIN_DEFAULT_PASSWORD=root' --name pgadmin -d docker.io/dpage/pgadmin4:latest


postgres-with-volume:
podman run --name pgdatabase -v pg-data:/var/lib/postgresql/data:Z --pod=postgre-sql -d -e POSTGRES_USER=admin@admin.com -e POSTGRES_PASSWORD=root docker.io/library/postgres:14


	(find files in explorer here: \\wsl.localhost\podman-machine-default\home\user\.local\share\containers\storage\volumes)
	(find files here from wsl machine: /home/user/.local/share/containers/storage/volumes/pg-data)