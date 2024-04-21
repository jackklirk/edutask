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
            # Connect with DB
            LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
            MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)
            client = pymongo.MongoClient(MONGO_URL)
            database = client.edutask
            # Drop collection if it exist to make it sure we are starting with a clean one
            database[fabricated_collection].drop()
            #database[fabricated_collection].create_index([("PN", 1)], unique=True)
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


    # This one fails problably because unique keys should have in app validation, not just on json
    # https://www.mongodb.com/community/forums/t/how-to-make-schema-field-unique/107585 
    @pytest.mark.assignment3
    def test_id4_creation_fail_2(self, sut):
        """
        Creating two objects with same unique key
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

    @pytest.mark.assignment3
    def test_id5_creation_fail_3(self, sut):
        """
        Creating with wrong datatypes values on keys
        """
        test_data = {
            "description": 0.5,
            "mock": 1,
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

        # First creation should work
        # Second should raise error since description is unique
        with pytest.raises(pymongo.errors.WriteError) as excinfo:
            sut.create(test_data)


    @pytest.mark.assignment3
    def test_id7_creation_fail_4(self, sut):
        """
        No argument provided
        """

        # Second should raise error since description is unique
        with pytest.raises(TypeError) as excinfo:
                sut.create()





# import pymongo.mongo_client
# import pytest
# import pymongo 
# import os
# import json
# from dotenv import dotenv_values
# from unittest.mock import patch, MagicMock
# from src.util.dao import DAO
# from src.util.validators import getValidator



# @pytest.fixture
# def database():
#     Local_Mongo_URL = dotenv_values('.env').get('MONGO_URL')
#     Mongo_URL = os.environ.get('MONGO_URL', Local_Mongo_URL)

#     client = pymongo.MongoClient(Mongo_URL)
#     return client


# @pytest.mark.assignment3
# def test_mongodb_connection(database): 
    
#     assert database.admin.command("ping")["ok"] != 0.0

# @pytest.fixture
# def database_rollback(database):
#     session = database.start_session()
#     session.start_transaction()
#     try: 
#         yield session

#     finally:
#         session.abort_transaction()



# @pytest.mark.assignment3
# @pytest.mark.parametrize('collection_name, data',[('test', {'description':'Testing functionality'})])
# def test_create_success(database, database_rollback, collection_name, data): 
#     i = 1
#     d = 2
#     db = database.edutask
#     with open('backend/test/Lab1/Assignment3/static/test.json') as f:
#         data = json.load(f)

#     print(db.list_collection_names())
#     with patch('src.util.dao.getValidator') as mockedValidator:
#         mockedValidator.return_value = data
#         dao = DAO(collection_name)
        
#         assert dao.create()


