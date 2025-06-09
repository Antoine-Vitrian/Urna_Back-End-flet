from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/')
def get_users():
    pass
    # consultar o banco para conseguir a lista de usuários

@router.get('/{user_id}')
def get_user(user_id: int):
    pass   
    # consultar o banco para conseguir um usuário