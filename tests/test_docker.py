"""
Created on 2025-02-23

@author: wf
"""
from tests.basetest import Basetest
from storage.dockerutil import DockerEnv, DockerMap

class TestDockerUtil(Basetest):
    """
    test for the DockerUtil helper class
    """

    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)

    """
    check the docker container map
    """

    def testDocker(self):
        DockerEnv.setup(debug=self.debug)
        cmap = DockerMap.getContainerMap()

        for i, container_name in enumerate(cmap.keys(), start=1):
            container = cmap[container_name]
            bindings = container.host_config.port_bindings
            image = container.config.image
            ports = " ".join(
                [
                    f"{port.split('/')[0]}➡{binding[0].host_port}"
                    for port, binding in bindings.items()
                ]
            )
            if self.debug:
                print(f"{i}:{container_name}:{image} {ports}")
