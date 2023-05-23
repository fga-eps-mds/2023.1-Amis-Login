import sys
from pathlib import Path
import pytest

# Adiciona o diretório "src" ao caminho de importação
sys.path.append(str(Path(__file__).resolve().parents[3]))

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.domain.repositories.student_repository import StudentRepository
from src.domain.models.student import Student

# Restante do código de teste...


# Test data
test_student_data = {
    "bairro": "Test Bairro",
    "cep": "12345-678",
    "cidade": "Test City",
    "cpf": "12345678901",
    "data_nascimento": "2000-01-01",
    "deficiencia": False,
    "descricao_endereco": "Test Address",
    "email": "test@example.com",
    "login": "testuser",
    "nome": "Test User",
    "senha": "testpassword",
    "status": "PRODUCAO",
    "telefone": "1234567890"
}

# Mocking Session class for testing
class MockSession:
    def merge(self, student):
        pass

    def add(self, student):
        pass

    def commit(self):
        pass

    def query(self, model):
        return self

    def all(self):
        return []

    def filter(self, condition):
        return self

    def first(self):
        return None

    def delete(self, student):
        pass

@pytest.fixture
def mock_db_session():
    return MockSession()

def test_save_student(mock_db_session):
    student_repo = StudentRepository()
    student = Student(**test_student_data)

    result = student_repo.save_student(mock_db_session, student)

    assert result == student

def test_find_all_student(mock_db_session):
    student_repo = StudentRepository()

    result = student_repo.find_all_student(mock_db_session)

    assert result == []

def test_find_by_login_student(mock_db_session):
    student_repo = StudentRepository()

    result = student_repo.find_by_login_student(mock_db_session, "testuser")

    assert result is None

def test_exists_by_cpf_student(mock_db_session):
    student_repo = StudentRepository()

    result = student_repo.exists_by_cpf_student(mock_db_session, "12345678901")

    assert result is False

def test_delete_by_login_student(mock_db_session):
    student_repo = StudentRepository()

    student_repo.delete_by_login_student(mock_db_session, "testuser")

    # No assertion, just making sure the function runs without errors

def test_update_by_login(mock_db_session):
    student_repo = StudentRepository()
    student = Student(**test_student_data)

    with pytest.raises(HTTPException) as exc:
        student_repo.update_by_login(mock_db_session, student)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert str(exc.value.detail) == "student não encontrado"

