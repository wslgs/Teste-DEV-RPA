# Projeto de Testes para AeC

Este repositório contém dois projetos de robôs de automação desenvolvidos em Python: um robô web para coletar dados de livros no site DemoQA e um robô desktop para configurar alarmes no aplicativo Relógio do Windows.

---

## Projeto Robô Web

### Descrição do Projeto

Este projeto consiste em um robô web desenvolvido em Python que realiza a automação de tarefas no site DemoQA. O robô é responsável por coletar dados de livros da seção "Book Store Application" e salvar esses dados em um banco de dados SQL Server. Além disso, o projeto inclui scripts para a criação do banco de dados e das tabelas necessárias.

### Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
robo_web/
│
├── data/
│   └── books.csv           # Arquivo CSV gerado contendo os dados dos livros
│
├── logs/
│   └── rpa_log.log         # Arquivo de log gerado pelo robô
│
├── reports/
│   └── (vazio)             # Diretório reservado para relatórios futuros
│
├── scripts/
│   └── database.py         # Script para criação do banco de dados e tabelas
│
├── src/
│   └── web_automation.py   # Script principal de automação web
│
├── chromedriver.exe        # Executável do ChromeDriver
├── requirements.txt        # Arquivo de dependências do projeto
└── .env                    # Arquivo de configuração com variáveis de ambiente
```

### Instalação

#### Pré-requisitos

- Python 3.x instalado
- Google Chrome instalado
- ChromeDriver compatível com a versão do Google Chrome

#### Passos para Instalação

1. Clone este repositório para o seu ambiente local:

    ```bash
    git clone https://github.com/wslgs/Teste-DEV-RPA.git
    cd robo_web
    ```

2. Instale as dependências do projeto usando o `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure as variáveis de ambiente no arquivo `.env`:

    ```text
    # .env
    # Configurações de conexão com o banco de dados SQL Server
    SQL_SERVER=localhost
    SQL_DATABASE=master
    SQL_USERNAME=sa
    SQL_PASSWORD=Sagem22CoM

    # Caminho para o ChromeDriver
    CHROME_DRIVER_PATH=C:\Users\Weslley Gomes\Desktop\TESTE AEC\robo_web\chromedriver.exe

    # Credenciais de login para o site DemoQA
    DEMOQA_USERNAME=wslgs
    DEMOQA_PASSWORD=Sagem22CoM!
    ```

### Utilização

#### 1. Criação do Banco de Dados e Tabela

Execute o script `database.py` para criar o banco de dados `DemoQA` e a tabela `Books`:

```bash
python scripts/database.py
```

#### 2. Execução da Automação Web

Execute o script `web_automation.py` para realizar a automação no site DemoQA e coletar os dados dos livros:

```bash
python src/web_automation.py
```

### Arquivos Gerados

- `logs/rpa_log.log`: Arquivo de log contendo informações detalhadas sobre a execução do robô.
- `data/books.csv`: Arquivo CSV contendo os dados dos livros coletados.

### Scripts

#### `scripts/database.py`

Este script é responsável pela criação do banco de dados `DemoQA` e da tabela `Books`. Ele conecta ao banco de dados SQL Server utilizando as configurações definidas no arquivo `.env` e executa os comandos SQL necessários.

#### `src/web_automation.py`

Este script é o principal responsável pela automação web. Ele realiza as seguintes tarefas:

1. Faz login no site DemoQA.
2. Interage com diversas seções do site (Elements, Forms, Alerts, Frames & Windows, Widgets, Interactions).
3. Coleta dados dos livros na seção "Book Store Application".
4. Salva os dados coletados no banco de dados SQL Server.
5. Exporta os dados coletados para um arquivo CSV.

### Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:

- `pandas`
- `selenium`
- `pyodbc`
- `python-dotenv`

Para instalar todas as dependências, execute:

```bash
pip install -r requirements.txt
```

---

## Projeto Robô Desktop para Configuração de Alarme no Windows

### Descrição

Este projeto é um robô de automação desktop desenvolvido para configurar alarmes no aplicativo Relógio do Windows. O robô automatiza a abertura do aplicativo, a criação de alarmes específicos e a configuração de várias opções, como hora, repetição e soneca.

### Funcionalidades

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

### Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
robo_desktop/
├── alarm.py                # Script principal de automação desktop
└── requirements.txt        # Arquivo de dependências do projeto
```

### Instalação

#### Pré-requisitos

- Python 3.x
- pip (gerenciador de pacotes do Python)

#### Passos para Instalação

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

### Uso

1. Execute o script de automação:

   ```bash
   python alarm.py
   ```

2. O robô abrirá o aplicativo Relógio do Windows e configurará os alarmes automaticamente.

### Estrutura do Código

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

### Versão do Windows

Este projeto foi testado no Windows 11 Home 64 bits, versão 22631.