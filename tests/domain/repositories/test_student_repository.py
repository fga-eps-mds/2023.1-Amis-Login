from unittest import mock
from unittest.mock import MagicMock, patch
import pytest
from src.domain.models.student import Status, Student, StudentResponse
from src.infrastructure.repositories.student_repository import StudentRepository
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))


def generate_session():
    return MagicMock(spec=Session)


def test_find_all():
    # Arrange
    database = generate_session()
    student_repository = StudentRepository(database)
    expected_result = [Student(), Student()]
    database().query().all.return_value = expected_result

    # Act
    result = student_repository.find_all_student()

    # Assert
    assert result == expected_result


def test_save_new_student():
    # Arrange
    database = generate_session()
    test_session = database

    student = Student(
        bairro= "Test Bairro",
        cep= "12345678",
        cidade= "Test City",
        cpf= "17553041025",
        data_nascimento= "2000-01-01",
        deficiencia= False,
        descricao_endereco= "Test Address",
        email= "testamis@gmail.com",
        login= "amisteste2",
        nome= "amisteste1",
        senha= "testpassword",
        status= 1,
        telefone= "12234567890"
    )
    test_session.query().filter().first.return_value = None
    student_repository = StudentRepository(database)

    # Act
    result = student_repository.save_student(student)

    # Assert"12234567890"
    assert result == student

    test_session.close()


def test_validateStudent():
    student = Student(
        bairro= "Test Bairro",
        cep= "12345678",
        cidade= "Test City",
        cpf= "17553041025",
        data_nascimento= "2000-01-01",
        deficiencia= False,
        descricao_endereco= "Test Address",
        email= "testamis@gmail.com",
        login= "amisteste2",
        nome= "amisteste1",
        senha= "testpassword",
        status= Status.PRODUCAO,
        telefone= "12234567890"
    )

    database = generate_session()

    result = StudentRepository(database).validate_student(student)
    
    assert result['bairro']['status'] is True
    assert result['cep']['status'] is True
    assert result['cidade']['status'] is True
    assert result['cpf']['status'] is True
    assert result['dNascimento']['status'] is True
    assert result['email']['status'] is True
    assert result['login']['status'] is True
    assert result['nome']['status'] is True
    assert result['senha']['status'] is True
    assert result['status']['status'] is True
    assert result['telefone']['status'] is True
    assert result['completeStatus'] is True

def test_invalidateStudent():
   ## Arrange
    student = Student(
        bairro= "Test Bairro",
        cep= "12345678",
        cidade= "Test City",
        cpf='07497550',  # cpf inválido
        data_nascimento= "2000-01-01",
        deficiencia= False,
        descricao_endereco= "Test Address",
        email= "testamis@gmail.com",
        login= "amisteste2",
        nome= "amisteste1",
        senha= "testpassword",
        status= Status.PRODUCAO,
        telefone= "12234567890"
    )

    database = generate_session()
    result = StudentRepository(database).validate_student(student)

    assert result['bairro']['status'] is True
    assert result['cep']['status'] is True
    assert result['cidade']['status'] is True
    assert result['cpf']['status'] is False
    assert result['dNascimento']['status'] is True
    assert result['email']['status'] is True
    assert result['login']['status'] is True
    assert result['nome']['status'] is True
    assert result['senha']['status'] is True
    assert result['status']['status'] is True
    assert result['telefone']['status'] is True
    assert result['completeStatus'] is False



def test_invalidateStudent_2():
  ##  Arrange
    student = Student(
        bairro= "Test Bairro",
        cep= "12345678",
        cidade= "Test City",
        cpf= "17553041025",
        data_nascimento= "2000-01-01",
        deficiencia= False,
        descricao_endereco= "Test Address",
        email= "testamis@gmail.com",
        login= "amisteste2",
        nome= "amisteste1",
        senha= "testpassword",
        status= Status.PRODUCAO,
        telefone= "112566"
    )

    database = generate_session()
    result = StudentRepository(database).validate_student(student)

    assert result['bairro']['status'] is True
    assert result['cep']['status'] is True
    assert result['cidade']['status'] is True
    assert result['cpf']['status'] is True
    assert result['dNascimento']['status'] is True
    assert result['email']['status'] is True
    assert result['login']['status'] is True
    assert result['nome']['status'] is True
    assert result['senha']['status'] is True
    assert result['status']['status'] is True
    assert result['telefone']['status'] is False
    assert result['completeStatus'] is False

@mock.patch("infrastructure.repositories.student_repository")
def test_find_all(mock_repository):
    # Criação do mock do repositório
    mock_repository_instance = mock_repository.return_value
    mock_repository_instance.find_all.return_value = [
        StudentResponse(
            bairro= "Test Bairro",
            cep= "12345678",
            cidade= "Test City",
            cpf= "17553041025",
            data_nascimento= "2000-01-01",
            deficiencia= False,
            descricao_endereco= "Test Address",
            email= "testamis@gmail.com",
            login= "amisteste2",
            nome= "amisteste1",
            senha= "testpassword",
            status= Status.PRODUCAO,
            telefone= "12234567890"
        )
    ]

    students = mock_repository_instance.find_all()

    mock_repository_instance.find_all.assert_called_once()

    # Verifica o resultado retornado pela função
    assert len(students) == 1
    assert students[0].bairro == "Test Bairro"
    assert students[0].cep == "12345678"
    assert students[0].cidade == "Test City"
    assert students[0].cpf == "17553041025"
    assert students[0].data_nascimento == "2000-01-01"
    assert students[0].deficiencia is False
    assert students[0].descricao_endereco == "Test Address"
    assert students[0].email == "testamis@gmail.com"
    assert students[0].login == "amisteste2"
    assert students[0].nome == "amisteste1"
    assert students[0].senha == "testpassword"
    assert students[0].status == Status.PRODUCAO
    assert students[0].telefone == "12234567890"
