'''
Created 2021

@author: wf
'''

import unittest
import weaviate
import time
#import getpass

person_schema = {
    "classes": [
    {
    "class": "Person",
    "description": "A person such as humans or personality known through culture",
    "properties": [
        {
        "name": "name",
        "description": "The name of this person",
        "dataType": ["text"]
        }
    ]
    },
    {
    "class": "Group",
    "description": "A set of persons who are associated with each other over some common properties",
    "properties": [
        {
        "name": "name",
        "description": "The name under which this group is known",
        "dataType": ["text"]
        },
        {
        "name": "members",
        "description": "The persons that are part of this group",
        "dataType": ["Person"]
        }
    ]
    }
]
}



class TestWeaviate(unittest.TestCase):
    # NEW link to the page
    # https://www.semi.technology/developers/weaviate/current/client-libraries/python.html

    def setUp(self):
        '''
        set up this test case
        '''
        self.port=8080
        self.host="localhost"
        pass
    
    
    def getClient(self):
        '''
        get the client
        '''
        url=f"http://{self.host}:{self.port}"
        self.client=weaviate.Client(url) 
        return self.client

    def tearDown(self):
        pass
        
    def testRunning(self):
        '''
        make sure weaviate is running
        '''
        w=self.getClient()
        self.assertTrue(w.is_live())
        self.assertTrue(w.is_ready())
            

    def testWeaviateSchema(self):
        # NEW link to the page
        # https://www.semi.technology/developers/weaviate/current/client-libraries/python.html
        w = self.getClient()
        #contains_schema = w.schema.contains()

        # it is a good idea to check if Weaviate has a schema already when testing, otherwise it will result in an error
        # this way you know for sure that your current schema is known to weaviate.

        if w.schema.contains():
            # delete the existing schema, (removes all the data objects too)
            w.schema.delete_all()
        # instead of w.create_schema(person_schema)
        w.schema.create(person_schema)
        entries=[
            [ {"name": "John von Neumann"}, "Person", "b36268d4-a6b5-5274-985f-45f13ce0c642"],
            [ {"name": "Alan Turing"}, "Person", "1c9cd584-88fe-5010-83d0-017cb3fcb446"],
            [ {"name": "Legends"}, "Group", "2db436b5-0557-5016-9c5f-531412adf9c6" ]
        ]
        for entry in entries:
            dict,type,uid=entry
            try:
                # instead of w.create(dict,type,uid), see https://www.semi.technology/developers/weaviate/current/restful-api-references/objects.html#create-a-data-object
                w.data_object.create(dict,type,uid)
            # ObjectAlreadyExistsException is the correct exception starting weaviate-client 2.0.0
            except weaviate.exceptions.ObjectAlreadyExistsException as taee: 
                print ("%s already created" % dict['name'])
            
        pass
    
    def testPersons(self):
        return
        w = self.getClient()

        schema = {
        #"actions": {"classes": [],"type": "action"}, `actions` and `things` were removed in weaviate v1.0 and removed in weaviate-client v2.0
        # Now there is only `objects`
        "classes": [
            {
            "class": "Person",
            "description": "A person such as humans or personality known through culture",
            "properties": [
                {
                    #"cardinality": "atMostOne", were removed in weaviate v1.0 and weaviate-client v2.0
                    "dataType": ["text"],
                    "description": "The name of this person",
                    "name": "name"
                }
            ]
            }
            ]
        }
        # instead of w.create_schema(schema)
        w.schema.create(schema) 
        
        # instead of  w.create_thing({"name": "Andrew S. Tanenbaum"}, "Person")
        w.data_object.create({"name": "Andrew S. Tanenbaum"}, "Person")
        w.data_object.create({"name": "Alan Turing"}, "Person")
        w.data_object.create({"name": "John von Neumann"}, "Person")
        w.data_object.create({"name": "Tim Berners-Lee"}, "Person")
        
    def testEventSchema(self):    
        '''
        https://stackoverflow.com/a/63077495/1497139
        '''
        return
        schema = {
            # "things": { , were removed in weaviate v1.0 and weaviate-client v2.0
            # "type": "thing", was removed in weaviate v1.0 and weaviate-client v2.0
            "classes": [
                {
                "class": "Event",
                "description": "event",
                "properties": [
                    {
                    "name": "acronym",
                    "description": "acronym",
                    "dataType": [
                        "text"
                    ]
                    },
                    {
                    "name": "inCity",
                    "description": "city reference",
                    "dataType": [
                        "City"
                    ],
                    # "cardinality": "many", were removed in weaviate v1.0 and weaviate-client v2.0
                    }
                ]
                },
                {
                "class": "City",
                "description": "city",
                "properties": [
                    {
                    "name": "name",
                    "description": "name",
                    "dataType": [
                        "text"
                    ]
                    },
                    {
                    "name": "hasEvent",
                    "description": "event references",
                    "dataType": [
                        "Event"
                    ],
                    # "cardinality": "many", were removed in weaviate v1.0 and weaviate-client v2.0
                    }
                ]
                }
            ]
        }


        client = self.getClient()

        # this test is going to fail if you are using the same Weaviate instance
        # We already created a schema in the test above so the new schme is not going to be created
        # and will result in an error.
        # we can delete the schema and create a new one.
        
        # instead of client.contains_schema()
        if client.schema.contains():
            # delete the existing schema, (removes all the data objects too)
            client.schema.delete_all()
        # instead of client.create_schema(schema)
        client.schema.create(schema)

        event = {"acronym": "example"}
        # instead of client.create(...)
        client.data_object.create(event, "Event", "2a8d56b7-2dd5-4e68-aa40-53c9196aecde")
        city = {"name": "Amsterdam"}
        client.data_object.create(city, "City", "c60505f9-8271-4eec-b998-81d016648d85")

        time.sleep(2.0)
        # instead of client.add_reference(...), see https://www.semi.technology/developers/weaviate/current/restful-api-references/objects.html#cross-references
        client.data_object.reference.add("c60505f9-8271-4eec-b998-81d016648d85", "hasEvent", "2a8d56b7-2dd5-4e68-aa40-53c9196aecde")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main() 