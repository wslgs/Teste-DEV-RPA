import subprocess
import time
import logging
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Arrays para as opções de alarme e soneca
alarm_sounds = ["Alarms", "Xilofone", "Acordes", "Toque", "Jingle", "Transição", "Decrescente", "Quique", "Eco"]
snooze_times = ["Desativado", "5 minutos", "10 minutos", "20 minutos", "30 minutos", "1 hora"]

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

def criar_alarme(hora, minuto, nome, dias, soneca, repetir=True, campainha=None):
    try:
        logging.info("Clicando no botão + para adicionar um novo alarme...")
        add_alarm_button = clock.child_window(title="Adicionar um alarme", control_type="Button")
        add_alarm_button.wait('visible', timeout=10).click()
        time.sleep(2)  # Adicionar um delay para garantir que a janela está pronta
        
        logging.info("Configurando o novo alarme...")
        
        # Configurar a hora e minutos do alarme usando teclado
        logging.info("Inserindo hora e minutos...")
        for digit in f"{hora:02d}":
            send_keys(f"{{VK_NUMPAD{digit}}}")
        send_keys("{TAB}")
        for digit in f"{minuto:02d}":
            send_keys(f"{{VK_NUMPAD{digit}}}")
        send_keys("{TAB}")
        time.sleep(1)
        
        # Configurar o nome do alarme
        logging.info("Configurando o nome do alarme...")
        send_keys(f"{nome.replace(' ', '{SPACE}')}")
        time.sleep(1)
        
        # Verificar se a próxima seção é "Repetir alarme"
        logging.info("Verificando a próxima seção...")
        send_keys("{TAB}")
        if repetir:
            send_keys("{SPACE}")
        send_keys("{TAB}")
        
        # Configurar os dias da semana
        logging.info("Configurando os dias da semana...")
        for dia in range(1, 8):  # Navegar pelos dias de Domingo a Sábado
            if dia in dias:
                send_keys("{SPACE}")
            send_keys("{RIGHT}")
            time.sleep(0.5)
        
        # Configurar o som do alarme
        if campainha:
            logging.info("Configurando o som do alarme...")
            send_keys("{TAB}")
            index = alarm_sounds.index(campainha)
            for _ in range(index):
                send_keys("{DOWN}")
            send_keys("{TAB}")
        else:
            send_keys("{TAB}")
            send_keys("{TAB}")

        # Configurar soneca
        logging.info("Configurando a soneca...")
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
        logging.info("Salvando o alarme...")
        send_keys("{SPACE}")
        time.sleep(2)
        
        logging.info("Alarme criado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao criar o alarme: {e}")
        exit()

# Criar o primeiro alarme
criar_alarme(hora=8, minuto=0, nome="Tenha um excelente dia de trabalho!", dias=[2, 3, 4, 5, 6], soneca="5 minutos")

# Criar o segundo alarme
criar_alarme(hora=7, minuto=45, nome="Curtir o final de semana", dias=[1, 7], soneca="30 minutos", repetir=True, campainha="Jingle")
