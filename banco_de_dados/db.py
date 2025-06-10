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
    CREATE TABLE IF NOT EXISTS eleitores (
        cpf TEXT PRIMARY KEY,
        nome TEXT,
        rg TEXT,
        data_nasc DATE,
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

# Fechando a conexão
connection.close()

# Funções para facilitar visualizações no Front-End

def ver_votos_function():
    connection = sqlite3.connect("urna_futuro.db")

    # Cria a View
    cursor.execute('''
    CREATE VIEW votos_por_candidato AS
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

# Funções para facilitar visualizações no Front-End

def ver_votos_function():
    # Executa a View
    dados = cursor.execute('''
    SELECT 
        nome,
        total_votos
    FROM votos_por_candidato
''').fetchall()
    
    print(dados)
    
def ver_candidatos():
    connection = sqlite3.connect("urna_futuro.db")
    cursor.execute('''
    SELECT * FROM candidatos
''').fetchall()
    
    connection.close()

def ver_eleitor():
    connection = sqlite3.connect("urna_futuro.db")
    cursor.execute('''
    SELECT * FROM eleitores
''').fetchall()
    
    connection.close()
    
# Função pra cadastrar candidatos
def adicionar_candidato(number, name, partido_politico, slogans, propostas):
    connection = sqlite3.connect("urna_futuro.db")
    try:
        cursor.execute("""
            INSERT INTO candidatos (numero, nome, partido, slogan, propostas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            number.value,
            name.value,
            partido_politico.value,
            slogans.value,
            propostas.value
        ))
        connection.commit()

        # Limpa os campos
        for campo in [number, name, partido_politico, slogans, propostas]:
            campo.value = ""

    except Exception as erro:
        print("Erro ao adicionar candidato:", erro)

        connection.close()

# Função para cadastrar eleitor
def adicionar_eleitor(cpf, nome, rg, tipo_usuario):
    connection = sqlite3.connect("urna_futuro.db")
    try:
        cursor.execute("""
            INSERT INTO eleitores (cpf, nome, rg, tipo_usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cpf.value,
            nome.value,
            rg.value,
            tipo_usuario.value
        ))
        connection.commit()

        # Limpa os campos
        for campo in [cpf, nome, rg, tipo_usuario]:
            campo.value = ""

    except Exception as erro:
        print("Erro ao adicionar eleitor:", erro)

    connection.close()

# Função para adicionar voto
def votar(eleitor, candidato):
    connection = sqlite3.connect("urna_futuro.db")
    try:
        cursor.execute("""
            INSERT INTO votos (numero, nome, partido, slogan, propostas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            eleitor.value,
            candidato.value
        ))
        connection.commit()

        # Limpa os campos
        for campo in [eleitor, candidato]:
            campo.value = ""

    except Exception as erro:
        print("Erro ao adicionar voto:", erro)

    connection.close()
