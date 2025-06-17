from fastapi import APIRouter, Path, HTTPException
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
    try:
        dados = db.ver_candidatos()
        
        candidatos = [{'numero': numero, 'nome': nome, 'partido': partido, 'slogan': slogan, 'proposta': proposta} for numero, nome, partido, slogan, proposta in dados]
        return candidatos
    except Exception as erro:
        print('erro: ', erro)
        raise HTTPException(status_code=500, detail='Erro interno do servidor')

@router.get('/{num_cand}')
# função que possui um parâmetro que tem uma descrição, o valor padrão é None, então um erro irá acontecer se nenhum parâmetro for passado
def get_candidato(num_cand: int = Path(..., description='O número do candidato que deseja votar')):
    # consultar o banco de dados para conseguir o candidato pelo número, 
    candidato = db.ver_candidato(num_cand)

    # condição: se o candidato não existe retornar erro 404
    if candidato is None:
        raise HTTPException(status_code=404, detail='Candidato não encontrado')

    return {
        "numero": candidato[0],
        "nome": candidato[1],
        "partido": candidato[2],
        "slogan": candidato[3],
        "partido": candidato[4]
    }

@router.post('/cadastrar')
def cadastrar_candidato(cand: Candidato):
    # cadastra o candidato no banco
    existe = True if db.ver_candidato(cand.numero) else False # checa se o número já existe
    
    if not existe: # caso o número seja novo
        # cria o candidato
        candidato = db.adicionar_candidato(cand.numero, cand.nome, cand.partido, cand.slogan, cand.proposta)
        
        if candidato.get('erro'): # se ocorreu erro
            raise HTTPException(status_code=500)
        
        return {'mensagem': 'sucesso'}
    else: 
        raise HTTPException(status_code=409, detail='Número de candidato já existente.')
