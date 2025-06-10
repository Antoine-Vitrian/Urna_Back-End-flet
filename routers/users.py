from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from banco_de_dados import db
from datetime import date, datetime

router = APIRouter(prefix='/users', tags=['users'])

class User(BaseModel):
    cpf: int
    nome: str
    rg: int
    data_nasc: str # formato deve ser YYYY-MM-DD

@router.get('/')
def get_users():
    # consultar o banco para conseguir a lista de usuários
    try:
        dados = db.ver_eleitores()
        
        eleitores = [{'cpf': cpf, 'nome': nome, 'rg': rg, 'data_nasc': data_nasc} for cpf, nome, rg, data_nasc in dados]
        return eleitores
    except Exception as erro:
        print('erro: ', erro, '\n', dados)
        raise HTTPException(status_code=500, detail='Erro interno do servidor')

@router.get('/{cpf}')
def get_user(cpf: int):
    # consultar o banco para conseguir um usuário
    eleitor = db.ver_eleitor(cpf)

    # condição: se o eleitor não existe retornar erro 404
    if not eleitor:
        raise HTTPException(status_code=404, detail='eleitor não encontrado')

    return {
        "cpf": eleitor[0],
        "nome": eleitor[1],
        "rg": eleitor[2],
        "data_nasc": eleitor[3]
    }

@router.post('/criar_eleitor')
def criar_usuario(user: User):
    # Registrar um usuário no banco de dados
    # se o cpf do usuário já existe retornar erro 409
    existe = True if db.ver_eleitor(user.cpf) else False

    if not existe: # caso o cpf seja novo
    

        # cria o eleitor
        eleitor = db.adicionar_eleitor(user.cpf, user.nome, user.rg)

        if eleitor.get('erro'): # se ocorreu um erro
            raise HTTPException(status_code=500)
        
        return {'mensagem': 'sucesso'}
    else:
        raise HTTPException(status_code=409, detail='cpf já registrado no sistema')
