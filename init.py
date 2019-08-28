import os, re

root = os.getcwd()
conf_path = "{}/conf".format(root)
docker_path = "{}/docker-compose.yml".format(root)
template_service_path = "{}/service.template".format(root)
template_conf_path = "{}/template.conf".format(root)

N = int(os.getenv("N", "1"))
PORT = int(os.getenv("PORT", "19000"))
RPC_PORT = int(os.getenv("RPC_PORT", PORT + 1))
STEP = int(os.getenv("STEP", 10))

def get_env(nums=1, port_0=19000, rpc_port_0=19001, step=10):
    def build_item(index):
        if index == 0:
            return {
                "$ID": "0",
                "$CONF_NAME": "0.conf",
                "$LISTEN": "1",
                "$CONNECT_HOST": "0.0.0.0",
                "$CONNECT_PORT": "{}".format(port_0),
                "$PORT": "{}".format(port_0),
                "$RPC_PORT": "{}".format(rpc_port_0),
            }
        return {
            "$ID": "{}".format(index),
            "$CONF_NAME": "{}.conf".format(index),
            "$LISTEN": "0",
            "$CONNECT_HOST": "0.0.0.0",
            "$CONNECT_PORT": "{}".format(port_0),
            "$PORT": "{}".format(str(port_0 + index * step)),
            "$RPC_PORT": "{}".format(str(rpc_port_0 + index * step)),
        }
    return list(map(build_item, range(nums)))


def build_template(env, template):
    for k, v in env.items():
        template = template.replace(k, v)
    return template

def write_conf(name, conf_path, text):
    conf = open("{}/{}".format(conf_path, name), "w")
    conf.write(text)
    conf.close()

template_conf = open(template_conf_path, "r").read()
template_service = open(template_service_path, "r").read()
docker_compose = open(docker_path, "w")

env_maps = get_env(N, PORT, RPC_PORT, STEP)

docker_services = """\
version: "3"
services:
"""

for env_map in env_maps:
    conf = build_template(env_map, template_conf)
    write_conf(env_map["$CONF_NAME"], conf_path, conf)
    docker_services += build_template(env_map, template_service)
docker_compose.write(docker_services)
docker_compose.close()

print("env template init over")
print("starting docker....")
os.system("sudo docker-compose up")

