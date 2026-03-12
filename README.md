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
   git clone [https://github.com/arturvas/unlp_materias_watcher.git](https://github.com/arturvas/unlp_materias_watcher.git)
   cd unlp_materias_watcher