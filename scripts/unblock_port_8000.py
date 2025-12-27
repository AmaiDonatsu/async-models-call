import psutil
import subprocess

def kill_process_on_port(port: int) -> bool:
    """
    Mata cualquier proceso que esté usando el puerto especificado.
    Usa netstat para mayor confiabilidad en Windows.
    """
    killed_any = False
    current_pid = psutil.Process().pid
    
    try:
        # Usar netstat para encontrar PIDs (más confiable en Windows)
        result = subprocess.run(
            ['netstat', '-ano'], 
            capture_output=True, 
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = int(parts[-1])
                    if pid != current_pid and pid != 0:
                        try:
                            proc = psutil.Process(pid)
                            print(f"✅ Encontrado proceso {proc.name()} (PID: {pid}) en puerto {port}. Terminando...")
                            proc.kill()
                            killed_any = True
                        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            print(f"⚠️ No se pudo matar PID {pid}: {e}")
    except Exception as e:
        print(f"❌ Error buscando procesos: {e}")
    
    # Método alternativo: buscar procesos Python que contengan "server" en sus argumentos
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] != current_pid:
                cmdline = proc.info.get('cmdline') or []
                cmdline_str = ' '.join(cmdline).lower()
                if 'server.py' in cmdline_str or 'uvicorn' in cmdline_str:
                    # Verificar si tiene conexiones en el puerto
                    for conn in proc.connections(kind='inet'):
                        if conn.laddr.port == port:
                            print(f"✅ Encontrado proceso {proc.info['name']} (PID: {proc.info['pid']}) con server.py. Terminando...")
                            proc.kill()
                            killed_any = True
                            break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if not killed_any:
        print(f"ℹ️ Puerto {port} está libre.")
    
    return killed_any


if __name__ == "__main__":
    kill_process_on_port(8000)