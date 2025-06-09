from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/votos', tags=['votos'])

@router.get('/')
def get_votos():
    pass
    # consulta o banco para conseguir os votos por candidatos

@router.post('/')
def votar(usuario: int, num_cand: int):
    pass
    # registra voto