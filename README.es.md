# SIU Guaraní Tracker - UNLP

[Português](README.md) | [English](README.en.md)

Un script de automatización desarrollado en Python para monitorear la disponibilidad de cupos en materias del sistema SIU Guaraní de la Universidad Nacional de La Plata (UNLP).

El proyecto fue creado originalmente para rastrear la apertura de cupos en la concurrida materia de Anatomía (Cátedras B y C) y envía notificaciones en tiempo real a través de un bot de Telegram tan pronto como el número de inscritos sea menor que la capacidad de la comisión.

## Funcionalidades

* **Sesión Persistente:** Realiza el inicio de sesión una única vez y mantiene los cookies de sesión activos, evitando la sobrecarga en el servidor de la facultad.
* **Extracción de HTML Dinámico:** Supera la limitación de Toba/Guaraní, que encapsula el HTML de respuesta dentro de funciones JavaScript, utilizando Expresiones Regulares para extraer y procesar los datos.
* **Notificaciones en Tiempo Real:** Integración sencilla con la API de Telegram para el envío inmediato del enlace de inscripción cuando se encuentra una vacante.

## Requisitos Previos

* Python 3.x instalado.
* Un bot configurado en Telegram (obtén el Token vía BotFather y tu Chat ID).
* Credenciales activas en el SIU Guaraní de la UNLP.

## Instalación

1. Clona este repositorio en tu máquina local:
```bash
git clone https://github.com/arturvas/unlp_materias_watcher.git
cd unlp_materias_watcher
```

2. Configura el entorno virtual:
```bash
python3 -m venv venv
```

3. Dependiendo de tu sistema operativo, ejecuta:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1
```

4. Instala los requerimientos:
```bash
pip install -r requirements.txt
```

## Configuración

En la raíz del proyecto, haz una copia del archivo de ejemplo de variables de entorno:
```bash
cp .env.example .env
```

Abre el archivo `.env` recién creado y completa tu información:
```bash
TELEGRAM_BOT_TOKEN: El token proporcionado por BotFather.
TELEGRAM_CHAT_ID: El ID de tu conversación con el bot.
GUARANI_USER: Tu usuario de acceso.
GUARANI_PASS: Tu contraseña del sitio Guaraní UNLP.
```

## Modo de Uso

```bash
python3 tracker.py
```

La terminal mostrará una cuenta regresiva y el estado actual de las comisiones monitoreadas. Para detener el script, presiona `Ctrl + C` en la terminal.
