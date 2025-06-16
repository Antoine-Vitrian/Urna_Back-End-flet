# Banco de Dados Urna

# Importando SQLite3
import sqlite3

# Conectando e criando o Banco de Dados ao código
connection = sqlite3.connect("urna_futuro.db")

# Cria um cursor que executará códigos SQL
cursor = connection.cursor()

# Manipulando dados com SQL

# Criando Tabelas

# Tabela de Tipos de Usuário
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tipo_usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT
    )
''')

# Tabela de Eleitores
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        cpf TEXT PRIMARY KEY,
        nome TEXT,
        senha TEXT,
        tipo INTEGER,
        FOREIGN KEY (tipo) REFERENCES tipo_usuario(id)  
    )
''')

# Tabela de Candidatos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidatos (
        numero INTEGER PRIMARY KEY,
        nome TEXT,
        partido TEXT,
        slogan TEXT,
        proposta TEXT     
    )
''')

# Tabela de Votos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS votos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eleitor INTEGER,
        candidato INTEGER,
        FOREIGN KEY (eleitor) REFERENCES eleitores(cpf),
        FOREIGN KEY (candidato) REFERENCES candidatos(numero)
    )
''')



# checa se a tabela tipo_usuario já foi preenchida
cursor.execute('SELECT * FROM tipo_usuario')
existe = True if len(cursor.fetchall()) > 0 else False

if not existe: # cria os tipos de usuários
    cursor.execute('''
    INSERT INTO tipo_usuario (tipo)
    VALUES('eleitor'), ('admin')
    ''')

# checa se o admin existe
cursor.execute('SELECT * FROM usuarios WHERE tipo = 2')
existe = True if len(cursor.fetchall()) > 0 else False

if not existe:
    cursor.execute('''
INSERT INTO usuarios (cpf, nome, senha, tipo)
VALUES (11111111111, 'Admin', 'senha_supersecreta', 2)
''')

# Views
cursor.execute('''
    CREATE VIEW IF NOT EXISTS votos_por_candidato AS
        SELECT 
            c.numero,
            c.nome,
            c.partido,
            COUNT(v.id) AS total_votos,
            ROUND(
                100.0 * COUNT(v.id) / (
                    SELECT COUNT(*) FROM votos
                ), 2
            ) AS porcentagem_votos
        FROM candidatos c
        LEFT JOIN votos v ON c.numero = v.candidato
        GROUP BY c.numero, c.nome, c.partido;
''')

# Fechando a conexão
connection.close()

# Funções para facilitar visualizações no Front-End

def ver_votos_function():
    connection = sqlite3.connect("urna_futuro.db")
    cursor = connection.cursor()
    # Executa a View
    votos = cursor.execute('''
    SELECT 
        nome,
        total_votos
    FROM votos_por_candidato
''').fetchall()
    
    connection.close()
    return votos
    
def ver_candidatos():
    connection = sqlite3.connect("urna_futuro.db")
    cursor = connection.cursor()
    
    candidatos = cursor.execute('''
    SELECT * FROM candidatos
''').fetchall()
    
    connection.close()
    return candidatos

def ver_eleitores():
    connection = sqlite3.connect("urna_futuro.db")
    cursor = connection.cursor()
    
    eleitores = cursor.execute('''
SELECT cpf, nome
FROM usuarios
WHERE tipo = 1
''').fetchall()
    
    connection.close()
    return eleitores

def ver_candidato(num):
    connection = sqlite3.connect("urna_futuro.db")
    cursor = connection.cursor()

    candidato = cursor.execute('''
SELECT * 
FROM candidatos
WHERE numero = ?
''', (num,)).fetchall()
    
    if len(candidato) > 0:
        return candidato[0]
    else:
        return None

def ver_eleitor(cpf):
    connection = sqlite3.connect("urna_futuro.db")
    cursor = connection.cursor()

    eleitor = cursor.execute('''
SELECT * 
FROM usuarios
WHERE cpf = ? AND tipo = 1
''', (cpf,)).fetchall()
    
    if len(eleitor) > 0:
        return eleitor[0]
    else:
        return None

# Função pra cadastrar candidatos
def adicionar_candidato(number, name, partido_politico, slogans, propostas):
    connection = sqlite3.connect("urna_futuro.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO candidatos (numero, nome, partido, slogan, proposta)
            VALUES (?, ?, ?, ?, ?)
        """, (
            number,
            name,
            partido_politico,
            slogans,
            propostas
        ))
        connection.commit()

        return {'mensagem': 'sucesso ao adicionar'}
    except Exception as erro:
        print("Erro ao adicionar candidato:", erro)
        return {
            'mensagem': 'erro ao adicionar candidato',
            'erro': erro    
        }

    finally:
        connection.close()

# Função para cadastrar eleitor
def adicionar_eleitor(cpf, nome, senha):
    connection = sqlite3.connect("urna_futuro.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (cpf, nome, senha, tipo)
            VALUES (?, ?, ?, 1)
        """, (
            cpf,
            nome,
            senha
        ))
        connection.commit()

        return {
            'mensagem': 'Sucesso ao adicionar eleitor.'
        }

    except Exception as erro:
        print("Erro ao adicionar eleitor:", erro)
        return {
            'mensagem': 'Erro ao adicionar eleitor.',
            'erro': erro
        }
    finally:
       connection.close()

# Função para adicionar voto
def votar(eleitor, candidato):
    connection = sqlite3.connect("urna_futuro.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO votos (eleitor, candidato)
            VALUES (?, ?)
        """, (
            eleitor,
            candidato
        ))
        connection.commit()

        teste = cursor.execute("""
SELECT * 
FROM votos
ORDER BY id DESC
LIMIT 1
""").fetchall()

        print(teste)

        return {'mensagem': 'sucesso'}

    except Exception as erro:
        print("Erro ao adicionar voto:", erro)

        return {
            'mensagem': 'Erro ao adicionar voto',
            'erro': str(erro)
        }

    finally:
        connection.close()

def verificar_senha(cpf):
    connection = sqlite3.connect("urna_futuro.db")
    cursor = connection.cursor()
    try:
        cursor.execute('''
SELECT cpf, senha
FROM usuarios
WHERE cpf = ?
''', (cpf,))
        user = cursor.fetchall()
        
        if len(user) > 0:
            return {
                "cpf": user[0][0],
                "senha": user[0][1],
                "check": True
            }
        else:
            return {
                "erro": "usuario nao encontrado",
                'check': False
            }
    except Exception as erro:
        print('erro no banco:', str(erro))
        return {'mensagem': str(erro), 'check': False}
    finally:
        connection.close()