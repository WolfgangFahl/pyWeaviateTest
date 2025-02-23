"""
Created on 2021-09-25
Refactored on 2025-02-23

Weaviate Query Execution Context

@author: wf
"""
import argparse
import weaviate
from python_on_whales import docker

from storage.dockerutil import DockerEnv, DockerMap


class WeaviateQueryExecutionContext:
    """
    Weaviate Query Execution context for version 1.29.0.

    See:
    https://weaviate.io/developers/weaviate/installation/docker-container
    https://weaviate-python-client.readthedocs.io/en/stable/
    """

    def __init__(
        self, port=8080, grpc_port=50051, host="localhost", debug: bool = False
    ):
        """
        Constructor for Weaviate Query Execution Context.

        Args:
            port (int): The port for the Weaviate REST API.
            grpc_port (int): The port for the gRPC API.
            host (str): The hostname for the Weaviate service.
            debug (bool): If True, enables debug logging.
        """
        self.port = port
        self.grpc_port = grpc_port
        self.host = host
        self.debug = debug
        self.client = None

    def getClient(self, local: bool = True, with_compose: bool = False):
        """
        get a Weaviate Client.

        Args:
            local (bool): If True, starts Weaviate locally.
            with_compose (bool): If True, uses docker-compose (not implemented yet).
        """
        if local:
            self.ensure_weaviate()
            if with_compose:
                raise NotImplementedError("Compose support is not implemented yet.")
            client = weaviate.connect_to_local()
        else:
            raise NotImplementedError("Cloud support is not implemented yet.")
        return client

    @classmethod
    def get(cls, debug: bool = False) -> "WeaviateQueryExecutionContext":
        """
        Start a Weaviate instance.

        Returns:
            WeaviateQueryExcutionContext: A Weaviate QEC instance.
        """
        DockerEnv.setup(debug=debug)
        weaviate = cls()
        return weaviate

    def ensure_weaviate(self):
        """
        Ensure the Weaviate container is running with the configured ports.
        """
        container_map = DockerMap.getContainerMap()
        weaviate_found = False
        image = "cr.weaviate.io/semitechnologies/weaviate:1.29.0"

        for container in container_map.values():
            if image in container.config.image:
                weaviate_found = True
                break

        if not weaviate_found:
            docker.container.run(
                image, detach=True, publish=[(self.port, 8080), (self.grpc_port, 50051)]
            )

    def is_ready(self) -> bool:
        """
        Check if Weaviate is ready to accept requests.

        Returns:
            bool: True if Weaviate is ready.
        """
        with self.getClient() as client:
            ready = client.is_ready()
            return ready

    def create_schema(self, schema: dict):
        """
        Create a schema in Weaviate.

        Args:
            schema (dict): The schema definition.
        """
        if self.client.schema.contains():
            self.client.schema.delete_all()
        self.client.schema.create(schema)

def main():
    """
    Main entry point for weaviate startup
    """
    parser = argparse.ArgumentParser(description="Start weaviate")
    parser.add_argument('--debug', action='store_true', help='enable debug mode')
    parser.add_argument('-s', '--start', action='store_true', help='start weaviate')
    parser.add_argument('-p', '--port', type=int, default=8090, help='port to use (default: 8090)')

    args = parser.parse_args()
    if args.start:
        wqec = WeaviateQueryExecutionContext(port=args.port,debug=args.debug)
        is_ready = wqec.is_ready()
        print(f"Weaviate {'✅ ready' if is_ready else '❌ not ready'}")
        return 0 if is_ready else 1

if __name__ == "__main__":
    main()

