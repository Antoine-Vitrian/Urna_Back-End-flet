from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from banco_de_dados import db

router = APIRouter(prefix='/votos', tags=['votos'])

class Voto(BaseModel):
    cpf_eleitor: str
    num_cand: int

@router.get('/')
def get_votos():
    # consulta o banco para conseguir os votos por candidatos
    votos = db.ver_votos_function()
    print(votos)
    return votos

@router.post('/votar')
def votar(voto: Voto):
    # registra voto
    response = db.votar(voto.cpf_eleitor, voto.num_cand)

    print(response)

    if response['mensagem'] == 'sucesso':
        return {'status_code': 200}
    else:
        raise HTTPException(status_code=500)
