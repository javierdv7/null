import platform
import subprocess
import os




def lanzar_terminal_fullscreen():
    sistema = platform.system()
    ruta_script = os.path.abspath("none")

    try:
        if sistema == "Windows":
            subprocess.Popen([
                "powershell",
                "-WindowStyle", "Maximized",
                "-Command",
                f'Start-Process python -ArgumentList "{ruta_script}" -WindowStyle Maximized'
            ])

        elif sistema == "Darwin":  # macOS
            subprocess.Popen([
                "osascript", "-e",
                'tell application "Terminal" to activate',
                "-e",
                f'tell application "Terminal" to do script "python3 \\"{ruta_script}\\""'
            ])

        elif sistema == "Linux":
            subprocess.Popen([
                "gnome-terminal", "--full-screen", "--", "bash", "-c",
                f"python3 '{ruta_script}'; exec bash"
            ])
        else:
            print("[X] Sistema operativo no soportado para terminal fullscreen.")

    except Exception as e:
        print(f"[!] Error lanzando terminal: {e}")

if __name__ == "__main__":
    lanzar_terminal_fullscreen()
