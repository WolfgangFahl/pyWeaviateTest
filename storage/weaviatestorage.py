'''
Created on 2021-09-25

@author: wf
'''
import weaviate
from python_on_whales import docker
from pathlib import Path
import os
import yaml

class Weaviate(object):
    '''
    weaviate storage wrapper
    '''

    def __init__(self,port=8080,host="localhost"):
        '''
        Constructor
        
        Args:
            port(int): the port for the weaviate docker service
            host(str): the host to use for the weaviate docker service
        '''
        self.port=port
        self.host=host
        self.url=f"http://{self.host}:{self.port}"
        self.client=weaviate.Client(self.url) 
       
        
    @staticmethod
    def start(port=None):
        '''
        start weaviate
        
        Args:
            port(int): the port to use - if None is specified the port mapping is read from the docker-compose file
        
        Returns:
            Weaviate: a weaviate instance
        
        '''
        if port is None:
            port=Weaviate.readPort()
        check=DockerUtil.check()
        if check is not None:
            raise Exception(check)
        containerMap=DockerUtil.getContainerMap()
        if not "weaviate_weaviate_1" in containerMap:
            Weaviate.startDockerContainer(port=port)
        weaviate=Weaviate(port=port)
        return weaviate
    
    @staticmethod
    def startDockerContainer():
        '''
        start the docker container for weaviate 
        from the docker composer file in the default dockerPath 
        
        '''
        dockerPath=Weaviate.getDockerPath()
        # change directory so that docker CLI will find the relevant dockerfile and docker-compose.yml
        os.chdir(dockerPath)
        # run docker compose up
        docker.compose.up(detach=True)    
        
    @staticmethod
    def getDockerPath():
        home = str(Path.home())
        dockerPath=f'{home}/.weaviate' 
        return dockerPath
        
    @staticmethod
    def readPort():    
        dockerPath=Weaviate.getDockerPath()
        composeYaml=f'{dockerPath}/docker-compose.yml'
        with open(composeYaml, 'r') as stream:
            compose = yaml.safe_load(stream)
            ports=compose['services']['weaviate']['ports'][0]
            portStr=ports.split(":")[0]
            return int(portStr)

        
        
class DockerUtil():
    '''
    helper class to work with Docker 
    '''
    @staticmethod
    def getContainerMap():
        '''
        get a map/dict of containers by container name
        convert lists of docker elements to maps for improved
        lookup functionality
        '''
        containerMap={}
        for container in docker.container.list():
            containerMap[container.name]=container
            pass
        return containerMap

    @staticmethod 
    def check()->str:
        errMsg=None
        if not docker.compose.is_installed():
            errMsg="""docker compose up needs to be working
            you might want to install https://github.com/docker/compose-cli
            Compose v2 can be installed manually as a CLI plugin, 
            by downloading latest v2.x release from https://github.com/docker/compose-cli/releases for your architecture and move into ~/.docker/cli-plugins/docker-compose
"""
        return errMsg
  
        