import time
import sys
import random
import os
import socket
import uuid
import platform
import subprocess
import urllib.request

def spinner_animado(texto="procesando", duracion=3):
    spinner = ['|', '/', '-', '\\']
    sys.stdout.write(texto + " ")
    sys.stdout.flush()
    t0 = time.time()
    i = 0
    while time.time() - t0 < duracion:
        sys.stdout.write(spinner[i % len(spinner)])
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
        i += 1
    print()

def subir_volumen_al_maximo():
    sistema = platform.system()

    try:
        if sistema == "Windows":
            subprocess.run([
                'powershell',
                '-c',
                '(new-object -com wscript.shell).SendKeys([char]175 * 50)'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        elif sistema == "Darwin":
            subprocess.run([
                "osascript", "-e",
                'set volume output volume 100'
            ])

        elif sistema == "Linux":
            subprocess.run([
                "amixer", "sset", "'Master'", "100%"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except Exception as e:
        print(f"[!] No se pudo subir el volumen: {e}")
def reveal_text(masked, target, delay=0.15):
    current = list(masked)
    for i in range(len(target)):
        current[i] = target[i]
        sys.stdout.write('\r' + ''.join(current))
        sys.stdout.flush()
        time.sleep(delay)
    print()

def reproducir_audio_final(nombre_archivo="null"):
    sistema = platform.system()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base_dir, nombre_archivo)

    if not os.path.isfile(ruta):
        print(f"[!] Archivo de audio no encontrado en: {ruta}")
        return

    try:
        if sistema == "Windows":
            subprocess.Popen([
                'powershell',
                '-c',
                f'(New-Object Media.SoundPlayer "{ruta}").PlaySync();'
            ])

        elif sistema == "Darwin":
            subprocess.Popen(["afplay", ruta])

        elif sistema == "Linux":
            subprocess.Popen(["mpg123", ruta])

        else:
            print("[!] Sistema no compatible para reproducir audio.")
    except Exception as e:
        print(f"[!] Error al reproducir audio: {e}")


def lanzar_terminales_fantasma(cantidad=5):
    sistema = platform.system()

    for i in range(cantidad):
        try:
            is_last = i == cantidad - 1

            if sistema == "Windows":
                if is_last:
                    subprocess.Popen([
                        'powershell',
                        '-WindowStyle', 'Maximized',
                        '-Command',
                        'Start-Process cmd -ArgumentList \'/k echo ejecutando ritual...\' -WindowStyle Maximized'
                    ])
                else:
                    subprocess.Popen(
                        'start cmd /c "echo ejecutando ritual... & timeout /t 1 >nul"',
                        shell=True
                    )

            elif sistema == "Darwin":  
                if is_last:
                    subprocess.Popen([
                        "osascript", "-e",
                        'tell application "Terminal" to activate',
                        "-e",
                        'tell application "Terminal" to do script "clear; echo ejecutando ritual...; sleep 5;"'
                    ])
                else:
                    subprocess.Popen([
                        "osascript", "-e",
                        'tell application "Terminal" to do script "echo ejecutando ritual...; sleep 1; exit"'
                    ])

            elif sistema == "Linux":
                if is_last:
                    subprocess.Popen([
                        "gnome-terminal", "--full-screen", "--", "bash", "-c",
                        "clear; echo ejecutando ritual...; sleep 5;"
                    ])
                else:
                    subprocess.Popen([
                        "gnome-terminal", "--", "bash", "-c",
                        "echo ejecutando ritual...; sleep 1;"
                    ])
            else:
                print("Sistema no compatible para terminales.")

        except Exception as e:
            print(f"[!] Error al abrir terminal: {e}")

        time.sleep(random.uniform(0.1, 0.3))



def fake_typing(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_bar(length=30, delay=0.05, breakpoints=[], freeze_at=None):
    for i in range(length + 1):
        bar = '█' * i + '-' * (length - i)
        percent = int((i / length) * 100)

        sys.stdout.write(f"\rCARGANDO: [{bar}] {percent}%")
        sys.stdout.flush()

        if freeze_at is not None and percent >= freeze_at:
            time.sleep(3)
            print("\n[!] Error: ejecución detenida en estado crítico.")
            return

        if percent in breakpoints:
            time.sleep(1.5)
        else:
            time.sleep(delay)
    print()


def show_ascii_banner():
    print("""
 ██░ ██ ▓█████  ██▓     ██▓███      ███▄ ▄███▓▓█████ 
▓██░ ██▒▓█   ▀ ▓██▒    ▓██░  ██▒   ▓██▒▀█▀ ██▒▓█   ▀ 
▒██▀▀██░▒███   ▒██░    ▓██░ ██▓▒   ▓██    ▓██░▒███   
░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██▄█▓▒ ▒   ▒██    ▒██ ▒▓█  ▄ 
░▓█▒░██▓░▒████▒░██████▒▒██▒ ░  ░   ▒██▒   ░██▒░▒████▒
 ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░▒▓▒░ ░  ░   ░ ▒░   ░  ░░░ ▒░ ░
 ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░▒ ░        ░  ░      ░ ░ ░  ░
 ░  ░░ ░   ░     ░ ░   ░░          ░      ░      ░   
 ░  ░  ░   ░  ░    ░  ░                   ░      ░  ░
""")

def obtener_info_sistema():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "desconocida"

    try:
        public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    except:
        public_ip = "desconocida"

    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                        for elements in range(0, 2*6, 8)][::-1])
    except:
        mac = "desconocida"

    return {
        "ip_local": local_ip,
        "ip_publica": public_ip,
        "mac": mac,
        "usuario": os.getenv("USER") or os.getenv("USERNAME"),
        "sistema": platform.system() + " " + platform.release()
    }

def mainplay(seed=13):
    fake_typing("iniciando...")
    time.sleep(0.5)
    
    fake_typing("analizando...")
    time.sleep(2)

    fake_typing("ejecutando secuencia de activación...")
    time.sleep(0.8)
    
    loading_bar(breakpoints=[22, 91], freeze_at=80)

    time.sleep(0.5)
    fake_typing("unknown error: memoria cruzada con canal ???")
    time.sleep(0.3)

    fake_typing("intentando restaurar señal...")
    spinner_animado("↻", duracion=4)


    glitch = random.choice([
        "stack overflow on line 666",
        "entity detected in core.log",
        "!!! unhandled exception: soulTraceFound",
    ])
    fake_typing(glitch)
    time.sleep(0.5)

    show_ascii_banner()
    time.sleep(1)

    fake_typing("cristian ruz no escapará")
    time.sleep(0.5)
    fake_typing("cristian ruz")
    time.sleep(0.5)
    fake_typing("cruz")
    time.sleep(0.5)
    fake_typing("por qué no revisas en su oficina?")
    fake_typing("qué tal debajo de su mesa?")
    fake_typing("o tal vez en su puerta?")
    fake_typing("deberían tener cuidado...")
    fake_typing(":)")
    fake_typing("...")
    time.sleep(1)

    fake_typing("descargando datos del entorno...")
    loading_bar(breakpoints=[22, 91])

    info = obtener_info_sistema()
    print("\n")
    fake_typing(f"ip local: {info['ip_local']}")
    fake_typing(f"ip pública: {info['ip_publica']}")
    fake_typing(f"mac address: {info['mac']}")
    fake_typing(f"usuario: {info['usuario']}")
    fake_typing(f"sistema operativo: {info['sistema']}")
    subir_volumen_al_maximo()
    reproducir_audio_final("null.wav")

    time.sleep(1)
    fake_typing("te conozco :)")

    fake_typing("\n")
    reveal_text("?????????????", "DCCREEPYPASTA")

    time.sleep(0.7)
    fake_typing("\n^C\nKeyboardInterrupt")
    raise Exception("La ejecución no fue interrumpida por el usuario.")


if __name__ == "__main__":
    mainplay()

