import os
import logging
import pandas as pd
import pyodbc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from dotenv import load_dotenv # type: ignore
from datetime import datetime

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de conexão com o banco de dados a partir do .env
SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = 'DemoQA'
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

# Caminho para o ChromeDriver a partir do .env
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')

# Credenciais de login para o site DemoQA a partir do .env
DEMOQA_USERNAME = os.getenv('DEMOQA_USERNAME')
DEMOQA_PASSWORD = os.getenv('DEMOQA_PASSWORD')

# Caminho para o diretório de logs
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Caminho para o diretório de reports
reports_directory = 'reports'
if not os.path.exists(reports_directory):
    os.makedirs(reports_directory)

# Configuração do logging
logger = logging.getLogger('MeuSistemaLogger')
logger.setLevel(logging.INFO)

# Criar handlers para o logger
file_handler = logging.FileHandler(os.path.join(log_directory, 'rpa_log.log'))
console_handler = logging.StreamHandler()

# Criar formatação e adicionar aos handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Adicionar handlers ao logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Variável global para armazenar erros
error_reports = []

def save_error_report():
    """
    Salva as mensagens de erro acumuladas em um arquivo de relatório na pasta reports.
    """
    if error_reports:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        report_filename = os.path.join(reports_directory, f'report_{timestamp}.txt')
        with open(report_filename, 'w') as file:
            for error in error_reports:
                file.write(error + '\n')

def add_error_report(error_message):
    """
    Adiciona uma mensagem de erro à lista de erros.

    Args:
        error_message (str): Mensagem de erro a ser adicionada.
    """
    error_reports.append(error_message)

def login_demoqa(driver, username, password):
    """
    Realiza o login no site DemoQA.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver do Chrome.
        username (str): Nome de usuário para login.
        password (str): Senha para login.
    """
    try:
        logger.info('Iniciando processo de login')
        driver.get('https://demoqa.com/login')

        # Encontrar e preencher os campos de login
        user_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userName')))
        pass_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.ID, 'login')

        user_field.send_keys(username)
        pass_field.send_keys(password)

        # Garantir que o botão de login esteja visível e clicável
        driver.execute_script("arguments[0].scrollIntoView();", login_button)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login')))
        login_button.click()

        # Esperar até que a URL contenha 'profile', indicando sucesso no login
        WebDriverWait(driver, 10).until(EC.url_contains('profile'))
        logger.info('Login realizado com sucesso')
    except Exception as e:
        error_message = f'Erro durante o login: {e}'
        logger.error(error_message)
        add_error_report(error_message)

def interact_with_elements(driver):
    """
    Interage com a seção "Elements" do DemoQA.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver do Chrome.
    """
    try:
        logger.info('Interagindo com a seção Elements')
        driver.get('https://demoqa.com/elements')
        # Adicione interações específicas aqui
        logger.info('Interação com Elements concluída com sucesso')
    except Exception as e:
        error_message = f'Erro durante a interação com Elements: {e}'
        logger.error(error_message)
        add_error_report(error_message)

def interact_with_forms(driver):
    """
    Interage com a seção "Forms" do DemoQA.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver do Chrome.
    """
    try:
        logger.info('Interagindo com a seção Forms')
        driver.get('https://demoqa.com/forms')
        # Adicione interações específicas aqui
        logger.info('Interação com Forms concluída com sucesso')
    except Exception as e:
        error_message = f'Erro durante a interação com Forms: {e}'
        logger.error(error_message)
        add_error_report(error_message)

def interact_with_alerts_frames_windows(driver):
    """
    Interage com a seção "Alerts, Frame & Windows" do DemoQA.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver do Chrome.
    """
    try:
        logger.info('Interagindo com a seção Alerts, Frame & Windows')
        driver.get('https://demoqa.com/alertsWindows')
        # Adicione interações específicas aqui
        logger.info('Interação com Alerts, Frame & Windows concluída com sucesso')
    except Exception as e:
        error_message = f'Erro durante a interação com Alerts, Frame & Windows: {e}'
        logger.error(error_message)
        add_error_report(error_message)

def interact_with_widgets(driver):
    """
    Interage com a seção "Widgets" do DemoQA.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver do Chrome.
    """
    try:
        logger.info('Interagindo com a seção Widgets')
        driver.get('https://demoqa.com/widgets')
        # Adicione interações específicas aqui
        logger.info('Interação com Widgets concluída com sucesso')
    except Exception as e:
        error_message = f'Erro durante a interação com Widgets: {e}'
        logger.error(error_message)
        add_error_report(error_message)

def interact_with_interactions(driver):
    """
    Interage com a seção "Interactions" do DemoQA.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver do Chrome.
    """
    try:
        logger.info('Interagindo com a seção Interactions')
        driver.get('https://demoqa.com/interaction')
        # Adicione interações específicas aqui
        logger.info('Interação com Interactions concluída com sucesso')
    except Exception as e:
        error_message = f'Erro durante a interação com Interactions: {e}'
        logger.error(error_message)
        add_error_report(error_message)

