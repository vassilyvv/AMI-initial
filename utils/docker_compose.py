import os
def configure(filename: str, project_name: str, docker_image_name: str):
    final_result = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            final_result.append(
                line
                .replace('<project_name>', project_name)
                .replace('<backend_docker_image>', docker_image_name)
            )
    with open(filename, 'w') as f:
        for line in final_result:
            f.write(line)
    os.system('sudo chown ubuntu:ubuntu %s' % filename)
