import pymongo
import pytest
import json, os
from unittest.mock import patch
from dotenv import dotenv_values

from src.util.dao import DAO

# We should remove this, just testing the connections with existing collection
@pytest.mark.assignment3
def test_connection():
    testDao = DAO('todo')
    print(testDao.collection.name)
    assert testDao.collection.name == 'todo'

class TestCreation:
    @pytest.mark.assignment3
    #@pytest.mark.parametrize('email, obj', [('jandoe@test.se', {'Name': 'Jane'}), ('jan.doe@test.se', {'Name': 'Jane'})])
    # System under test will be a DAO object from the file dao.py
    @pytest.fixture
    def sut(self):
        # Julian said that it is good to create entities on db when testing, to not rely on existing ones.
        # We can mock a new entity and then delete it from the DB
        # I am basing on the slide 16
        # Update: I tried to create a file, but for some reason windows does not allow me to do so through pytest
        fabricated_collection = 'mocked_collection'
        fabricated_validator = {
                                "$jsonSchema": {
                                    "bsonType": "object",
                                        "required": ["description", "PN"],
                                        "properties": {
                                            "description": {
                                                "bsonType": "string",
                                                "description": "just mocking",
                                                "uniqueItems": True
                                            }, 
                                            "mock": {
                                                "bsonType": "bool"
                                            },
                                            "PN": {
                                                "bsonType": "int",
                                                "description": "Person Number",
                                                "uniqueItems": True
                                            }
                                        }
                                    }
                                }
        
        # Patch the getValidator to return the fabricated one
        with patch('src.util.dao.getValidator', autospec=True) as mocked_validator:
            mocked_validator.return_value = fabricated_validator
            
            # Create collection (since it does not exists) and return
            yield DAO(fabricated_collection)

            # After the return the collection can be deleted
            # https://www.w3schools.com/python/python_mongodb_drop_collection.asp
            # Using the dao connection as rerference
            LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
            MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)
            client = pymongo.MongoClient(MONGO_URL)
            database = client.edutask
            database[fabricated_collection].drop()


    @pytest.mark.assignment3
    def test_creation_success_1(self, sut):
        test_data = {
            "description": "Some mocked data",
            "mock": True,
            "PN": 2000000000
        }
        create_return = sut.create(test_data)
        assert create_return['description'] == test_data['description']
        assert create_return['mock'] == test_data['mock']

    @pytest.mark.assignment3
    def test_creation_fail_1(self, sut):
        test_data = {
            "mock": True
        }
        with pytest.raises(pymongo.errors.WriteError) as excinfo:
                sut.create(test_data)


    # This one fails problably because unique keys should have in app validation, not just on json
    # https://www.mongodb.com/community/forums/t/how-to-make-schema-field-unique/107585 
    @pytest.mark.assignment3
    def test_creation_fail_2(self, sut):
        """
        Creating same object twice
        """
        test_data = {
            "description": "Some more mocked data",
            "mock": True,
            "PN": 2000000000
        }

        # First creation should work
        sut.create(test_data)

        # Second should raise error since description is unique
        with pytest.raises(pymongo.errors.WriteError) as excinfo:
                sut.create(test_data)



        # @pytest.fixture
        # def sut(self):
        #     # Julian said that it is good to create entities on db when testing, to not rely on existing ones.
        #     # We can mock a new entity and them delete it from the DB
        #     # I am basing on the slide 16
        #     fabricated_validator_file_name = 'fabricated_collection'
        #     self.json_string = {"$jsonSchema": {
        #                                 "bsonType": "object",
        #                                 "required": ["just"],
        #                                 "properties": {
        #                                     "bsonType": "string",
        #                                     "just": "mocking",
        #                                     "uniqueItems": True
        #                                 }
        #                             }
        #                         }
        #     # Create the validator file
        #     with open(fabricated_validator_file_name, 'w') as outfile:
        #         json.dump(self.json_string, outfile)
            
        #     yield DAO(fabricated_validator_file_name)