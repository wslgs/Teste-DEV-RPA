import os
from datetime import datetime

def registrar_alarme():
    usuario = os.getlogin()
    diretorio_historico = f"C:\\Users\\{usuario}\\Documents\\histórico_robô"
    arquivo_historico = os.path.join(diretorio_historico, "historico.txt")

    if not os.path.exists(diretorio_historico):
        os.makedirs(diretorio_historico)

    if not os.path.exists(arquivo_historico):
        with open(arquivo_historico, 'w') as f:
            f.write("Histórico de Execução dos Alarmes\n")

    with open(arquivo_historico, 'a') as f:
        f.write(f"{datetime.now().strftime('%d/%m/%Y - %H:%M')}\n")

if __name__ == "__main__":
    registrar_alarme()
