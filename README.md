The script configures new machine to run docker-compose with specific docker images

Run `config.py` after new machine created from AMI.

### AMI prerequisites:
1. Authenticated on DockerHub (to pull private images)
2. Docker.io, docker-compose, awscli, PostgreSQL installed (to create database in RDS)
3. `sample.env` file must be copy of the file from AMI-initial repo.
4. `/home/ubungu/backup.sh` must be crontabbed
