from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from banco_de_dados import db

router = APIRouter(prefix='/votos', tags=['votos'])

class Voto(BaseModel):
    num_cand: int
    cpf_eleitor: int

@router.get('/')
def get_votos():
    pass
    # consulta o banco para conseguir os votos por candidatos

@router.post('/votar')
def votar(usuario: int, num_cand: int):
    pass
    # registra voto