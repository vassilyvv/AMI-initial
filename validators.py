import click
import re


def validate_project_name(context, parameter, value):
    if not re.match('^[a-zA-Z0-9-]+$', value):
        raise click.BadParameter('Project name must contain only alphanumeric characters')
    return value


def validate_domain(context, parameter, value):
    if not re.match('^[a-z0-9]+(\.[a-z0-9]+)+$', value):
        raise click.BadParameter('Bad domain. Must contain only lowercase alphanumeric characters')
    return value


def validate_docker_image_name(context, parameter, value):
    if not re.match('^[a-zA-Z0-9-]+(-[a-zA-Z0-9-]+)*\/[a-zA-Z0-9-]+(-[a-zA-Z0-9-]+)*:[a-zA-Z0-9-]+(-[a-zA-Z0-9-]+)*$', value):
        raise click.BadParameter('Bad docker image name. Does it contain a tag?')
    return value


def validate_unix_path(context, parameter, value):
    if not re.match('^/([a-zA-Z0-9_-]+/)*$', value):
        raise click.BadParameter('Bad unix path')
    return value
