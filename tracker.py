import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# --- CONFIGURAÇÕES ---
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

GUARANI_USER = os.getenv('GUARANI_USER')
GUARANI_PASS = os.getenv('GUARANI_PASS')

# URLs do SIU Guaraní
LOGIN_URL = 'https://autogestion.guarani.unlp.edu.ar/acceso'
MATERIA_URL = 'https://autogestion.guarani.unlp.edu.ar/cursada/elegir_materia/99f9b40a17f916863c3d2cd80e3760a07cef9b44'

def notificar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensagem}
    try:
        requests.post(url, data=payload)
        print(f"Notificação enviada: {mensagem}")
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")

def buscar_vagas():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    print("1. Acessando página de login...")
    res = session.get(LOGIN_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Extrai o token CSRF dinamicamente do form de login
    csrf_input = soup.find('input', {'name': '__csrf'})
    csrf_token = csrf_input['value'] if csrf_input else ''

    # payload de login (IMPORTANTE: confirme os nomes desses campos no HTML da tela de login)
    payload_login = {
        'usuario': GUARANI_USER, 
        'clave': GUARANI_PASS,
        '__csrf': csrf_token
    }

    print("2. Fazendo login...")
    res_login = session.post(LOGIN_URL, data=payload_login)
    
    if "Inscripción a materias" not in res_login.text and "acceso" in res_login.url:
        print("Falha no login. Verifique as credenciais ou os nomes dos campos do formulário.")
        return

    print("3. Acessando a página de Anatomia...")
    res_materia = session.get(MATERIA_URL)
    soup_materia = BeautifulSoup(res_materia.text, 'html.parser')

    comisiones = soup_materia.find_all('li', class_='comision')
    encontrou_vaga = False

    for comision in comisiones:
        titulo_tag = comision.find('h4')
        if not titulo_tag:
            continue
        
        nome_comision = titulo_tag.text.strip()
        
        divs_span9 = comision.find_all('div', class_='span9')
        for div in divs_span9:
            texto = div.text.strip()
            if '| Inscriptos:' in texto:
                partes = texto.split('| Inscriptos:')
                try:
                    cupo_total = int(partes[0].strip())
                    inscritos = int(partes[1].strip())
                    
                    if inscritos < cupo_total:
                        vagas_livres = cupo_total - inscritos
                        msg = f"🚨 VAGA ABERTA NA UNLP! 🚨\n{nome_comision}\nVagas Livres: {vagas_livres}\nCorre: {MATERIA_URL}"
                        notificar_telegram(msg)
                        encontrou_vaga = True
                except ValueError:
                    print("Erro ao converter números do cupo.")

    if not encontrou_vaga:
        print("Nenhuma vaga aberta no momento.")

if __name__ == "__main__":
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GUARANI_USER, GUARANI_PASS]):
        print("Erro: Verifique se o arquivo .env está configurado corretamente com todas as variáveis.")
    else:
        print("Iniciando rastreador da UNLP...")
        while True:
            try:
                buscar_vagas()
            except Exception as e:
                print(f"Erro inesperado: {e}")
            
            print("Aguardando 5 minutos para a próxima checagem...")
            time.sleep(300)