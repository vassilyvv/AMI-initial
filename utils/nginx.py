import os


def configure(filename: str, project_name: str, api_domain: str):
    final_result = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            final_result.append(
                line
                .replace('<api_domain>', api_domain)
                .replace('<project_name>', project_name)
            )
    with open(filename, 'w') as f:
        for line in final_result:
            f.write(line)
    os.system('sudo chown ubuntu:ubuntu %s' % filename)
