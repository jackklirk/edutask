import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController


@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('jandoe@test.se', {'Name': 'Jane'}), ('jan.doe@test.se', {'Name': 'Jane'})])
def test_id1_2_get_user_by_email_success(email, obj):
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [obj]
    uc = UserController(dao=mockedDAO)
    
    assert uc.get_user_by_email(email) == obj


@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('@test.se', ValueError), ('test.se', ValueError), ('se', ValueError), ('jan@test', ValueError), ('jan@.se', ValueError)])
def test_id3_7_get_user_by_email_failure(email, obj):
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [obj]
    uc = UserController(dao=mockedDAO)
    with pytest.raises(ValueError) as excinfo:  
        uc.get_user_by_email(email)

    assert str(excinfo.value) == 'Error: invalid email address'


@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('Hello@World.se', None)])
def test_id8_get_user_by_email_None(email, obj):
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = []
    uc = UserController(dao=mockedDAO)

    assert uc.get_user_by_email(email) == None

@pytest.mark.unit
def test_id9_get_user_by_email_Double(capsys):
    user1 = {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jandoe@test.se'}
    user2 = {'firstName': 'John', 'lastName': 'Doe', 'email': 'jandoe@test.se'}
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [user1, user2]
    uc = UserController(dao=mockedDAO)
    uc.get_user_by_email('jandoe@test.se')
    captured = capsys.readouterr()
    assert captured.out == 'Error: more than one user found with mail jandoe@test.se\n'

@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('jandoe@test.se', Exception)])
def test_id10_get_user_by_email_Exception(email, obj):
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = obj
    uc = UserController(dao=mockedDAO)
    with pytest.raises(Exception):
        uc.get_user_by_email(email)