def collect_book_data(driver):
    """
    Coleta dados dos livros disponíveis na seção "Book Store Application" do DemoQA.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver do Chrome.

    Returns:
        list: Lista de dicionários contendo os dados dos livros.
    """
    book_data = []
    try:
        logger.info('Iniciando coleta de dados dos livros')
        driver.get('https://demoqa.com/books')
        while True:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-tr-group')))

            # Encontrar todos os livros na tabela
            books = driver.find_elements(By.CLASS_NAME, 'rt-tr-group')

            for book in books:
                try:
                    # Verificar se todos os campos necessários estão presentes
                    img_element = book.find_elements(By.XPATH, './/img')
                    title_element = book.find_elements(By.XPATH, './/span[@id]')
                    author_elements = book.find_elements(By.XPATH, './/div[@class="rt-td" and @role="gridcell"]')

                    if img_element and title_element and len(author_elements) >= 4:
                        image = img_element[0].get_attribute('src')
                        title = title_element[0].text
                        author = author_elements[2].text
                        publisher = author_elements[3].text

                        book_data.append({
                            "image": image,
                            "title": title,
                            "author": author,
                            "publisher": publisher
                        })
                except (NoSuchElementException, TimeoutException) as e:
                    error_message = f'Erro ao coletar dados de um livro: {e}\nHTML do elemento: {book.get_attribute("outerHTML")}\nStacktrace: {e.stacktrace}'
                    logger.error(error_message)
                    add_error_report(error_message)
                    continue
            
            try:
                # Verificar se o botão "Next" está habilitado
                next_button = driver.find_element(By.XPATH, '//button[text()="Next"]')
                if 'disabled' in next_button.get_attribute('class'):
                    logger.info('Já está na última página de livros disponíveis.')
                    break  # Se o botão "Next" está desabilitado, saímos do loop
                else:
                    next_button.click()  # Clicar no botão "Next"
                    WebDriverWait(driver, 10).until(EC.staleness_of(books[0]))  # Esperar até que a página seja atualizada
            except NoSuchElementException:
                logger.info('Botão "Next" não encontrado, terminando coleta.')
                break  # Se o botão "Next" não for encontrado, saímos do loop
            except ElementClickInterceptedException:
                logger.info('Já está na última página de livros disponíveis.')
                break  # Se o botão "Next" não for clicável, saímos do loop

        logger.info('Dados dos livros coletados com sucesso')
    except Exception as e:
        error_message = f'Erro na coleta de dados dos livros: {e}'
        logger.error(error_message)
        add_error_report(error_message)
    return book_data

def save_to_database(book_data):
    """
    Salva os dados dos livros em um banco de dados SQL Server.

    Args:
        book_data (list): Lista de dicionários contendo os dados dos livros.
    """
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={SQL_SERVER};'
            f'DATABASE={SQL_DATABASE};'
            f'UID={SQL_USERNAME};'
            f'PWD={SQL_PASSWORD};'
            'TrustServerCertificate=yes;'
        )
        cursor = conn.cursor()

        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Books' and xtype='U')
            CREATE TABLE Books (
                id INT IDENTITY(1,1) PRIMARY KEY,
                image NVARCHAR(MAX),
                title NVARCHAR(255),
                author NVARCHAR(255),
                publisher NVARCHAR(255)
            )
        ''')

        for book in book_data:
            cursor.execute('''
                INSERT INTO Books (image, title, author, publisher)
                VALUES (?, ?, ?, ?)
            ''', book['image'], book['title'], book['author'], book['publisher'])

        conn.commit()
        cursor.close()
        conn.close()
        logger.info('Dados salvos no banco de dados com sucesso')
    except Exception as e:
        error_message = f'Erro ao salvar dados no banco de dados: {e}'
        logger.error(error_message)
        add_error_report(error_message)

def export_to_csv(book_data):
    """
    Exporta os dados dos livros para um arquivo CSV.

    Args:
        book_data (list): Lista de dicionários contendo os dados dos livros.
    """
    try:
        df = pd.DataFrame(book_data)
        df.to_csv('data/books.csv', index=False)
        logger.info('Dados exportados para CSV com sucesso')
    except Exception as e:
        error_message = f'Erro ao exportar dados para CSV: {e}'
        logger.error(error_message)
        add_error_report(error_message)

if __name__ == '__main__':
    driver = None
    try:
        logger.info('Inicializando o WebDriver do Chrome')
        
        # Configuração para suprimir mensagens de erro do ChromeDriver
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        logger.info('WebDriver inicializado com sucesso')

        # Realizar login e coleta de dados
        login_demoqa(driver, DEMOQA_USERNAME, DEMOQA_PASSWORD)
        
        # Interagir com cada seção
        interact_with_elements(driver)
        interact_with_forms(driver)
        interact_with_alerts_frames_windows(driver)
        interact_with_widgets(driver)
        interact_with_interactions(driver)
        
        # Coletar dados da Book Store Application
        book_data = collect_book_data(driver)
        
        # Salvar dados no banco de dados
        save_to_database(book_data)
        
        # Exportar dados para CSV
        export_to_csv(book_data)

        logger.info(f'Dados coletados: {book_data}')
    except Exception as e:
        error_message = f'Erro na execução principal: {e}'
        logger.error(error_message)
        add_error_report(error_message)
    finally:
        if driver:
            driver.quit()
            logger.info('WebDriver fechado')
        save_error_report()
