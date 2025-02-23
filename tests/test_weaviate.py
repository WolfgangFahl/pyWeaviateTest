"""
Created 2021

@author: wf
"""

import logging

from lodstorage.sample2 import Sample
from weaviate.classes.config import DataType, Property

from storage.dockerutil import DockerEnv
from storage.weaviate_qec import WeaviateQueryExecutionContext
from tests.basetest import Basetest


class TestWeaviate(Basetest):
    """
    Test Weaviate functionality
    """

    def setUp(self, debug=True, profile=True):
        """
        set up this test case
        """
        Basetest.setUp(self, debug, profile)
        DockerEnv.setup(debug=debug)
        self.wqec = WeaviateQueryExecutionContext.get(debug=debug)
        self.royal_samples = Sample.get("royals")["QE2 heirs up to number in line 5"]

    def testRunning(self):
        """
        make sure weaviate is running
        """
        self.assertTrue(self.wqec.is_ready())

    def test_collection(self):
        """
        test create,read,update and delete operations
        using a collection
        """
        with self.wqec.getClient() as client:
            try:
                client.collections.delete("Royal")
            except Exception as ex:
                if self.debug:
                    msg = str(ex)
                    logging.debug(msg)
            # Create Royal collection based on Royal dataclass fields
            properties = [
                Property(name="name", data_type=DataType.TEXT),
                Property(name="wikidata_id", data_type=DataType.TEXT),
                Property(name="number_in_line", data_type=DataType.INT),
                Property(name="born_iso_date", data_type=DataType.TEXT),
                Property(name="died_iso_date", data_type=DataType.TEXT),
                Property(name="last_modified_iso", data_type=DataType.TEXT),
                Property(name="age", data_type=DataType.INT),
                Property(name="of_age", data_type=DataType.BOOL),
                Property(name="wikidata_url", data_type=DataType.TEXT),
            ]
            collection = client.collections.create("Royal", properties=properties)
