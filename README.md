# Robo Desktop para Configuração de Alarme no Windows

## Descrição

Este projeto é um robô de automação desktop desenvolvido para configurar alarmes no aplicativo Relógio do Windows. O robô automatiza a abertura do aplicativo, a criação de alarmes específicos e a configuração de várias opções, como hora, repetição e soneca.

## Funcionalidades

- Abre o aplicativo Relógio do Windows.
- Acessa a aba "Alarme".
- Adiciona novos alarmes com as seguintes configurações:
  - **Primeiro Alarme:**
    - Hora: 08:00
    - Nome do Alarme: "Tenha um excelente dia de trabalho!"
    - Repetição: Segunda a Sexta-feira
    - Soneca: 5 minutos
  - **Segundo Alarme:**
    - Hora: 07:45
    - Nome do Alarme: "Curtir o final de semana"
    - Repetição: Sábado e Domingo
    - Soneca: 30 minutos
    - Campainha: Jingle

## Pré-requisitos

- Python 3.x
- pip (gerenciador de pacotes do Python)

## Instalação

1. Clone o repositório para sua máquina local:
   ```bash
   git clone https://github.com/wslgs/Teste-DEV-RPA.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd robo_desktop
   ```

3. Instale as dependências necessárias usando o arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Execute o script de automação:
   ```bash
   python alarm.py
   ```

2. O robô abrirá o aplicativo Relógio do Windows e configurará os alarmes automaticamente.

## Estrutura do Código

O script `alarm.py` realiza as seguintes etapas principais:

1. Abre o aplicativo Relógio do Windows.
2. Conecta-se à janela do Relógio.
3. Navega até a aba "Alarme".
4. Adiciona um novo alarme clicando no botão "+".
5. Configura a hora, minutos, nome do alarme, repetição, som do alarme e soneca.
6. Salva o alarme configurado.

### Trechos de Código Importantes

- **Abertura do aplicativo de Relógio do Windows:**
  ```python
  subprocess.Popen(['start', 'ms-clock:'], shell=True)
  ```

- **Conexão à janela do Relógio:**
  ```python
  app = Application(backend="uia").connect(title_re="Relógio")
  clock = app.window(title_re="Relógio")
  ```

- **Configuração da hora e minutos do alarme:**
  ```python
  for digit in f"{hora:02d}":
      send_keys(f"{{VK_NUMPAD{digit}}}")
  send_keys("{TAB}")
  for digit in f"{minuto:02d}":
      send_keys(f"{{VK_NUMPAD{digit}}}")
  send_keys("{TAB}")
  ```

- **Configuração do nome do alarme:**
  ```python
  send_keys(f"{nome.replace(' ', '{SPACE}')}")
  ```

- **Navegação e configuração dos dias da semana:**
  ```python
  for dia in range(1, 8):
      if dia in dias:
          send_keys("{SPACE}")
      send_keys("{RIGHT}")
  ```

- **Configuração do som do alarme:**
  ```python
  if campainha:
      send_keys("{TAB}")
      index = alarm_sounds.index(campainha)
      for _ in range(index):
          send_keys("{DOWN}")
      send_keys("{TAB}")
  else:
      send_keys("{TAB}")
  ```

- **Configuração da soneca:**
  ```python
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
  ```

## Versão do Windows

Este projeto foi testado no Windows 11 Home 64 bits, versão 22631.