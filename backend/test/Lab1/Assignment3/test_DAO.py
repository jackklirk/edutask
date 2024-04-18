import pymongo.mongo_client
import pytest
import pymongo 
import os
from dotenv import dotenv_values
from unittest.mock import patch, MagicMock
from src.util.dao import DAO
from src.util.validators import getValidator



@pytest.fixture
def database():
    Local_Mongo_URL = dotenv_values('.env').get('MONGO_URL')
    Mongo_URL = os.environ.get('MONGO_URL', Local_Mongo_URL)

    client = pymongo.MongoClient(Mongo_URL)
    return client


@pytest.mark.assignment3
def test_mongodb_connection(database): 
    
    assert database.admin.command("ping")["ok"] != 0.0

@pytest.fixture
def database_rollback(database):
    session = database.start_session()
    session.start_transaction()
    try: 
        yield session

    finally:
        session.abort_transaction()



@pytest.mark.assignment3
@pytest.mark.parametrize('collection_name, data',[('todo', {'description':'Testing functionality'})])
def test_create_success(database, database_rollback, collection_name, data): 
    db = database.edutask
    
    dao = DAO(collection_name)

    
    assert dao.create(data) == data


