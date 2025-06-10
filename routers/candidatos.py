from fastapi import APIRouter, Path
from typing import Optional
from pydantic import BaseModel
from banco_de_dados import db

router = APIRouter(prefix='/candidatos', tags=['candidatos'])

class Candidato(BaseModel):
    numero: int
    nome: str
    partido: str
    slogan: Optional[str] = None
    proposta: str    

@router.get('/')
def get_candidatos():
    # consultar o banco de dados para conseguir a lista de todos os candidatos
    candidatos = None # trocar por função que retorna todos os candidatos

    return candidatos

@router.get('/{num_cand}')
# função que possui um parâmetro que tem uma descrição, o valor padrão é None, então um erro irá acontecer se nenhum parâmetro for passado
def get_candidato(num_cand: int = Path(..., description='O número do candidato que deseja votar')):
    # consultar o banco de dados para conseguir o candidato pelo número, 
    candidato = None # função do banco de dados que consegue um candidato

    # condição: se o candidato não existe retornar erro 404

    return candidato

@router.post('/cadastrar')
def cadastrar_candidato(candidato: Candidato):
    # cadastra o candidato no banco
    candidato = None # trocar por função que cadastra o candidato
    # condição se o número do candidato já existe, retornar erro 409 (conflict)
