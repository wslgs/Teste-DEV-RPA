import os
import pyodbc
from dotenv import load_dotenv # type: ignore

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de conexão com o banco de dados a partir do .env
SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

def create_database():
    """
    Cria o banco de dados DemoQA.
    """
    try:
        # Conexão ao banco de dados master para criar o novo banco de dados
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={SQL_SERVER};'
            f'DATABASE={SQL_DATABASE};'  # Conectando-se ao banco de dados master para criar o banco de dados
            f'UID={SQL_USERNAME};'  # Nome de usuário
            f'PWD={SQL_PASSWORD};'  # Senha
            'TrustServerCertificate=yes;'
        )
        conn.autocommit = True  # Desabilita a transação automática
        cursor = conn.cursor()

        # Criando o banco de dados
        cursor.execute('CREATE DATABASE DemoQA')
        
        cursor.close()
        conn.close()
        print('Banco de dados criado com sucesso')
    except pyodbc.Error as e:
        if '1801' in str(e):
            print('Banco de dados já existe. Pulando a criação do banco de dados.')
        else:
            print(f'Erro ao criar banco de dados: {e}')

def create_table():
    """
    Cria a tabela Books no banco de dados DemoQA.
    """
    try:
        # Conexão ao novo banco de dados DemoQA para criar a tabela
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={SQL_SERVER};'
            f'DATABASE=DemoQA;'  # Conectando-se ao banco de dados DemoQA
            f'UID={SQL_USERNAME};'  # Nome de usuário
            f'PWD={SQL_PASSWORD};'  # Senha
            'TrustServerCertificate=yes;'
        )
        cursor = conn.cursor()

        # Criando a tabela Books
        cursor.execute('''
            CREATE TABLE Books (
                id INT IDENTITY(1,1) PRIMARY KEY,
                image NVARCHAR(MAX),
                title NVARCHAR(255),
                author NVARCHAR(255),
                publisher NVARCHAR(255)
            )
        ''')

        conn.commit()
        cursor.close()
        conn.close()
        print('Tabela criada com sucesso')
    except pyodbc.Error as e:
        if '2714' in str(e):
            print('A tabela já existe. Pulando a criação da tabela.')
        else:
            print(f'Erro ao criar a tabela: {e}')

if __name__ == "__main__":
    create_database()
    create_table()
