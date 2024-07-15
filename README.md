# Projeto de Testes para AeC

Este repositório contém dois projetos de robôs de automação desenvolvidos em Python: um robô web para realizar interações e coletar dados no site DemoQA e um robô desktop para configurar alarmes no aplicativo Relógio do Windows.

---

## Apresentação

Olá, meu nome é Weslley Gomes Dantas, tenho 26 anos e sou Desenvolvedor e DevOps. Este projeto foi desenvolvido como parte de um teste prático para a AeC, com o objetivo de avaliar minhas habilidades em desenvolvimento de robôs para automação web e desktop. O teste é composto por duas etapas, conforme descrito abaixo:

1. Criação de um robô web que acessa o site DemoQA, realiza interações específicas e salva dados em um banco de dados SQL.
2. Criação de um robô desktop que configura alarmes no aplicativo Relógio do Windows.

## Projeto Robô Web

### Descrição do Projeto

O robô web foi desenvolvido para acessar o site [DemoQA](https://demoqa.com/), realizar interações em diversas seções e coletar dados de livros na seção "Book Store Application". Esses dados são salvos em um banco de dados SQL Server e exportados para um arquivo CSV.

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
- Pip
- Google Chrome instalado
- ChromeDriver compatível com a versão do Google Chrome
- SQL Server 2022

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

1. **Inicializa o WebDriver do Chrome:** Configura o ChromeDriver e inicializa uma instância do WebDriver do Chrome.

2. **Realiza o login no site DemoQA:**
   - Navega até a página de login.
   - Preenche os campos de login com as credenciais fornecidas no arquivo `.env`.
   - Clica no botão de login e espera até que a URL contenha 'profile', indicando sucesso no login.

3. **Interage com várias seções do site DemoQA:**
   - **Elements:** Preenche e envia o formulário na seção "Text Box".
   - **Forms:** Preenche e envia o formulário na seção "Practice Form", incluindo a seleção de gênero, hobbies, e a escolha de estado e cidade.
   - **Alerts, Frames & Windows:** Navega até "Browser Windows", abre uma nova aba e depois a fecha.
   - **Widgets:** Navega até "Accordian", fecha a seção "What is Lorem Ipsum?" que já está aberta, e então expande e fecha as seções "Where does it come from?" e "Why do we use it?".
   - **Interactions:** Navega até "Sortable", seleciona a aba "List" e rearranja os itens na lista usando a funcionalidade de arrastar e soltar do Selenium.

4. **Coleta dados dos livros na seção "Book Store Application":**
   - Navega até a página de livros.
   - Coleta informações sobre cada livro disponível (imagem, título, autor, editora).
   - Continua coletando dados até que todas as páginas de livros tenham sido processadas.

5. **Salva os dados coletados no banco de dados SQL Server:**
   - Conecta ao banco de dados utilizando as configurações fornecidas no arquivo `.env`.
   - Insere os dados dos livros na tabela `Books`.

6. **Exporta os dados coletados para um arquivo CSV:**
   - Cria um DataFrame com os dados coletados e salva no arquivo `data/books.csv`.

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

### Logging e Relatórios de Erro

- **Logging:** O script registra informações detalhadas sobre a execução em um arquivo de log localizado em `logs/rpa_log.log`.
- **Relatórios de Erro:** Em caso de erros, as mensagens de erro são acumuladas e salvas em um arquivo de relatório na pasta `reports`.

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
   - Verifica se o diretório `histórico_robô` e o arquivo `historico.txt` existem

. Se não existirem, cria-os.
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

### Vídeos Demonstrativos

No repositório, há dois vídeos que apresentam o funcionamento dos dois robôs:

1. **Robô Web:**
   - Demonstra as interações nas páginas do site DemoQA, mostrando a funcionalidade de coleta de dados dos livros e outras interações realizadas.
   - O vídeo segue os passos descritos na seção "Utilização" e apresenta o resultado final.

2. **Robô Desktop:**
   - Demonstra a configuração de dois alarmes de teste no aplicativo Relógio do Windows.
   - O vídeo segue os passos descritos na seção "Uso" e mostra a funcionalidade de salvar e registrar os alarmes configurados.