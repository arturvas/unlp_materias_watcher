# SIU Guaraní Tracker - UNLP

Um script de automação desenvolvido em Python para monitorar a disponibilidade de vagas em disciplinas no sistema SIU Guaraní da Universidade Nacional de La Plata (UNLP). 

O projeto foi criado originalmente para rastrear a abertura de vagas na concorrida matéria de Anatomia (Cátedras B e C) e envia notificações em tempo real através de um bot do Telegram assim que o número de inscritos for menor que a capacidade da turma.

## Funcionalidades

* **Sessão Persistente:** Realiza o login uma única vez e mantém os cookies de sessão vivos, evitando sobrecarga no servidor da faculdade.
* **Extração de HTML Dinâmico:** Contorna a limitação do Toba/Guaraní, que encapsula o HTML de resposta dentro de funções JavaScript, usando Expressões Regulares para extrair e fazer o parse dos dados.
* **Notificações em Tempo Real:** Integração simples com a API do Telegram para envio imediato do link de inscrição quando uma vaga é encontrada.

## Pré-requisitos

* Python 3.x instalado.
* Um bot configurado no Telegram (obtenha o Token via BotFather e o seu Chat ID).
* Credenciais ativas no SIU Guaraní da UNLP.

## Instalação

1. Clone este repositório para a sua máquina local:
```bash
git clone https://github.com/arturvas/unlp_materias_watcher.git

cd unlp_materias_watcher
```

2. Instale as bibliotecas necessárias.

```bash
python3 -m venv venv
```

3. A depender do seus SO, rode:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1
```
4. Depois:
```bash
pip install -r requirements.txt
```


## Configuração
Na raiz do projeto, faça uma cópia do arquivo de exemplo das variáveis de ambiente:

```bash
cp .env.example .env
```

Abra o arquivo .env recém-criado e preencha as suas informações:

```bash
TELEGRAM_BOT_TOKEN: O token fornecido pelo BotFather.

TELEGRAM_CHAT_ID: O ID da sua conversa com o bot.

GUARANI_USER: Seu usuário de acesso.

GUARANI_PASS: Sua senha do site Guaraní UNLP.
```

## Como Usar

```bash
python3 tracker.py
```

O terminal exibirá uma contagem regressiva e o status atual das turmas sendo monitoradas. Para interromper o script, pressione Ctrl + C no terminal.