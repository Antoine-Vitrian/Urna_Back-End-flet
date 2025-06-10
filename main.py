from fastapi import FastAPI
from routers import candidatos, users, votos

app = FastAPI()
# routers
app.include_router(candidatos.router)
app.include_router(users.router)
app.include_router(votos.router)

@app.get('/')
def root():
    return 'oi'