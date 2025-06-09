from fastapi import APIRouter, HTTPException, Path

router = APIRouter(prefix='/candidatos', tags=['candidatos'])

@router.get('/')
def get_candidatos():
    pass
    # consultar o banco de dados para conseguir a lista de todos os candidatos

@router.get('/{num_cand}')
# função que possui um parâmetro que tem uma descrição, o valor padrão é None, então um erro irá acontecer se nenhum parâmetro for passado
def get_candidato(num_cand: int = Path(..., description='O número do candidato que deseja votar')):
    pass
    # consultar o banco de dados para conseguir o candidato pelo número, 

@router.post('/')
def cadastrar_candidato(numero: int, nome: str, partido: str, slogan: str, proposta: str):
    pass
    # cadastra o candidato no banco