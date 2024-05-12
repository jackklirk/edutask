import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController


@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('jandoe@test.se', {'Name': 'Jane'})])
def test_id1_get_user_by_email_success(email, obj):

    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [obj]
    uc = UserController(dao=mockedDAO)
    
    assert uc.get_user_by_email(email) == obj

@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('jan.doe@test.se', {'Name': 'Jane'})])
def test_id2_get_user_by_email_success(email, obj):
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [obj]
    uc = UserController(dao=mockedDAO)
    
    assert uc.get_user_by_email(email) == obj


@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('@test.se', ValueError)])
def test_id3_get_user_by_email_failure(email, obj):
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [obj]
    uc = UserController(dao=mockedDAO)
    with pytest.raises(ValueError) as excinfo:  
        uc.get_user_by_email(email)

    assert str(excinfo.value) == 'Error: invalid email address'

@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('test.se', ValueError), ('se', ValueError)])
def test_id4_get_user_by_email_failure(email, obj):
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [obj]
    uc = UserController(dao=mockedDAO)
    with pytest.raises(ValueError) as excinfo:  
        uc.get_user_by_email(email)

    assert str(excinfo.value) == 'Error: invalid email address'

@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('jan@test', ValueError)])
def test_id5_get_user_by_email_failure(email, obj):
    mockedDAO = MagicMock()
    mockedDAO.find.return_value = [obj]
    uc = UserController(dao=mockedDAO)
    with pytest.raises(ValueError) as excinfo:  
        uc.get_user_by_email(email)
        
    assert str(excinfo.value) == 'Error: invalid email address'


@pytest.mark.unit
@pytest.mark.parametrize('email, obj', [('jan@.se', ValueError)])
def test_id6_get_user_by_email_failure(email, obj):

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
    assert uc.get_user_by_email('jandoe@test.se') == user1
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
