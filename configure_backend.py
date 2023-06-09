import shutil

import click

from utils.docker_compose import configure as configure_docker_compose
from utils.nginx import configure as configure_nginx
from validators import validate_project_name, validate_domain, validate_docker_image_name

DOCKER_COMPOSE_FILENAME = '/home/ubuntu/docker-compose.yaml'
NGINX_CONFIG_FILENAME = '/home/ubuntu/nginx.conf'


def generate_config_files(use_celery: bool):
    shutil.copyfile(
        f'/home/ubuntu/templates/docker-compose/docker-compose-{"" if use_celery else "no-"}celery.yaml',
        DOCKER_COMPOSE_FILENAME
    )
    shutil.copyfile(
        f'/home/ubuntu/templates/nginx.conf',
        NGINX_CONFIG_FILENAME
    )


@click.command()
@click.option("--project-name",
              prompt="Project name",
              help="Will be used for env variables file and nginx log files.",
              callback=validate_project_name)
@click.option("--docker-image-name",
              prompt="Docker image with tag",
              callback=validate_docker_image_name)
@click.option("--api-domain",
              prompt="API domain",
              help="Example: myapi.com. Will be used in nginx configuration file.",
              callback=validate_domain)
@click.option("--celery/--no-celery", prompt="Use celery?")
def configure_backend(project_name: str, docker_image_name: str, api_domain: str, celery: bool):
    generate_config_files(celery)
    configure_nginx(NGINX_CONFIG_FILENAME, project_name, api_domain)
    configure_docker_compose(DOCKER_COMPOSE_FILENAME, project_name, docker_image_name)


if __name__ == '__main__':
    print("ENSURE YOU'RE RUNNING THIS SCRIPT FROM PROJECT DIRECTORY ON HOST MACHINE")
    configure_backend()
