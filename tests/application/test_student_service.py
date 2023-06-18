import pytest
from unittest.mock import MagicMock, Mock, patch
from application.student_service import StudentService
from domain.models.student import Student, Status
from fastapi.testclient import TestClient
import requests

@pytest.fixture
def student_repository_mock():
    return MagicMock()

@pytest.fixture
def tokens_repository_mock():
    return MagicMock()

@pytest.fixture
def client():
    from main import app
    with TestClient(app) as client:
        yield client

# def test_verify_token(student_repository_mock, tokens_repository_mock):
#     Mocking the necessary objects
#     tokens_repository_mock.verifyToken.return_value = "testuser2"
#     student = Student(
#         bairro= "Gama",
#         cep="49030-540",
#         cidade="Brasilia",
#         cpf="1234567890",
#         data_nascimento="2001-01-01",
#         deficiencia=False,
#         descricao_endereco="Nothing",
#         email="email@test.com",
#         login="testuser2",
#         nome="John Doe",
#         senha="password",
#         status=Status.PRODUCAO,
#         telefone="61921432134"
#     )
#     student_repository_mock.find_by_login.return_value = student

#     service = StudentService(
#         studentRepository=student_repository_mock,
#         tokensRepository=tokens_repository_mock
#     )

#     returned_student = service.verifyToken(token="testuser2")

#     assert returned_student == student
#     tokens_repository_mock.verifyToken.assert_called_once_with(token="testuser2")
#     student_repository_mock.find_by_login.assert_called_once_with("testuser2")

def test_refresh_session(tokens_repository_mock):
    tokens_repository_mock.verifyToken.return_value = True
    tokens_repository_mock.refreshToken.return_value = ("new_user_token", "new_refresh_token")

    service = StudentService(
        studentRepository=MagicMock(),
        tokensRepository=tokens_repository_mock
    )

    result = service.refreshSession(refresh_token="test_refresh_token")

    assert result == ("new_user_token", "new_refresh_token")
    tokens_repository_mock.verifyToken.assert_called_once_with(token="test_refresh_token")
    tokens_repository_mock.refreshToken.assert_called_once_with(refresh_token="test_refresh_token")
    
def test_failed_refresh_session_invalid_token(tokens_repository_mock):
    tokens_repository_mock.verifyToken.return_value = False

    service = StudentService(
        studentRepository=MagicMock(),
        tokensRepository=tokens_repository_mock
    )

    result = service.refreshSession(refresh_token="invalid_token")

    assert result is None

def test_delete_refresh_token(tokens_repository_mock):
    service = StudentService(
        studentRepository=MagicMock(),
        tokensRepository=tokens_repository_mock
    )

    result = service.delete_refresh_token(refresh_token="test_refresh_token")

    assert result is None
