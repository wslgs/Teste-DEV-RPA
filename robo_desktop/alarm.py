import subprocess
import time
import logging
import os
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys
from datetime import datetime

# Configurar diretórios de logs e reports
log_directory = 'logs'
reports_directory = 'reports'

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

if not os.path.exists(reports_directory):
    os.makedirs(reports_directory)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Verificar se os handlers já estão configurados para evitar duplicação
if not logger.hasHandlers():
    # Adicionar handlers para o logger
    file_handler = logging.FileHandler(os.path.join(log_directory, 'alarms_log.log'))
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levellevel)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

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
        report_filename = os.path.join(reports_directory, f'report_{timestamp}.report')
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

# Arrays para as opções de alarme e soneca
alarm_sounds = ["Alarms", "Xilofone", "Acordes", "Toque", "Jingle", "Transição", "Decrescente", "Quique", "Eco"]
snooze_times = ["Desativado", "5 minutos", "10 minutos", "20 minutos", "30 minutos", "1 hora"]

# Função para abrir o relógio do Windows
def open_clock():
    try:
        logger.info("Abrindo o aplicativo de Relógio do Windows...")
        subprocess.Popen(['start', 'ms-clock:'], shell=True)
        time.sleep(5)  # Esperar alguns segundos para garantir que o aplicativo abriu
    except Exception as e:
        error_message = f"Erro ao abrir o aplicativo de Relógio do Windows: {e}"
        logger.error(error_message)
        add_error_report(error_message)

# Abrir o aplicativo de Relógio do Windows
open_clock()

# Listar todas as janelas para verificar o título correto
try:
    logger.info("Listando janelas abertas para verificar o título correto...")
    windows = Desktop(backend="uia").windows()
    for win in windows:
        logger.info(f"Janela encontrada: {win.window_text()}")
except Exception as e:
    error_message = f"Erro ao listar janelas abertas: {e}"
    logger.error(error_message)
    add_error_report(error_message)

# Tente conectar ao aplicativo de Relógio do Windows
try:
    logger.info("Conectando ao aplicativo de Relógio do Windows...")
    app = Application(backend="uia").connect(title_re="Relógio")
    clock = app.window(title_re="Relógio")
    logger.info("Conexão estabelecida com sucesso.")
except Exception as e:
    error_message = f"Erro ao conectar ao aplicativo de Relógio do Windows: {e}"
    logger.error(error_message)
    add_error_report(error_message)
    save_error_report()
    exit()

# Acessar a aba "Alarme" na esquerda
try:
    logger.info("Acessando a aba Alarme...")
    alarm_tab = clock.child_window(title="Alarme", control_type="ListItem")
    alarm_tab.wait('visible', timeout=10).select()
    logger.info("Aba Alarme acessada com sucesso.")
except Exception as e:
    error_message = f"Erro ao acessar a aba Alarme: {e}"
    logger.error(error_message)
    add_error_report(error_message)
    save_error_report()
    exit()

def criar_alarme(hora, minuto, nome, dias, soneca, repetir=True, campainha=None):
    try:
        logger.info("Clicando no botão + para adicionar um novo alarme...")
        add_alarm_button = clock.child_window(title="Adicionar um alarme", control_type="Button")
        add_alarm_button.wait('visible', timeout=10).click()
        time.sleep(2)  # Adicionar um delay para garantir que a janela está pronta
        
        logger.info("Configurando o novo alarme...")
        
        # Configurar a hora e minutos do alarme usando teclado
        logger.info("Inserindo hora e minutos...")
        for digit in f"{hora:02d}":
            send_keys(f"{{VK_NUMPAD{digit}}}")
        send_keys("{TAB}")
        for digit in f"{minuto:02d}":
            send_keys(f"{{VK_NUMPAD{digit}}}")
        send_keys("{TAB}")
        time.sleep(1)
        
        # Configurar o nome do alarme
        logger.info("Configurando o nome do alarme...")
        send_keys(f"{nome.replace(' ', '{SPACE}')}")
        time.sleep(1)
        
        # Verificar se a próxima seção é "Repetir alarme"
        logger.info("Verificando a próxima seção...")
        send_keys("{TAB}")
        if repetir:
            send_keys("{SPACE}")
        send_keys("{TAB}")
        
        # Configurar os dias da semana
        logger.info("Configurando os dias da semana...")
        for dia in range(1, 8):  # Navegar pelos dias de Domingo a Sábado
            if dia in dias:
                send_keys("{SPACE}")
            send_keys("{RIGHT}")
            time.sleep(0.5)
        
        # Configurar o som do alarme
        if campainha:
            logger.info("Configurando o som do alarme...")
            send_keys("{TAB}")
            index = alarm_sounds.index(campainha)
            for _ in range(index):
                send_keys("{DOWN}")
            send_keys("{TAB}")
        else:
            send_keys("{TAB}")
            send_keys("{TAB}")

        # Configurar soneca
        logger.info("Configurando a soneca...")
        current_index = snooze_times.index("10 minutos")
        desired_index = snooze_times.index(soneca)
        steps = desired_index - current_index
        if steps > 0:
            for _ in range(steps):
                send_keys("{DOWN}")
        elif steps < 0:
            for _ in range(-steps):
                send_keys("{UP}")
        send_keys("{TAB}")
        
        # Salvar o alarme
        logger.info("Salvando o alarme...")
        send_keys("{SPACE}")
        time.sleep(2)
        
        logger.info("Alarme criado com sucesso.")
    except Exception as e:
        error_message = f"Erro ao criar o alarme: {e}"
        logger.error(error_message)
        add_error_report(error_message)

# Criar o primeiro alarme
criar_alarme(hora=8, minuto=0, nome="Tenha um excelente dia de trabalho!", dias=[2, 3, 4, 5, 6], soneca="5 minutos")

# Criar o segundo alarme
criar_alarme(hora=7, minuto=45, nome="Curtir o final de semana", dias=[1, 7], soneca="30 minutos", repetir=True, campainha="Jingle")

# Salvar relatório de erros, se houver
save_error_report()
