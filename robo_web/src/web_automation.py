import os
import logging
import pandas as pd
import pyodbc
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from dotenv import load_dotenv # type: ignore
from datetime import datetime

# Diretórios necessários
directories = ['logs', 'data', 'reports']

# Criação dos diretórios, se não existirem
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

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
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_filename = os.path.join(reports_directory, f'report_{timestamp}.report')
    
    with open(report_filename, 'w') as file:
        if error_reports:
            for error in error_reports:
                file.write(error + '\n')
        else:
            file.write("Nenhum erro encontrado durante a execução.\n")

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
        
        # Clicar no item "Text Box" no menu à esquerda
        text_box_menu_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Text Box"]'))
        )
        text_box_menu_item.click()
        
        # Preencher os campos do formulário
        full_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'userName'))
        )
        email_field = driver.find_element(By.ID, 'userEmail')
        current_address_field = driver.find_element(By.ID, 'currentAddress')
        permanent_address_field = driver.find_element(By.ID, 'permanentAddress')
        time.sleep(2)
        
        full_name_field.send_keys('John Doe')
        email_field.send_keys('john.doe@example.com')
        current_address_field.send_keys('123 Current St, Current City')
        permanent_address_field.send_keys('456 Permanent St, Permanent City')
        time.sleep(2)
        
        # Rolar a página até o botão "Submit"
        submit_button = driver.find_element(By.ID, 'submit')
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(2)
        
        # Esperar até que o botão "Submit" esteja presente e clicável
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        
        logger.info('Formulário preenchido e enviado com sucesso')
        
        # Aguardar 2 segundos antes de sair da função
        time.sleep(2)
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
        driver.get('https://demoqa.com/automation-practice-form')
        
        # Preencher os campos do formulário
        first_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'firstName'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", first_name_field)
        first_name_field.send_keys('John')
        time.sleep(2)
        
        last_name_field = driver.find_element(By.ID, 'lastName')
        driver.execute_script("arguments[0].scrollIntoView(true);", last_name_field)
        last_name_field.send_keys('Doe')
        time.sleep(2)

        email_field = driver.find_element(By.ID, 'userEmail')
        driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
        email_field.send_keys('john.doe@example.com')
        time.sleep(2)

        gender_radio_button = driver.find_element(By.XPATH, '//label[text()="Male"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", gender_radio_button)
        gender_radio_button.click()
        time.sleep(2)

        mobile_field = driver.find_element(By.ID, 'userNumber')
        driver.execute_script("arguments[0].scrollIntoView(true);", mobile_field)
        mobile_field.send_keys('1234567890')
        time.sleep(2)

        # Interagir com o seletor de data de nascimento
        date_of_birth_field = driver.find_element(By.ID, 'dateOfBirthInput')
        driver.execute_script("arguments[0].scrollIntoView(true);", date_of_birth_field)
        date_of_birth_field.click()
        time.sleep(2)

        # Selecionar mês e ano
        month_select = driver.find_element(By.CLASS_NAME, 'react-datepicker__month-select')
        month_select.click()
        month_option = driver.find_element(By.XPATH, '//option[@value="2"]')  # Março é o mês 2 (0 indexado)
        month_option.click()
        time.sleep(2)

        year_select = driver.find_element(By.CLASS_NAME, 'react-datepicker__year-select')
        year_select.click()
        year_option = driver.find_element(By.XPATH, '//option[@value="1998"]')
        year_option.click()
        time.sleep(2)

        # Selecionar dia
        day_select = driver.find_element(By.XPATH, '//div[contains(@class, "react-datepicker__day--022") and not(contains(@class, "react-datepicker__day--outside-month"))]')
        day_select.click()
        time.sleep(2)
        
        subjects_field = driver.find_element(By.ID, 'subjectsInput')
        driver.execute_script("arguments[0].scrollIntoView(true);", subjects_field)
        subjects_field.send_keys('Math')
        subjects_field.send_keys(Keys.RETURN)
        time.sleep(2)

        hobbies_checkbox = driver.find_element(By.XPATH, '//label[text()="Sports"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", hobbies_checkbox)
        hobbies_checkbox.click()
        time.sleep(2)
        
        current_address_field = driver.find_element(By.ID, 'currentAddress')
        driver.execute_script("arguments[0].scrollIntoView(true);", current_address_field)
        current_address_field.send_keys('123 Current St, Current City')
        time.sleep(2)
        
        # Selecionar estado e cidade usando a caixa de seleção autocompletar
        state_dropdown = driver.find_element(By.ID, 'react-select-3-input')
        driver.execute_script("arguments[0].scrollIntoView(true);", state_dropdown)
        state_dropdown.send_keys('NCR')
        state_dropdown.send_keys(Keys.RETURN)
        time.sleep(2)
        
        city_dropdown = driver.find_element(By.ID, 'react-select-4-input')
        driver.execute_script("arguments[0].scrollIntoView(true);", city_dropdown)
        city_dropdown.send_keys('Delhi')
        city_dropdown.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # Rolar a página até o botão "Submit"
        submit_button = driver.find_element(By.ID, 'submit')
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        
        # Esperar até que o botão "Submit" esteja presente e clicável
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        time.sleep(2)

        logger.info('Formulário preenchido e enviado com sucesso')
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
        time.sleep(2)
        
        # Clicar no item "Browser Windows" no menu à esquerda
        browser_windows_menu_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Browser Windows"]'))
        )
        browser_windows_menu_item.click()
        time.sleep(2)
        
        # Clicar no botão "New Tab"
        new_tab_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'tabButton'))
        )
        new_tab_button.click()
        time.sleep(2)
        
        # Alternar para a nova aba
        driver.switch_to.window(driver.window_handles[1])
        logger.info('Nova aba aberta')
        time.sleep(2)
        
        # Fechar a nova aba
        driver.close()
        logger.info('Nova aba fechada')
        time.sleep(2)
        
        # Alternar de volta para a aba original
        driver.switch_to.window(driver.window_handles[0])
        logger.info('Retornado para a aba original')
        
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
        time.sleep(2)

        # Clicar no item "Accordian" no menu à esquerda
        accordian_menu_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Accordian"]'))
        )
        accordian_menu_item.click()
        time.sleep(2)
        
        # Fechar "What is Lorem Ipsum?" que já está aberto
        lorem_ipsum_section = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'section1Heading'))
        )
        lorem_ipsum_section.click()  # Fechar
        logger.info('Fechou "What is Lorem Ipsum?"')
        time.sleep(2)

        # Expandir e fechar "Where does it come from?"
        where_from_section = driver.find_element(By.ID, 'section2Heading')
        where_from_section.click()
        logger.info('Expandiu "Where does it come from?"')
        time.sleep(2)
        where_from_section.click()
        logger.info('Fechou "Where does it come from?"')
        time.sleep(2)

        # Expandir e fechar "Why do we use it?"
        why_use_section = driver.find_element(By.ID, 'section3Heading')
        why_use_section.click()
        logger.info('Expandiu "Why do we use it?"')
        time.sleep(2)
        why_use_section.click()
        logger.info('Fechou "Why do we use it?"')
        time.sleep(2)

        logger.info('Interação com Widgets concluída com sucesso')
    except Exception as e:
        error_message = f'Erro durante a interação com Widgets: {e}'
        logger.error(error_message)
        add_error_report(error_message)

