"""
Refactored on 2025-02-23

@author: wf
"""

import os

from python_on_whales import docker


class Logger(object):
    """
    simple logger
    """

    @classmethod
    def check_and_log(cls, msg: str, ok: bool) -> bool:
        """
        log the given message with the given ok flag

        Args:
            msg(str): the message to log/print
            ok(bool): if True show ✅ marker else ❌

        Return:
            bool: the ok parameter for fluid syntax
        """
        marker = "✅" if ok else "❌"
        print(f"{msg}:{marker}")
        return ok

    @classmethod
    def check_and_log_equal(self, nameA, valueA, nameB, valueB):
        msg = f"{nameA} {valueA}= {nameB} {valueB}?"
        return self.check_and_log(msg, valueA == valueB)


class DockerEnv:
    @staticmethod
    def setup(debug: bool = False) -> str:
        """
        setup the docker environment

        Args:
            debug (bool): if True show debug information

        Returns:
            str: an error message or None
        """
        os_path = os.environ["PATH"]
        paths = ["/usr/local/bin"]
        for path in paths:
            if os.path.islink(f"{path}/docker"):
                if not path in os_path:
                    os.environ["PATH"] = f"{os_path}{os.pathsep}{path}"
                    if debug:
                        print(
                            f"""modified PATH from {os_path} to \n{os.environ["PATH"]}"""
                        )
        errMsg = None
        if not docker.compose.is_installed():
            errMsg = """docker compose up needs to be working"""
        return errMsg


class DockerMap:
    """
    helper class to convert lists of docker elements to maps for improved
    lookup functionality
    """

    @staticmethod
    def getContainerMap():
        """
        get a map/dict of containers by container name
        """
        containerMap = {}
        for container in docker.container.list():
            containerMap[container.name] = container
            pass
        return containerMap


class DockerContainer:
    """
    helper class for docker container info
    """

    def __init__(self, name, kind, container):
        """
        constructor
        """
        self.name = name
        self.kind = kind
        self.container = container

    def check(self):
        """
        check the given docker container

        print check message and Return if container is running

        Args:
            dc: the docker container

        Returns:
            bool: True if the container is not None
        """
        ok = self.container.state.running
        msg = f"mediawiki {self.kind} container {self.name}"
        return Logger.check_and_log(msg, ok)

    def getHostPort(self, local_port: int = 80) -> int:
        """
        get the host port for the given local port

        Args:
            local_port (int): the local port to get the mapping for

        Returns:
            int: the  host port or None
        """
        host_port = None
        pb_dict = self.container.host_config.port_bindings
        p_local = f"{local_port}/tcp"
        if p_local in pb_dict:
            pb = pb_dict[p_local][0]
            host_port = pb.host_port
        return host_port
