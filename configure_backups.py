import stat
import os
from pathlib import Path

import click

from validators import validate_project_name, validate_unix_path

BACKUP_SCRIPT_FILENAME = '/home/ubuntu/backup.sh'

POSTGRES_BACKUP_SCRIPT_TEMPLATE = """
#!/bin/sh
cd {parent_directory}
MOMENT="$(date +%H%M%S)"
YEAR="$(date +%Y)"
MONTH="$(date +%m)"
DAY="$(date +%d)"
FILENAME=$MOMENT.sql
PGPASSWORD={postgres_password} pg_dump -h {postgres_endpoint} -p {postgres_port} -U {postgres_username} {database_name} > {parent_directory}/$FILENAME
AWS_ACCESS_KEY_ID={aws_access_key_id} AWS_SECRET_ACCESS_KEY={aws_secret_access_key} AWS_DEFAULT_REGION={aws_region} aws s3 cp {parent_directory}/$FILENAME s3://{aws_s3_bucket}/{project_name}/$YEAR/$MONTH/$DAY/
rm {parent_directory}/$FILENAME
"""


@click.command()
@click.option("--project-name",
              prompt="Project name",
              help="Will be used for naming backups folder in the backups bucket.",
              callback=validate_project_name)
@click.option("--parent-directory",
              prompt="Parent directory for script",
              callback=validate_unix_path)
@click.option("--postgres-username",
              prompt="Postgres username")
@click.option("--postgres-password",
              prompt="Postgres password")
@click.option("--postgres-endpoint",
              prompt="Postgres endpoint")
@click.option("--postgres-port",
              prompt="Postgres port")
@click.option("--database-name",
              prompt="Database name")
@click.option("--aws-access-key-id",
              prompt="AWS Access Key ID")
@click.option("--aws-secret-access-key",
              prompt="AWS secret access key")
@click.option("--aws-region",
              prompt="AWS region")
@click.option("--aws-s3-bucket",
              prompt="S3 bucket for backups")
def configure_backups(
        project_name: str,
        parent_directory: str,
        postgres_username: str,
        postgres_password: str,
        postgres_endpoint: str,
        postgres_port: int,
        database_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_region: str,
        aws_s3_bucket: str
):
    script_path = Path(parent_directory) / 'backup.sh'
    script = POSTGRES_BACKUP_SCRIPT_TEMPLATE.format(
        project_name=project_name,
        parent_directory=parent_directory,
        postgres_username=postgres_username,
        postgres_password=postgres_password,
        postgres_endpoint=postgres_endpoint,
        postgres_port=postgres_port,
        database_name=database_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_region=aws_region,
        aws_s3_bucket=aws_s3_bucket
    )
    script_path.write_text(script)
    script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
    os.system('sudo chown ubuntu:ubuntu %s' % script_path)
    print(f'{script_path} successfully created. Now you can add it to your cron.')


if __name__ == '__main__':
    configure_backups()
