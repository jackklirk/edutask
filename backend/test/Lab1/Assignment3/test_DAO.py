import pymongo
import pytest
import json, os
from unittest.mock import patch
from dotenv import dotenv_values

from src.util.dao import DAO


class TestConnection:
    @pytest.mark.assignment3
    def test_mongodb_connection(self): 
        Local_Mongo_URL = dotenv_values('.env').get('MONGO_URL')
        Mongo_URL = os.environ.get('MONGO_URL', Local_Mongo_URL)
        client = pymongo.MongoClient(Mongo_URL)
        assert client.admin.command("ping")["ok"] != 0.0

class TestCreation:
    @pytest.mark.assignment3
    # System under test will be a DAO object from the file dao.py
    @pytest.fixture
    def sut(self):
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
            # Connect with DB
            LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
            MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)
            client = pymongo.MongoClient(MONGO_URL)
            database = client.edutask
            # Drop collection if it exist to make it sure we are starting with a clean one
            database[fabricated_collection].drop()
            
            # Create collection (since it does not exists) and return
            yield DAO(fabricated_collection)
            
            # After the return/yield the collection can be deleted
            database[fabricated_collection].drop()


    @pytest.mark.assignment3
    def test_id1_creation_success_1(self, sut):
        """
        All keys filled according to the validator
        """
        test_data = {
            "description": "Some mocked data",
            "mock": True,
            "PN": 2000000000
        }
        create_return = sut.create(test_data)
        assert create_return['description'] == test_data['description']
        assert create_return['mock'] == test_data['mock']

    @pytest.mark.assignment3
    def test_id2_creation_success_2(self, sut):
        """
        Just the required keys
        """
        test_data = {
            "description": "Some more mocked data",
            "PN": 2000000001
        }
        create_return = sut.create(test_data)
        assert create_return['description'] == test_data['description']
        assert create_return['PN'] == test_data['PN']

    @pytest.mark.assignment3
    def test_id3_creation_fail_1(self, sut):
        """
        Missing required key "description"
        """
        test_data = {
            "mock": True,
            "PN": 123123132
        }
        with pytest.raises(pymongo.errors.WriteError) as excinfo:
            sut.create(test_data)

    @pytest.mark.assignment3
    def test_id4_creation_fail_2(self, sut):
        """
        Creating two objects with same unique key
        """
        test_data = {
            "description": "Some more mocked data",
            "mock": True,
            "PN": 2000000002
        }

        # First creation should work
        sut.create(test_data)

        # Second should raise error since description is unique
        with pytest.raises(pymongo.errors.WriteError) as excinfo:
                sut.create(test_data)

    @pytest.mark.assignment3
    def test_id5_creation_fail_3(self, sut):
        """
        Create with wrong datatypes values on keys
        """
        test_data = {
            "description": 0.5,
            "mock": 9,
            "PN": True
        }

        with pytest.raises(pymongo.errors.WriteError) as excinfo:
                sut.create(test_data)

    @pytest.mark.assignment3
    def test_id6_creation_fail_5(self, sut):
        """
        Empty  argument provided
        """
        test_data = {
        }

        with pytest.raises(pymongo.errors.WriteError) as excinfo:
            sut.create(test_data)

    @pytest.mark.assignment3
    def test_id7_creation_fail_4(self, sut):
        """
        No argument provided
        """

        with pytest.raises(TypeError) as excinfo:
                sut.create()
