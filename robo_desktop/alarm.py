import subprocess
import time
import logging
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(asctime)s - %(message)s')

# Função para abrir o relógio do Windows
def open_clock():
    logging.info("Abrindo o aplicativo de Relógio do Windows...")
    subprocess.Popen(['start', 'ms-clock:'], shell=True)
    time.sleep(5)  # Esperar alguns segundos para garantir que o aplicativo abriu

# Abrir o aplicativo de Relógio do Windows
open_clock()

# Listar todas as janelas para verificar o título correto
logging.info("Listando janelas abertas para verificar o título correto...")
windows = Desktop(backend="uia").windows()
for win in windows:
    logging.info(f"Janela encontrada: {win.window_text()}")

# Tente conectar ao aplicativo de Relógio do Windows
try:
    logging.info("Conectando ao aplicativo de Relógio do Windows...")
    app = Application(backend="uia").connect(title_re="Relógio")
    clock = app.window(title_re="Relógio")
    logging.info("Conexão estabelecida com sucesso.")
except Exception as e:
    logging.error(f"Erro ao conectar ao aplicativo de Relógio do Windows: {e}")
    exit()

# Acessar a aba "Alarme" na esquerda
try:
    logging.info("Acessando a aba Alarme...")
    alarm_tab = clock.child_window(title="Alarme", control_type="ListItem")
    alarm_tab.wait('visible', timeout=10).select()
    logging.info("Aba Alarme acessada com sucesso.")
except Exception as e:
    logging.error(f"Erro ao acessar a aba Alarme: {e}")
    exit()

# Criar o primeiro alarme clicando no botão "+"
try:
    logging.info("Clicando no botão + para adicionar um novo alarme...")
    add_alarm_button = clock.child_window(title="Adicionar um alarme", control_type="Button")
    add_alarm_button.wait('visible', timeout=10).click()
    time.sleep(2)  # Adicionar um delay para garantir que a janela está pronta
    
    logging.info("Configurando o novo alarme...")
    
    # Configurar a hora e minutos do alarme usando teclado
    logging.info("Inserindo hora e minutos...")
    send_keys("{UP}")
    send_keys("{TAB}")
    time.sleep(1)
    
    # Adicionar mais um tab para focar no campo do nome do alarme
    send_keys("{TAB}")
    
    # Configurar o nome do alarme
    logging.info("Configurando o nome do alarme...")
    send_keys("Tenha{SPACE}um{SPACE}excelente{SPACE}dia{SPACE}de{SPACE}trabalho!")
    time.sleep(1)
    
    # Verificar se a próxima seção é "Repetir alarme"
    logging.info("Verificando a próxima seção...")
    send_keys("{TAB}")
    send_keys("{TAB}")
    
    # Configurar os dias da semana
    logging.info("Configurando os dias da semana...")
    for _ in range(1, 8):  # Navegar pelos dias de Domingo a Sábado
        if _ in [2, 3, 4, 5, 6]:  # Ativar os dias de Segunda a Sexta
            send_keys("{SPACE}")
        send_keys("{RIGHT}")
        time.sleep(0.5)
    
    # Configurar soneca
    logging.info("Configurando a soneca...")
    send_keys("{TAB}{TAB}")
    send_keys("{UP}")

    # Salvar o alarme
    send_keys("{TAB}")
    send_keys("{SPACE}")
    time.sleep(2)
    
    logging.info("Primeiro alarme criado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao criar o primeiro alarme: {e}")
    exit()
