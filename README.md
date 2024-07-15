# Robo Desktop para Configuração de Alarme no Windows

## Descrição

Este projeto é um robô de automação desktop desenvolvido para configurar alarmes no aplicativo Relógio do Windows. O robô automatiza a abertura do aplicativo, a criação de um alarme específico e a configuração de várias opções, como hora, repetição e soneca.

## Funcionalidades

- Abre o aplicativo Relógio do Windows.
- Acessa a aba "Alarme".
- Adiciona um novo alarme com as seguintes configurações:
  - Hora: 08:00
  - Nome do Alarme: "Tenha um excelente dia de trabalho!"
  - Repetição: Segunda a Sexta-feira
  - Soneca: 5 minutos

## Pré-requisitos

- Python 3.x
- Biblioteca `pywinauto`

## Instalação

1. Clone o repositório para sua máquina local:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd seu-repositorio
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install pywinauto
   ```

## Uso

1. Execute o script de automação:
   ```bash
   python alarm.py
   ```

2. O robô abrirá o aplicativo Relógio do Windows e configurará o alarme automaticamente.

## Estrutura do Código

O script `alarm.py` realiza as seguintes etapas principais:

1. Abre o aplicativo Relógio do Windows.
2. Conecta-se à janela do Relógio.
3. Navega até a aba "Alarme".
4. Adiciona um novo alarme clicando no botão "+".
5. Configura a hora, minutos, nome do alarme, repetição e soneca.
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
  send_keys("{UP}")
  send_keys("{TAB}")
  ```

- **Configuração do nome do alarme:**
  ```python
  send_keys("Tenha{SPACE}um{SPACE}excelente{SPACE}dia{SPACE}de{SPACE}trabalho!")
  ```

- **Navegação e configuração dos dias da semana:**
  ```python
  for _ in range(1, 8):
      if _ in [2, 3, 4, 5, 6]:
          send_keys(" ")
      send_keys("{RIGHT}")
  ```

## Versão do Windows

Este projeto foi testado no Windows 11 Home 64 bits, versão 22631.