from selenium.webdriver import ActionChains

def interact_with_interactions(driver):
    """
    Interage com a seção "Interactions" do DemoQA.

    Args:
        driver (webdriver.Chrome): Instância do WebDriver do Chrome.
    """
    try:
        logger.info('Interagindo com a seção Interactions')
        driver.get('https://demoqa.com/interaction')
        time.sleep(2)

        # Clicar no item "Sortable" no menu à esquerda
        sortable_menu_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Sortable"]'))
        )
        sortable_menu_item.click()
        time.sleep(2)
        
        # Selecionar a aba "List"
        list_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'demo-tab-list'))
        )
        list_tab.click()
        time.sleep(2)

        # Pegar os elementos da lista
        items = driver.find_elements(By.XPATH, '//div[@id="demo-tabpane-list"]//div[@class="list-group-item list-group-item-action"]')
        
        # Criar uma instância de ActionChains
        actions = ActionChains(driver)

        # Realizar a ação de arrastar e soltar
        actions.click_and_hold(items[0]).move_to_element(items[2]).release().perform()
        time.sleep(2)
        actions.click_and_hold(items[1]).move_to_element(items[4]).release().perform()
        time.sleep(2)
        actions.click_and_hold(items[2]).move_to_element(items[5]).release().perform()
        time.sleep(2)

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
