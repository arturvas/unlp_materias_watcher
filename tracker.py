import os
import re
import sys
import time
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GUARANI_USER = os.getenv('GUARANI_USER')
GUARANI_PASS = os.getenv('GUARANI_PASS')

LOGIN_URL = 'https://autogestion.guarani.unlp.edu.ar/acceso'
MATERIA_URL = 'https://autogestion.guarani.unlp.edu.ar/cursada/elegir_materia/99f9b40a17f916863c3d2cd80e3760a07cef9b44'

def notificar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensagem}
    try:
        res = requests.post(url, data=payload)
        if res.status_code != 200:
            print(f"Erro no Telegram. Código: {res.status_code}")
    except Exception as e:
        print(f"Falha de conexão com Telegram: {e}")

def realizar_login(session):
    print("Realizando login no SIU Guaraní...")
    res = session.get(LOGIN_URL) 
    soup = BeautifulSoup(res.text, 'html.parser')
    
    csrf_input = soup.find('input', {'name': '__csrf'})
    csrf_token = csrf_input['value'] if csrf_input else ''

    payload_login = {
        'usuario': GUARANI_USER, 
        'password': GUARANI_PASS,
        'login': 'Ingresar',
        '__csrf': csrf_token
    }

    url_post_login = "https://autogestion.guarani.unlp.edu.ar/acceso?auth=form"
    res_login = session.post(url_post_login, data=payload_login)
    
    if "Inscripción a materias" not in res_login.text and "acceso" in res_login.url:
        print("Falha no login. Verifique o .env")
        return False
        
    print("Login realizado com sucesso!")
    return True

def buscar_vagas(session, tentativa):
    print("-" * 40)
    print(f"TENTATIVA {tentativa} | Verificando vagas...")

    res_materia = session.get(MATERIA_URL)
    
    if "acceso" in res_materia.url:
        print("[AVISO] Sessao expirada! Tentando relogar...")
        if realizar_login(session):
            res_materia = session.get(MATERIA_URL)
        else:
            return 

    html_dinamico = ""
    matches = re.finditer(r'kernel\.renderer\.on_arrival\((.*?)\);', res_materia.text, re.DOTALL)
    for match in matches:
        try:
            dados = json.loads(match.group(1))
            if dados.get("info", {}).get("id") == "info_materia":
                html_dinamico = dados.get("content", "")
                break
        except json.JSONDecodeError:
            continue

    if not html_dinamico:
        print("[ERRO] Nao foi possivel encontrar o HTML das comissoes no codigo-fonte.")
        return

    soup_materia = BeautifulSoup(html_dinamico, 'html.parser')
    comisiones = soup_materia.find_all('li', class_='comision')
    encontrou_vaga = False

    for comision in comisiones:
        titulo_tag = comision.find('h4')
        nome_comision = titulo_tag.text.strip() if titulo_tag else "Comissao sem titulo"
        
        catedra_valida = False
        divs_span3 = comision.find_all('div', class_='span3')
        
        for span3 in divs_span3:
            if "Cátedra" in span3.text:
                span9_valor = span3.find_next_sibling('div', class_='span9')
                if span9_valor and span9_valor.text.strip() in ['B', 'C']:
                    catedra_valida = True
                break 
        
        if not catedra_valida:
            continue
        
        divs_span9 = comision.find_all('div', class_='span9')
        for div in divs_span9:
            texto = div.text.strip()
            
            if '| Inscriptos:' in texto:
                partes = texto.split('| Inscriptos:')
                try:
                    cupo_total = int(partes[0].strip())
                    inscritos = int(partes[1].strip())

                    # MODO TESTE: forcando uma vaga
                    # inscritos = inscritos - 1
                    # -----------------------------
                    
                    print(f"[{nome_comision}] Cupo: {cupo_total} | Inscritos: {inscritos}")
                    
                    if inscritos < cupo_total:
                        vagas_livres = cupo_total - inscritos
                        msg = f"[ALERTA: VAGA ABERTA]\n{nome_comision}\nLIVRES: {vagas_livres}\nURL: {MATERIA_URL}"
                        notificar_telegram(msg)
                        encontrou_vaga = True
                        print("!!! VAGA ENCONTRADA !!!")
                except ValueError:
                    pass

    if not encontrou_vaga:
        print("Nenhuma vaga livre nas Catedras B e C no momento.")

def timer_to_retry(seconds):
    print(f"Aguardando {seconds} segundos...", end="")
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\rAguardando {i} segundos para a próxima tentativa... ")
        sys.stdout.flush()
        time.sleep(1)
    print("\r" + " " * 50 + "\r", end="")

if __name__ == "__main__":
    TEMPO_ESPERA = 5
    
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GUARANI_USER, GUARANI_PASS]):
        print("Erro: Faltam variáveis no .env")
    else:
        print("Iniciando rastreador da UNLP...")
        notificar_telegram(f"Rastreador iniciado! Monitorando vagas a cada {TEMPO_ESPERA} segundos...")
        
        sessao_requests = requests.Session()
        sessao_requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        realizar_login(sessao_requests)
        contador_tentativas = 1
        
        while True:
            try:
                buscar_vagas(sessao_requests, contador_tentativas)
            except Exception as e:
                print(f"Erro inesperado: {e}")
            
            contador_tentativas += 1
            
            timer_to_retry(TEMPO_ESPERA)