from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from banco_de_dados import db

router = APIRouter(prefix='/users', tags=['users'])

class User(BaseModel):
    cpf: int
    nome: str
    rg: int
    idade: int
    tipo: int

@router.get('/')
def get_users():
    # consultar o banco para conseguir a lista de usuários
    users = None # trocar pela função que retorna todos os usuários

@router.get('/{user_id}')
def get_user(user_id: int):
    # consultar o banco para conseguir um usuário
    user = None #trocar por função que retorna um usuário

    # condição: se o usuário não existe retornar erro 404

    return user

@router.post('/criar_usuario')
def criar_usuario(user: User):
    # Registrar um usuário no banco de dados
    # executar função para registrar no banco de dados

    #condição: se o cpf do usuário já existe retornar erro 409

    # retornar status 200 se tudo estiver certo
    pass