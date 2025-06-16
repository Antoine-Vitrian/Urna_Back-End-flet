from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from banco_de_dados import db
from passlib.hash import bcrypt

router = APIRouter(prefix='/users', tags=['users'])

class Login(BaseModel):
    cpf: str
    senha: str

class User(BaseModel):
    cpf: str
    nome: str
    senha: str

@router.get('/')
async def get_users():
    # consultar o banco para conseguir a lista de usuários
    try:
        dados = db.ver_eleitores()
        
        eleitores = [{'cpf': cpf, 'nome': nome, } for cpf, nome in dados]
        return eleitores
    except Exception as erro:
        print('erro: ', erro, '\n', dados)
        raise HTTPException(status_code=500, detail='Erro interno do servidor')

@router.get('/{cpf}')
async def get_user(cpf: int):
    # consultar o banco para conseguir um usuário
    eleitor = db.ver_eleitor(cpf)
    print(eleitor)
    # condição: se o eleitor não existe retornar erro 404
    if not eleitor:
        raise HTTPException(status_code=404, detail='eleitor não encontrado')

    return {
        "cpf": eleitor[0],
        "nome": eleitor[1],
    }

@router.post('/criar_eleitor')
async def criar_usuario(user: User):
    # Registrar um usuário no banco de dados
    # se o cpf do usuário já existe retornar erro 409
    existe = True if db.ver_eleitor(user.cpf) else False

    if not existe: # caso o cpf seja novo
        if not len(user.cpf) == 11:
            raise HTTPException(status_code=400, detail='dados inválidos')

        senha_hash = bcrypt.hash(user.senha)
    
        # cria o eleitor
        eleitor = db.adicionar_eleitor(int(user.cpf), user.nome, senha_hash)

        if eleitor.get('erro'): # se ocorreu um erro
            raise HTTPException(status_code=500, detail="erro interno do servidor")
        
        return {'mensagem': 'sucesso'}
    else:
        raise HTTPException(status_code=409, detail='cpf já registrado no sistema')

@router.post('/login')
async def login(login: Login):
    check = db.verificar_senha(login.cpf)

    if check['check']:
        user = db.ver_eleitor(login.cpf)

        print(type(login.senha.encode()))
        print(type(check['senha']))

        if bcrypt.verify(login.senha, check['senha']):
            return User(cpf=user[0], nome=user[1], senha='***')
        else:
            raise HTTPException(status_code=401, detail="Senha incorreta")
    else:
        raise HTTPException(status_code=404, detail="usuario nao encontrado")
