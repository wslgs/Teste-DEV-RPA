# Projeto de Testes para AeC

Este repositório contém dois projetos de robôs de automação desenvolvidos em Python: um robô web para realizar interações e coletar dados no site DemoQA e um robô desktop para configurar alarmes no aplicativo Relógio do Windows.

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

Este projeto é um robô de automação desktop desenvolvido para configurar alarmes no aplicativo Relógio do Windows. O robô automatiza a abertura do aplicativo, a criação de alarmes específicos e a configuração de várias opções, como hora, repetição e soneca. Além disso, o robô registra os alarmes criados e agenda tarefas no Windows para registrar a execução dos alarmes.

### Funcionalidades

- Abre o aplicativo Relógio do Windows.
- Acessa a aba "Alarme".
- Adiciona novos alarmes com configurações específicas.
- Registra os alarmes criados em um arquivo histórico.
- Agenda tarefas no Windows para registrar a execução dos alarmes.

### Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
robo_desktop/
├── logs/
│   └── alarms_log.log         # Arquivo de log gerado pelo robô
│
├── reports/
│   └── (vazio)                # Diretório reservado para relatórios futuros
│
├── alarm.py                   # Script principal de automação desktop
├── register_alarm.py          # Script para registrar a execução do alarme
└── requirements.txt           # Arquivo de dependências do projeto
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

1. **Configuração de Logs e Diretórios:**
   - Configura diretórios para logs e relatórios.
   - Cria handlers para registrar logs em arquivo e no console.

2. **Criação do Diretório e Arquivo Histórico:**
   - Verifica se o diretório `histórico_robô` e o arquivo `historico.txt` existem. Se não existirem, cria-os.
   - O arquivo `historico.txt` armazena a data e hora de execução dos alarmes.

3. **Abertura do Aplicativo Relógio do Windows:**
   - Utiliza o comando `subprocess.Popen` para abrir o aplicativo Relógio.

4. **Conexão à Janela do Relógio:**
   - Utiliza a biblioteca `pywinauto` para conectar-se à janela do Relógio e garantir que a aba "Alarme" está acessível.

5. **Adição de Novos Alarmes:**
   - Configura a hora, minutos, nome do alarme, repetição, som do alarme e soneca.
   - Navega pelas opções do alarme usando comandos de teclado (`send_keys`).

6. **Criação de Tarefas Agendadas:**
   - Utiliza o comando `schtasks` para criar tarefas agendadas no Windows, que executam o script `register_alarm.py` nos horários dos alarmes configurados.
   - Para alarmes repetitivos, a tarefa é agendada semanalmente para os dias selecionados.
   - Para alarmes não repetitivos, a tarefa é agendada uma única vez.

7. **Registro de Alarmes Criados:**
   - Registra a data e hora dos alarmes criados no arquivo `historico.txt`.

8. **Fechamento do Aplicativo Relógio do Windows:**
   - Fecha o aplicativo Relógio após a configuração dos alarmes.

### Versão do Windows

Este projeto foi testado no Windows 11 Home 64 bits, versão 22631.