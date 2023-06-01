import pytest
from httpx import AsyncClient
from fastapi import status




GLOBAL_RESPONSE = []
HTTPS_STUDENT = "http://localhost:9090"

# CREATE
@pytest.mark.asyncio
async def test_create_student():
    '''Função para testar a criação de uma student'''
    data = {        
        "bairro": "Test Bairro",
        "cep": "12345678",
        "cidade": "Test City",
        "cpf": "17553041025",
        "data_nascimento": "2000-01-01",
        "deficiencia": False,
        "descricao_endereco": "Test Address",
        "email": "testamis@gmail.com",
        "login": "amisteste2",
        "nome": "amisteste1",
        "senha": "testpassword",
        "status": 1,
        "telefone": "12234567890"
    }
    async with AsyncClient(base_url=HTTPS_STUDENT, timeout=30.0) as async_client:
        response = await async_client.post("/student/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

# GET ALL
@pytest.mark.asyncio
async def test_read_all_student():
    '''Função para testar exibição de todas socialWorker (ainda sem paginação)'''
    async with AsyncClient(base_url=HTTPS_STUDENT, timeout=30.0) as async_client:
        response = await async_client.get("/student/")
    assert response.status_code == status.HTTP_200_OK


# FIND BY LOGIN
@pytest.mark.asyncio
async def test_find_by_login_student():
    '''Função para testar a busca de uma student por login'''
    login = "amisteste2"
    async with AsyncClient(base_url=HTTPS_STUDENT, timeout=30.0) as async_client:
        response = await async_client.get(f"/student/{login}")
    assert response.status_code == status.HTTP_200_OK


# UPDATE
@pytest.mark.asyncio
async def test_update_student():
    '''Função para testar a atualização de uma student'''
    data = {        
        "bairro": "Test Bairro",
        "cep": "12345678",
        "cidade": "Test City",
        "cpf": "17553041025",
        "data_nascimento": "2000-01-01",
        "deficiencia": False,
        "descricao_endereco": "Test Address",
        "email": "testamis123@gmail.com",
        "login": "amisteste2",
        "nome": "amisteste1",
        "senha": "testpassword",
        "status": 1,
        "telefone": "12234567890"
    }
    async with AsyncClient(base_url=HTTPS_STUDENT, timeout=30.0) as async_client:
        response = await async_client.put("/student/amisteste2", json=data)
    assert response.status_code == status.HTTP_200_OK

# DELETE
@pytest.mark.asyncio
async def test_delete_student():
    '''Função para testar a exclusão de uma student'''
    async with AsyncClient(base_url=HTTPS_STUDENT, timeout=30.0) as async_client:
        response = await async_client.delete("/student/amisteste2")
    assert response.status_code == status.HTTP_204_NO_CONTENT
